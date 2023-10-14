# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import example_pb2 as example__pb2


class CustomerTransactionStub(object):
    """Interface for Customer To Bank Transaction
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PerformCustomerTransaction = channel.unary_unary(
                '/example.CustomerTransaction/PerformCustomerTransaction',
                request_serializer=example__pb2.CTransaction.SerializeToString,
                response_deserializer=example__pb2.CResponse.FromString,
                )


class CustomerTransactionServicer(object):
    """Interface for Customer To Bank Transaction
    """

    def PerformCustomerTransaction(self, request, context):
        """A simple RPC.
        
        Sends a CTransaction Type
        
        A CResponse is returned with the new balance of the account.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CustomerTransactionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PerformCustomerTransaction': grpc.unary_unary_rpc_method_handler(
                    servicer.PerformCustomerTransaction,
                    request_deserializer=example__pb2.CTransaction.FromString,
                    response_serializer=example__pb2.CResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'example.CustomerTransaction', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CustomerTransaction(object):
    """Interface for Customer To Bank Transaction
    """

    @staticmethod
    def PerformCustomerTransaction(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/example.CustomerTransaction/PerformCustomerTransaction',
            example__pb2.CTransaction.SerializeToString,
            example__pb2.CResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
