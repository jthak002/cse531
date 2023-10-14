from concurrent import futures
import logging

import grpc
import example_pb2
import example_pb2_grpc

class CustomerToBankGRPC(example_pb2_grpc.CustomerTransactionServicer):
    def PerformCustomerTransaction(self, request, context):
        logging.info(f"Received a CUSTOMER request to {request.interface} for cust_id {request.cust_id} with "
                     f"tran_id {request.tran_id} for amount {request.money}")
        return example_pb2.CResponse(cust_id=request.cust_id, tran_id=request.tran_id, interface=request.interface, result='success')

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_CustomerTransactionServicer_to_server(CustomerToBankGRPC(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()

## Test and Debug Only
if __name__ == "__main__":
    logging.basicConfig()
    serve()
