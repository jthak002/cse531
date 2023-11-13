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

    def increment_local_time(self):
        """
        Function to increment localtime of the customer by 1 unit.
        :return: None
        """
        self.localtime += 1
        return self.localtime

    def createStub(self):
        """
        Function to set up the stub for the local customer process
        :return:
        """
        try:
            self.stub = example_pb2_grpc.CustomerTransactionStub(grpc.insecure_channel("localhost:"+str(50000+self.id)))
        except grpc.RpcError:
            logger.error(f"Encountered error while creating stub for sending message to bank for CustomerID#{self.id}")
            logger.debug(sys.exc_info())
            exit(1)
        logger.info(f"Created a gRPC STUB for CustomerID#{self.id}")

    def executeEvents(self):
        temp_list = []
        for event in self.events:
            try:
                fn_localtime = self.increment_local_time()
                logger.info(f"%%% Executing the event with tran_id#{event.get('customer-request-id')} for "
                            f"customerID#{self.id} at local_time: {self.localtime}")
                if event.get('interface') == 'query':
                    response = self.stub.Query(example_pb2.CTransaction(cust_id=self.id,
                                                                        tran_id=event.get('customer-request-id'),
                                                                        interface='query', money=0,
                                                                        localtime=self.localtime))
                    temp_list.append({'customer-request-id': event.get('customer-request-id'),
                                                       'logical_clock': fn_localtime, 'interface': 'query',
                                                       'comment': f'event_sent from customer {self.id}'})
                elif event['interface'] == 'deposit':
                    response = self.stub.Deposit(example_pb2.CTransaction(cust_id=self.id,
                                                                          tran_id=event.get('customer-request-id'),
                                                                        interface='deposit', money=event.get('money'),
                                                                          localtime=self.localtime))
                    temp_list.append({'customer-request-id': event.get("customer-request-id"),
                                                       'logical_clock': fn_localtime, 'interface': 'deposit',
                                                       'comment': f'event_sent from customer {self.id}'})
                elif event['interface'] == 'withdraw':
                    response = self.stub.Withdraw(example_pb2.CTransaction(cust_id=self.id,
                                                                           tran_id=event.get('customer-request-id'),
                                                                          interface='withdraw',
                                                                          money=event.get('money'),
                                                                           localtime=self.localtime))
                    temp_list.append({'customer-request-id': event.get('customer-request-id'),
                                                       'logical_clock': fn_localtime, 'interface': 'withdraw',
                                                       'comment': f'event_sent from customer {self.id}'})
                else:
                    logger.error(f"Encountered Invalid Event for CustomerID#{self.id}; DETAILS OF EVENT- {event}")
                self.shared_list.append(copy.deepcopy({'id': self.id, 'type': 'customer',
                                                      'events': temp_list}))
            except KeyError:
                logger.error(f"Invalid event encountered for CustomerID#{self.id}; DETAILS OF EVENT- {event}")
                continue

    def getMessages(self):
        return {'id': self.id, 'type': 'customer', 'events': copy.deepcopy(self.recvMsg)}

    def branchTerminate(self) -> (bool, dict):
        logger.info(f"Customer with id{self.id} is sending terminate request to branch id {self.id}")
        response = self.stub.Terminate(example_pb2.Bterminate())
        return (True, json.loads(response.event_resp_string)) if response.exit_code == 0 else (False, {})
