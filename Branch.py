import sys
import traceback
from concurrent import futures
import threading
import grpc
import example_pb2
import example_pb2_grpc
import logging
import json

logger = logging.getLogger(__name__)

BASE_PORT = 50000
# setting up max_workers to 1 prevent issues with multiple workers causing race conditions.
MAX_WORKERS = 10


class Branch(example_pb2_grpc.CustomerTransactionServicer):
    id = 0
    balance = 0
    peer_branches = []
    stubList = []
    server = None
    local_time = 0
    events = []
    lock = None

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
                channel = grpc.insecure_channel("localhost:" + str(50000 + peer))
                stub = example_pb2_grpc.CustomerTransactionStub(channel)
                self.stubList.append({'peer_id': peer, 'stub': stub})
        except Exception:
            logger.error("Encountered error while creating stubs from ")
            exit(1)
        logger.info(f"Initializing Branch with ID#{self.id} with peer branches stubs {self.peer_branches}")
        # a list of received messages used for debugging purpose
        self.recvMsg = []
        self.lock = threading.Lock()
        # iterate the processID of the branches
        # TODO: students are expected to store the processID of the branches
        pass

    def compare_set_localtime(self, remote_clock=0, src_branch_id=-1) -> int:
        """
        This function compares the local branch time to the provided remote branch clock time, and if the local branch
        time is less than the remote branch time is lesser than the remote branch time, then it sets the local branch
        time to the value of the remote branch time, according to lamport's logical clock algorithm.
        :param remote_clock: the logical time of the remote process/customer
        :param src_branch_id: the logical time of the local process
        :return: None
        """
        if self.local_time >= remote_clock:
            self.local_time += 1
        else:
            self.local_time = remote_clock + 1
            logger.debug(
                f"Set the localtime for the local_branch id{self.id} to remote_clock time: {remote_clock} from "
                f" {f'remote_branch: {src_branch_id}' if src_branch_id != -1 else 'customer'}")
        return self.local_time

    def increment_local_time(self) -> int:
        """
        Function to increase the local_time of the process by 1. Write this simple statement as a function so that
        future mutexes can be implemented cleanly in this code block itself.
        :return: self.local_time the localtime incremented by 1
        """
        logger.debug(f"incrementing time on branch_id: {self.id}")
        self.local_time += 1
        return self.local_time

    def send_btransaction_message(self, cust_id: int, tran_id: int, src_branch_id, interface: str,
                                  amount: float) -> bool:
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
            with self.lock:
                fn_localtime = self.increment_local_time()
                self.events.append({'customer-request-id': cust_id, 'logical_clock': fn_localtime,
                                    'interface': interface.lower(), 'comment': f'event_sent to branch '
                                                                    f'{stub_dict.get('peer_id')}'})
            logger.debug(f"SENDING BTransaction Message from {src_branch_id} to "
                         f"PEER_BANKID#{stub_dict.get('peer_id')} for cust_id{cust_id} with tran_id{tran_id} for "
                         f"{interface} operation for amount{amount}")
            if interface == "PROPAGATE_DEPOSIT":
                response = stub_dict.get('stub').Propagate_Deposit(
                    example_pb2.BTransaction(cust_id=cust_id, tran_id=tran_id, src_branch_id=self.id,
                                             interface=interface, money=amount,
                                             src_branch_localtime=fn_localtime))

            elif interface == "PROPAGATE_WITHDRAW":
                response = stub_dict.get('stub').Propagate_Withdraw(
                    example_pb2.BTransaction(cust_id=cust_id, tran_id=tran_id, src_branch_id=self.id,
                                             interface=interface, money=amount,
                                             src_branch_localtime=fn_localtime))
            else:
                logger.critical("INVALID INTERFACE in Branch.send_btransaction_message() - exiting now")
                exit(1)
            if response.status:
                # simply pass - no longer performing the remote balance sanity check like before; the balance will
                # not be consistent due the differing requests from each user to the branch.
                pass
            else:
                logger.warning(f"FAILURE SENDING {interface} from {self.id} to {stub_dict.get('peer_id')}")
                return response.status
        return True

    def Query(self, request, context):
        """
        Function to query the bank balance of the customer
        :param request: holds the contents of the gRPC request
        :param context: -
        :return: example_pb2.CResponse Object Type
        """
        with self.lock:
            logging.info(f">>> Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                         f"tran_id {request.tran_id} at localtime {self.local_time}")
            self.compare_set_localtime(remote_clock=request.localtime)
            self.events.append({'customer-request-id': request.cust_id, 'logical_clock': self.local_time, 'interface':
                                'query', 'comment': f'query_recv from {request.cust_id}'})
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
        with self.lock:
            deposit_amount = request.money
            logging.info(f">>> Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                         f"tran_id {request.tran_id} at localtime {self.local_time}")
            fn_localtime = self.compare_set_localtime(remote_clock=request.localtime)
            self.events.append({'customer-request-id': request.cust_id, 'logical_clock': fn_localtime,
                                'interface': 'deposit', 'comment': f'event_recv from customer {request.cust_id}'})
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
        transaction_status: str = 'success' if propagate_status else 'failure'

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
        with self.lock:
            withdraw_amount = request.money
            logging.info(f">>> Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                         f"tran_id {request.tran_id} at localtime {self.local_time}")
            fn_localtime = self.compare_set_localtime(remote_clock=request.localtime)
            self.events.append({'customer-request-id': request.cust_id, 'logical_clock': fn_localtime,
                                'interface': 'withdraw', 'comment': f'event_recv from customer {request.cust_id}'})
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
        transaction_status: str = 'success' if propagate_status else 'failure'

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
        with self.lock:
            deposit_amount = request.money
            logging.debug(f"Received a BRANCH DEPOSIT PROPAGATION request to {request.interface} for cust_id "
                          f"{request.cust_id} with tran_id {request.tran_id}")
            fn_localtime = self.compare_set_localtime(remote_clock=request.src_branch_localtime)
            self.events.append({'customer-request-id': request.cust_id, 'logical_clock': fn_localtime,
                                'interface': 'propogate_deposit', 'comment': f'event_recv from branch '
                                                                             f'{request.src_branch_id}'})
            self.balance += deposit_amount
        transaction_status = True
        logger.info(f"BRANCH with ID#{self.id} has the balance INCREASED by {request.money} for {request.cust_id} To "
                    f"BALANCE {self.balance} via BRANCH DEPOSIT PROPAGATION from BRANCH_ID{request.src_branch_id} "
                    f"with tran_id: {request.tran_id}")
        logging.debug(f"Returning a CUSTOMER response for {request.interface} for cust_id {request.cust_id} with "
                      f"tran_id {request.tran_id} with {transaction_status}")
        return example_pb2.BResponse(cust_id=self.id, tran_id=request.tran_id, interface=request.interface,
                                     money=self.balance, status=transaction_status)

    def Propagate_Withdraw(self, request, context):
        """
        Function to Propagate Withdraw money into the bank balance of the customer
        :param request: holds the contents of the gRPC request
        :param context: -
        :return: example_pb2.BResponse Object Type
        """
        with self.lock:
            withdraw_amount = request.money
            logging.debug(f"Received a BRANCH WITHDRAWAL PROPAGATION request to {request.interface} for cust_id "
                          f"{request.cust_id} with tran_id {request.tran_id}")
            fn_localtime = self.compare_set_localtime(remote_clock=request.src_branch_localtime)
            self.events.append({'customer-request-id': request.cust_id, 'logical_clock': fn_localtime,
                                'interface': 'propogate_withdraw', 'comment': f'event_recv from branch '
                                                                              f'{request.src_branch_id}'})
            self.balance -= withdraw_amount
        logger.info(f"BRANCH with ID#{self.id} has the balance DECREASED by {request.money} for cust_id "
                    f"{request.cust_id} To BALANCE {self.balance} via BRANCH WITHDRAW PROPAGATION from "
                    f"BRANCH_ID{request.src_branch_id} with tran_id: {request.tran_id}")
        logging.debug(f"Returning a BRANCH WITHDRAW PROPAGATION response for {request.interface} for cust_id "
                      f"{request.cust_id} with tran_id {request.tran_id} with status {True}")
        return example_pb2.BResponse(cust_id=self.id, tran_id=request.tran_id, interface=request.interface,
                                     money=self.balance, status=True)

    def Terminate(self, request, context):
        """
        Function to terminate the branch and write the events to file.
        :param request: grpc variable which stores the contents of the `Bterminate` RPC message from client
        :param context: grpc variable for context
        :return example_pb2.BTerminate_Status type object
        """
        logger.info(f"Received request to terminate branch with ID: {self.id}")
        exit_code = 0
        event_list_str = ''
        try:
            logger.info(f"Wrote the events for branch_id {self.id} to `event_list_str` variable")
            event_list_str = json.dumps({'id': self.id, 'type': 'branch', 'events': self.events})
            self.server.stop(grace=0)
        except Exception:
            logger.error(f"Could not send the response back to customer because of exception {sys.exc_info()}")
            exit_code = 1
        return example_pb2.Bterminate_Status(exit_code=exit_code, event_resp_string=event_list_str)

    def branch_grpc_serve(self):
        logging.info(f"Starting branch server on localhost with {self.port}")
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
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
