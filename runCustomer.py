import logging
import json
from Customer import Customer

logger = logging.getLogger(__name__)


def read_customer_json(filepath: str):
    logger.info(f"Reading the FILEPATH {filepath} for customer initialization events")
    with open('input_small.json', 'r') as input_test_file:
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
            customer_list.append(Customer(id=input_test.get('id'), events=input_test.get('events')))
    return customer_list

def execute_customer_events(customer_list):
    response_list = []
    for customer in customer_list:
        customer.createStub()
        customer.executeEvents()
        dict_response = customer.getMessages()
        logger.info(f"#### {dict_response}")
        response_list.append(dict_response)
    with open('customer_output.json','a') as customer_output:
        customer_output.write(json.dumps(response_list))
        customer_output.close()


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

