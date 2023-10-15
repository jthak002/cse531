from concurrent import futures
import grpc
import example_pb2
import example_pb2_grpc
import logging

logger = logging.getLogger(__name__)


BASE_PORT = 50000

class Branch(example_pb2_grpc.CustomerTransactionServicer):
    id = 0
    balance = 0
    peer_branches = []
    stubList = []
    server = None
    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        logger.info(f"Initializing Branch with ID#{self.id}")
        self.port = str(BASE_PORT + id)
        # replica of the Branch's balance
        self.balance = balance
        logger.info(f"Initializing Branch with ID#{self.id} with balance: {self.balance}")
        # the list of process IDs of the branches
        self.peer_branches = branches
        logger.info(f"Initializing Branch List with ID#{self.id} with peer branches: {self.peer_branches}")
        # the list of Client stubs to communicate with the branches
        self.stubList = []
        try:
            for peer in self.peer_branches:
                logger.debug(f"Setting up gRPC channel between {self.id} and {peer}")
                channel = grpc.insecure_channel("localhost:"+str(50000+peer))
                stub = example_pb2_grpc.CustomerTransactionStub(channel)
                self.stubList.append({'peer_id': peer, 'stub': stub})
        except Exception:
            logger.error("Encountered error while creating stubs from ")
            exit(1)
        logger.info(f"Initializing Branch with ID#{self.id} with peer branches stubs {self.peer_branches}")
        # a list of received messages used for debugging purpose
        self.recvMsg = []
        # iterate the processID of the branches
        # TODO: students are expected to store the processID of the branches
        pass

    def send_btransaction_message(self, cust_id:int, tran_id:int, src_branch_id, interface:str, amount:float) -> bool:
        """
        Function to propagate deposit or withdraw from branch to peer branches
        :param cust_id: customer id of the account - right now the same as the account
        :param tran_id: transaction id of the account
        :param src_branch_id: the id of the branch initiating the source transaction
        :param interface: either PROPAGATE_DEPOSIT or PROPAGATE_WITHDRAW
        :param amount: The amount to deposit or withdraw
        :return: True if all nodes received the transaction properly, else False
        """
        for stub_dict in self.stubList:
            logger.debug(f"SENDING BTransaction Message from {src_branch_id} to PEER_BANKID#{stub_dict.get('peer_id')} for "
                        f"cust_id{cust_id} with tran_id{tran_id} for {interface} operation for amount{amount}")
            if interface == "PROPAGATE_DEPOSIT":
                response = stub_dict.get('stub').Propagate_Deposit(example_pb2.BTransaction(cust_id=cust_id,
                                                                                        tran_id=tran_id,
                                                                                        src_branch_id=self.id,
                                                                                        interface=interface,
                                                                                        money=amount))
            elif interface == "PROPAGATE_WITHDRAW":
                response = stub_dict.get('stub').Propagate_Withdraw(example_pb2.BTransaction(cust_id=cust_id,
                                                                                            tran_id=tran_id,
                                                                                            src_branch_id=self.id,
                                                                                            interface=interface,
                                                                                            money=amount))
            else:
                logger.critical("INVALID INTERFACE in Branch.send_btransaction_message() - exiting now")
                exit(1)
            if response.status:
                # SANITY CHECK THAT PROPAGATION WENT SUCCESSFULLY
                if self.balance == response.money:
                    pass
                else:
                    logger.critical("self.balance DOES NOT MATCH response.money - ABORT")
                logger.debug(f"SUCCESSFULLY SENT {interface} from {self.id} to {stub_dict.get('peer_id')}")
            else:
                logger.warning(f"FAILURE SENDING {interface} from {self.id} to {stub_dict.get('peer_id')}")
                return response.status
        return True


    # TODO: students are expected to process requests from both Client and Branch
    def MsgDelivery(self,request, context):
        pass


    def Query(self, request, context):
        """
        Function to query the bank balance of the customer
        :param request: holds the contents of the gRPC request
        :param context: -
        :return: example_pb2.CResponse Object Type
        """
        logging.info(f">>> Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id}")
        balance_str = 'balance: ' + str(self.balance)
        logging.info(f"Returning a CUSTOMER response for {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id} as {balance_str}")
        return example_pb2.CResponse(cust_id=self.id, tran_id=request.tran_id, interface=request.interface,
                                     result=balance_str)

    def Deposit(self, request, context):
        """
        Function to Deposit money into the bank balance of the customer
        :param request: holds the contents of the gRPC request
        :param context: -
        :return: example_pb2.CResponse Object Type
        """
        deposit_amount = request.money
        logging.info(f">>> Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id}")
        self.balance += deposit_amount
        ###################################
        # CODE FOR PROPAGATING BALANCE HERE
        propagate_status = self.send_btransaction_message(cust_id=request.cust_id, tran_id=request.tran_id,
                                                          src_branch_id=self.id, interface='PROPAGATE_DEPOSIT',
                                                          amount=request.money)
        ###################################
        if propagate_status:
            logger.debug(
                f"BRANCH with ID#{self.id} has the balance INCREASED by {request.money} To BALANCE {self.balance} "
                f"via CUSTOMER DEPOSIT with tran_id: {request.tran_id}")
        else:
            logger.warning(f"DEPOSIT FAILED for ID#{self.id} with PROPAGATE DEPOSIT FAILURE")
        transaction_status:str = 'success' if propagate_status else 'failure'

        logging.info(f"Returning a CUSTOMER response for {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id} as {transaction_status}")
        return example_pb2.CResponse(cust_id=self.id, tran_id=request.tran_id, interface=request.interface,
                                     result=transaction_status)

    def Withdraw(self, request, context):
        """
        Function to Withdraw money into the bank balance of the customer
        :param request: holds the contents of the gRPC request
        :param context: -
        :return: example_pb2.CResponse Object Type
        """
        withdraw_amount = request.money
        logging.info(f">>> Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id}")
        self.balance -= withdraw_amount
        ###################################
        # CODE FOR PROPAGATING BALANCE HERE
        propagate_status = self.send_btransaction_message(cust_id=request.cust_id, tran_id=request.tran_id,
                                                          src_branch_id=self.id, interface='PROPAGATE_WITHDRAW',
                                                          amount=request.money)
        ###################################
        if propagate_status:
            logger.debug(
                f"BRANCH with ID#{self.id} has the balance DECREASED by {request.money} To BALANCE {self.balance} "
                f"via CUSTOMER WITHDRAWAL with tran_id: {request.tran_id}")
        else:
            logger.warning(f"WITHDRAWAL FAILED for ID#{self.id} with PROPAGATE WITHDRAW FAILURE")
        transaction_status:str = 'success' if propagate_status else 'failure'

        logging.info(f"Returning a CUSTOMER response for {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id} as {transaction_status}")
        return example_pb2.CResponse(cust_id=self.id, tran_id=request.tran_id, interface=request.interface,
                                     result=transaction_status)

    def Propagate_Deposit(self, request, context):
        """
        Function to Propagate Deposit money into the bank balance of the customer
        :param request: holds the contents of the gRPC request
        :param context: -
        :return: example_pb2.BResponse Object Type
        """
        deposit_amount = request.money
        logging.debug(f"Received a BRANCH DEPOSIT PROPAGATION request to {request.interface} for cust_id "
                     f"{request.cust_id} with tran_id {request.tran_id}")
        self.balance += deposit_amount
        transaction_status = True
        logger.info(f"BRANCH with ID#{self.id} has the balance INCREASED by {request.money} for {request.cust_id} To "
                    f"BALANCE {self.balance} via BRANCH DEPOSIT PROPAGATION from BRANCH_ID{request.src_branch_id} "
                    f"with tran_id: {request.tran_id}")
        logging.debug(f"Returning a CUSTOMER response for {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id} with {transaction_status}")
        return example_pb2.BResponse(cust_id=self.id, tran_id=request.tran_id, interface=request.interface,
                                     money=self.balance, status = transaction_status)

    def Propagate_Withdraw(self, request, context):
        """
        Function to Propagate Withdraw money into the bank balance of the customer
        :param request: holds the contents of the gRPC request
        :param context: -
        :return: example_pb2.BResponse Object Type
        """
        withdraw_amount = request.money
        logging.debug(f"Received a BRANCH WITHDRAWAL PROPAGATION request to {request.interface} for cust_id "
                     f"{request.cust_id} with tran_id {request.tran_id}")
        self.balance -= withdraw_amount
        logger.info(f"BRANCH with ID#{self.id} has the balance DECREASED by {request.money} for cust_id "
                    f"{request.cust_id} To BALANCE {self.balance} via BRANCH WITHDRAW PROPAGATION from "
                    f"BRANCH_ID{request.src_branch_id} with tran_id: {request.tran_id}")
        logging.debug(f"Returning a BRANCH WITHDRAW PROPAGATION response for {request.interface} for cust_id "
                     f"{request.cust_id} with tran_id {request.tran_id} with status {True}")
        return example_pb2.BResponse(cust_id=self.id, tran_id=request.tran_id, interface=request.interface,
                                     money=self.balance, status=True)

    def branch_grpc_serve(self):
        logging.info(f"Starting branch server on localhost with {self.port}")
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        example_pb2_grpc.add_CustomerTransactionServicer_to_server(self, self.server)
        self.server.add_insecure_port("[::]:" + self.port)
        self.server.start()
        logging.info("Branch Server started, listening on " + self.port)
        self.server.wait_for_termination()


if __name__ == '__main__':
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    logger.addHandler(console)
    logger.info(f"Trying to start branch process with ID: {1}")
    test_branch = Branch(id=0, balance=400, branches=[])
    test_branch.branch_grpc_serve()