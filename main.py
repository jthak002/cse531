import copy
import logging
import argparse
import time
import json

from runBranch import read_json, create_bank_processes_dict, create_bank_processes
from runCustomer import read_customer_json, create_customer_objects, execute_customer_events

logger = logging.getLogger(__name__)

CUSTOMER_OUTPUT_FILEPATH = './tests/'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str,
                        help="The path of the file which contains the input events")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Change the verbosity of logs to DEBUG. default is INFO")
    args = parser.parse_args()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    if args.verbose:
        logger.setLevel(level=logging.DEBUG)
    else:
        logger.setLevel(level=logging.INFO)
    logger.addHandler(handler)

    logging.info("Starting the test script. Setting up the Bank Branches.")
    input_tests = read_json(filepath=args.filepath)
    branch_list = create_bank_processes_dict(input_tests=input_tests)
    branch_processes = create_bank_processes(branch_list=branch_list)
    logger.info("Sleeping for 10s to give all the Branch Processes time to setup.")
    time.sleep(10)

    logging.info("Setting up the customer events.")
    input_tests = read_customer_json(filepath=args.filepath)
    customer_list = create_customer_objects(input_tests=input_tests, output_filepath=CUSTOMER_OUTPUT_FILEPATH)
    execute_customer_events(customer_list=customer_list)

    logging.info(f"You can find the output for the customers in `{CUSTOMER_OUTPUT_FILEPATH}/customer_output.x.json` "
                 f"where x is the customer ID.")
