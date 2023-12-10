import grpc
import example_pb2
import example_pb2_grpc
import sys
import time
import logging
import json
import copy

logger = logging.getLogger(__name__)

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = []
        # pointer for the stub
        self.stub = None
        # variable to track localtime
        self.localtime = 0
        self.shared_list = None
        self.last_write_id = 'NO_WRITE_YET'

    def increment_local_time(self):
        """
        Function to increment localtime of the customer by 1 unit.
        :return: None
        """
        self.localtime += 1
        return self.localtime

    def createStub(self, branch_id):
        """
        Function to set up the stub for the local customer process
        :return:
        """
        try:
            self.stub = example_pb2_grpc.CustomerTransactionStub(grpc.insecure_channel("localhost:"+str(50000+branch_id)))
        except grpc.RpcError:
            logger.error(f"Encountered error while creating stub for sending message to bank for CustomerID#{self.id} "
                         f"to communicate with branch_id")
            logger.debug(sys.exc_info())
            exit(1)
        logger.info(f"Created a gRPC STUB for CustomerID#{self.id}")

    def executeEvents(self):
        temp_list = []
        for event in self.events:
            try:
                self.createStub(branch_id=event.get('branch'))
                fn_localtime = self.increment_local_time()
                logger.info(f"%%% Executing the event with tran_id#{event.get('customer-request-id')} for "
                            f"customerID#{self.id} at local_time: {self.localtime}")
                if event.get('interface') == 'query':
                    response = self.stub.Query(example_pb2.CTransaction(cust_id=self.id,
                                                                        tran_id=event.get('id'),
                                                                        interface='query', money=0,
                                                                        localtime=self.localtime,
                                                                        prev_writeset_id=self.last_write_id))
                    temp_list.append({'id': self.id,'recv':[{'interface': 'query', 'balance': response.money,
                                                             'branch': event.get('branch')}]})
                elif event['interface'] == 'deposit':
                    response = self.stub.Deposit(example_pb2.CTransaction(cust_id=self.id,
                                                                          tran_id=event.get('id'),
                                                                          interface='deposit',
                                                                          money=event.get('money'),
                                                                          localtime=self.localtime,
                                                                          prev_writeset_id=self.last_write_id))
                    self.last_write_id = response.curr_writeset_id
                    temp_list.append({'id': self.id, 'recv': [{'id': event.get('id'), 'interface': 'deposit',
                                                               'result': response.result}]})
                elif event['interface'] == 'withdraw':
                    response = self.stub.Withdraw(example_pb2.CTransaction(cust_id=self.id,
                                                                           tran_id=event.get('id'),
                                                                           interface='withdraw',
                                                                           money=event.get('money'),
                                                                           localtime=self.localtime,
                                                                           prev_writeset_id=self.last_write_id))
                    self.last_write_id = response.curr_writeset_id
                    temp_list.append({'id': self.id, 'recv': [{'id': event.get('id'), 'interface': 'withdraw',
                                                               'result': response.result}]})
                else:
                    logger.error(f"Encountered Invalid Event for CustomerID#{self.id}; DETAILS OF EVENT- {event}")
            except KeyError:
                logger.error(f"Invalid event encountered for CustomerID#{self.id}; DETAILS OF EVENT- {event}")
                continue
        self.shared_list=copy.deepcopy(temp_list)

    def getMessages(self):
        return {'id': self.id, 'type': 'customer', 'events': copy.deepcopy(self.recvMsg)}

    def branchTerminate(self) -> (bool, dict):
        logger.info(f"Customer with id{self.id} is sending terminate request to branch id {self.id}")
        response = self.stub.Terminate(example_pb2.Bterminate())
        return (True, json.loads(response.event_resp_string)) if response.exit_code == 0 else (False, {})
