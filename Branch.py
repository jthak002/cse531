from concurrent import futures
import grpc
import example_pb2
import example_pb2_grpc
import logging

logger = logging.getLogger(__name__)


BASE_PORT = 50000

class CustomerToBankGRPC(example_pb2_grpc.CustomerTransactionServicer):
    def Query(self, request, context):
        logging.info(f"Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id} for amount {request.money}")
        return example_pb2.CResponse(cust_id=request.cust_id, tran_id=request.tran_id, interface=request.interface, result='success')

class Branch(example_pb2_grpc.CustomerTransactionServicer):
    id = 0
    balance = 0
    branches = []
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
        self.branches = branches
        logger.info(f"Initializing Branch with ID#{self.id} with peer branches: {self.branches}")
        # the list of Client stubs to communicate with the branches
        self.stubList = []
        # a list of received messages used for debugging purpose
        self.recvMsg = []
        # iterate the processID of the branches
        # TODO: students are expected to store the processID of the branches
        pass

    def setup_stub_list(self):
        logger.info(f"The stubs for BRANCH ID# {self.id} seem to be uninitialized. Creating now.")
        try:
            for peer in self.branches:
                logger.debug(f"Setting up gRPC channel between {self.id} and {peer}")
                channel = grpc.insecure_channel("localhost:"+str(50000+peer))
                stub = example_pb2_grpc.CustomerTransactionStub(channel)
                self.stubList.append({'peer_id': peer, 'stub': stub})
        except Exception:
            logger.error("Encountered error while creating stubs from ")
            exit(1)
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
        logging.info(f"Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
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
        logging.info(f"Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id}")
        self.balance += deposit_amount
        ###################################
        # CODE FOR PROPAGATING BALANCE HERE
        propagate_status = True
        ###################################
        if propagate_status:
            logger.info(
                f"BRANCH with ID#{self.id} has the balance INCREASED by {request.money} To BALANCE {self.balance} "
                f"via CUSTOMER DEPOSIT with tran_id: {request.tran_id}")
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
        logging.info(f"Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id}")
        self.balance -= withdraw_amount
        ###################################
        # CODE FOR PROPAGATING BALANCE HERE
        propagate_status = True
        ###################################
        if propagate_status:
            logger.info(
                f"BRANCH with ID#{self.id} has the balance DECREASED by {request.money} To BALANCE {self.balance} "
                f"via CUSTOMER WITHDRAWAL with tran_id: {request.tran_id}")
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
        logging.info(f"Received a BRANCH DEPOSIT PROPAGATION request to {request.interface} for cust_id "
                     f"{request.cust_id} with tran_id {request.tran_id}")
        self.balance += deposit_amount
        transaction_status = 'SUCCESS'
        logger.info(f"BRANCH with ID#{self.id} has the balance INCREASED by {request.money} for {request.cust_id} To "
                    f"BALANCE {self.balance} via BRANCH DEPOSIT PROPAGATION from BRANCH_ID{request.src_branch_id} "
                    f"with tran_id: {request.tran_id}")
        logging.info(f"Returning a CUSTOMER response for {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id} with {transaction_status}")
        return example_pb2.BResponse(cust_id=self.id, tran_id=request.tran_id, interface=request.interface,
                                     result=transaction_status)

    def Propagate_Withdraw(self, request, context):
        """
        Function to Propagate Withdraw money into the bank balance of the customer
        :param request: holds the contents of the gRPC request
        :param context: -
        :return: example_pb2.BResponse Object Type
        """
        deposit_amount = request.money
        logging.info(f"Received a BRANCH WITHDRAWAL PROPAGATION request to {request.interface} for cust_id "
                     f"{request.cust_id} with tran_id {request.tran_id}")
        self.balance -= deposit_amount
        logger.info(f"BRANCH with ID#{self.id} has the balance DECREASED by {request.money} for cust_id "
                    f"{request.cust_id} To BALANCE {self.balance} via BRANCH WITHDRAW PROPAGATION from "
                    f"BRANCH_ID{request.src_branch_id} with tran_id: {request.tran_id}")
        logging.info(f"Returning a BRANCH WITHDRAW PROPAGATION response for {request.interface} for cust_id "
                     f"{request.cust_id} with tran_id {request.tran_id} with status {True}")
        return example_pb2.BResponse(cust_id=self.id, tran_id=request.tran_id, interface=request.interface,
                                     status=True)

    def branch_grpc_serve(self):
        logging.info(f"Starting branch server on process{self.port}")
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