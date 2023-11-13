import logging
import json
from Customer import Customer
from multiprocessing import Process, Manager

logger = logging.getLogger(__name__)


def read_customer_json(filepath: str):
    logger.info(f"Reading the FILEPATH {filepath} for customer initialization events")
    with open(filepath, 'r') as input_test_file:
        file_contents = input_test_file.read()

    input_tests = json.loads(file_contents)
    input_test_file.close()
    logger.debug(f"Read the following events: {input_tests}")
    return input_tests


def create_customer_objects(input_tests: dict):
    # list to store the details of every bank process
    customer_list = []
    logger.info("parsing & filtering the the list of customer initialization events in the input.json file")
    for input_test in input_tests:
        if input_test.get('type') == "customer":
            customer_list.append(Customer(id=input_test.get('id'), events=input_test.get('customer-requests')))
    return customer_list


def execute_customer_events(customer_list, output_filename:str):
    response_list = []
    customer_process_list = []
    logger.info("creating and starting individual processes for each customer")
    try:
        for customer in customer_list:
            customer.createStub()
            process = Process(target=customer.executeEvents, args=shared_list)
            customer_process_list.append(process)
            process.start()
    except KeyboardInterrupt:
        logger.error("Encountered Keyboard Interrupt in the middle of initializing the customer processes - terminating"
                     " all the half initialized and running customer processes")
        for customer_process in customer_process_list:
            customer_process.terminate()
        logger.info("No Output since the program was exited half way through")
        return customer_list

    # herding all the customer processes and fetching the outputs after execution
    # -joining the execution of all the customer processes
    for customer_process in customer_process_list:
        customer_process.join()
    # -gathering the output from all the process
    for customer in customer_list:
        dict_response = customer.getMessages()
        logger.debug(f"#### {dict_response}")
        response_list.append(dict_response)
    with open(output_filename,'w') as customer_output:
        customer_output.write(json.dumps(response_list))
        customer_output.close()
    return customer_list


if __name__ == '__main__':
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(level=logging.INFO)
    logger.addHandler(handler)
    input_tests = read_customer_json(filepath="./input_small.json")
    customer_list = create_customer_objects(input_tests)
    execute_customer_events(customer_list)

