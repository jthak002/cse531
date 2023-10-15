import copy
from concurrent import futures
import grpc
import example_pb2
import example_pb2_grpc
import logging
import json
from Branch import Branch
from multiprocessing import Process, Event


handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
logger.addHandler(handler)
logger = logging.getLogger()


def read_json(filepath: str):
    logger.info(f"Reading the FILEPATH {filepath} for branch initialization events")
    with open('input_small.json', 'r') as input_test_file:
        file_contents = input_test_file.read()

    input_tests = json.loads(file_contents)
    input_test_file.close()
    logger.debug(f"Read the following events: {input_tests}")
    return input_tests


def create_bank_processes_dict(input_tests: dict):
    # list to store the details of every bank process
    branch_list = []
    # list to store the
    branch_peers_list = []
    logger.info("parsing & filtering the the list of bank initialization events in the input.json file")
    for input_test in input_tests:
        if input_test.get('type') == "branch":
            branch_peers_list.append(input_test.get('id'))
            branch_list.append({'id': input_test.get('id'), 'balance': input_test.get('balance')})
    logger.debug(f"The branch_peers_list is {branch_peers_list}")
    logger.info("creating a final list of dicts with the bank process information which contains the list of peer banks"
                "minus the self_id")
    for branch in branch_list:
        branch_id = branch.get('id')
        branch['branch_peers_list'] = [peer for peer in branch_peers_list if peer != branch_id]
    logger.debug(f"The final bank process list is: {branch_list}")
    return branch_list


def create_bank_processes(branch_list: list):
    branch_objects = []
    branch_processes = []
    logger.info(f"Starting the bank processes for serving {len(branch_list)} gRPC processes.")
    try:
        for branch in branch_list:
            branch_object = Branch(id=branch.get('id'), balance=branch.get('balance'),
                                     branches=branch.get('branch_peers_list'))
            branch_objects.append(branch_object)
            process = Process(target=branch_object.branch_grpc_serve)
            branch_processes.append(process)
            process.start()
        for process in branch_processes:
            process.join()

    except KeyboardInterrupt:
        logger.warning("Received KeyboardInterruptException - Terminating now.")
        for process in branch_processes:
            process.terminate()


if __name__ == '__main__':
    input_tests = read_json(filepath="./input_small.json")
    branch_list = create_bank_processes_dict(input_tests=input_tests)
    create_bank_processes(branch_list=branch_list)
