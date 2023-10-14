from concurrent import futures
import logging

import grpc
import example_pb2
import example_pb2_grpc

class CustomerToBankGRPC(example_pb2_grpc.CustomerTransactionServicer):
    def PerformCustomerTransaction(self, request, context):
        return example_pb2.CResponse(cust_id=29, tran_id=29, interface='test', result='success')

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_CustomerTransactionServicer_to_server(CustomerToBankGRPC(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()
