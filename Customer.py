import grpc
import example_pb2
import example_pb2_grpc
import sys
import time
import logging
import json

logger = logging.getLogger(__name__)

class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None

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
        for event in self.events:
            try:
                response_record = {}
                logger.info(f"%%% Executing the event with tran_id#{event.get('id')} for customerID#{self.id}")
                if event.get('interface') == 'query':
                    response = self.stub.Query(example_pb2.CTransaction(cust_id=self.id, tran_id=event.get('id'),
                                                                        interface='query', money=0))
                    response_record = {'interface': 'query', 'result': response.result}
                elif event['interface'] == 'deposit':
                    response = self.stub.Deposit(example_pb2.CTransaction(cust_id=self.id, tran_id=event.get('id'),
                                                                        interface='deposit', money=event.get('money')))
                    response_record = {'interface': 'deposit', 'result': response.result}
                elif event['interface'] == 'withdraw':
                    response = self.stub.Withdraw(example_pb2.CTransaction(cust_id=self.id, tran_id=event.get('id'),
                                                                          interface='withdraw',
                                                                          money=event.get('money')))
                    response_record = {'interface': 'withdraw', 'result': response.result}
                else:
                    logger.error(f"Encountered Invalid Event for CustomerID#{self.id}; DETAILS OF EVENT- {event}")
                self.recvMsg.append(response_record)

            except KeyError:
                logger.error(f"Invalid event encountered for CustomerID#{self.id}; DETAILS OF EVENT- {event}")
                continue

    def getMessages(self):
        return {'id': self.id, 'recv': self.recvMsg}
