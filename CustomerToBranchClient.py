from __future__ import print_function

import grpc
import example_pb2
import example_pb2_grpc
import logging

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    logging.info("Sending a request for cust_id=29, tran_id=69, interface=\'deposit\', money=340 ")
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = example_pb2_grpc.CustomerTransactionStub(channel)
        response = stub.PerformCustomerTransaction(example_pb2.CTransaction(cust_id=29, tran_id=69, interface='deposit', money=340))
    logging.info(f"Customer Stub client received: cust_id={response.cust_id}, tran_id={response.tran_id}, "
                 f"interface={response.interface} with the result code={response.result}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run()