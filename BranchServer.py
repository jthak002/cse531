from concurrent import futures
import grpc
import example_pb2
import example_pb2_grpc

import logging

def serve():
    port = "50051"
    logging.info(f"Starting branch server on process{int(port)%50000}")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_CustomerTransactionServicer_to_server(CustomerToBankGRPC(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info("Server started, listening on " + port)
    server.wait_for_termination()

## Test and Debug Only
if __name__ == "__main__":
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    logger.addHandler(console)
    logger = logging.getLogger(__name__)
    logger.info("Starting Branch Process")
    serve()
