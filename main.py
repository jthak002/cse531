import copy
import logging
import argparse
import time
import json

from runBranch import read_json, create_bank_processes_dict, create_bank_processes
from runCustomer import read_customer_json, create_customer_objects, execute_customer_events

logger = logging.getLogger(__name__)

BRANCH_OUTPUT_FILENAME = './tests/branch_output.json'
CUSTOMER_OUTPUT_FILENAME = './tests/customer_output.json'
EVENTS_OUTPUT_FILENAME = './tests/event_output.json'

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
    customer_list = create_customer_objects(input_tests)
    execute_customer_events(customer_list=customer_list, output_filename=CUSTOMER_OUTPUT_FILENAME)
    time.sleep(10)
    logging.info("Script execution is complete. Sending terminate signal to all of the Branch Processes")
    # writing the server output to file.
    server_event_list = []
    for customer in customer_list:
        status, response_dict = customer.branchTerminate()
        if status:
            logger.info(f"processed server events for branch {customer.id}")
            server_event_list.append(response_dict)
        else:
            logger.error("Encountered error while parsing branch event output")
            server_event_list.append(response_dict)
    with open(BRANCH_OUTPUT_FILENAME, 'w') as fd:
        fd.write(json.dumps(server_event_list))
        fd.close()

    # collating the events_json from both processes
    with open(CUSTOMER_OUTPUT_FILENAME, 'r') as customer_fd:
        customer_events_list = json.loads(customer_fd.read())
        customer_fd.close()
    with open(BRANCH_OUTPUT_FILENAME, 'r') as branch_fd:
        branch_events_list = json.loads(branch_fd.read())
        branch_fd.close()

    collated_events_list = []
    for events in branch_events_list:
        cust_id = events.get('id')
        cust_type = events.get('type')
        for event in events.get('events'):
            temp_dict = copy.deepcopy(event)
            temp_dict['id'] = cust_id
            temp_dict['type'] = cust_type
            collated_events_list.append(temp_dict)

    for events in customer_events_list:
        br_id = events.get('id')
        br_type = events.get('type')
        for event in events.get('events'):
            temp_dict = copy.deepcopy(event)
            temp_dict['id'] = br_id
            temp_dict['type'] = br_type
            collated_events_list.append(temp_dict)

    # sorted_by_cust_id_and_logical_clock =
    # sorted(collated_events_list, key=lambda x: (x['customer-request-id'], x['logical_clock']))

    with open(EVENTS_OUTPUT_FILENAME, 'w') as event_fd:
        event_fd.write(json.dumps(collated_events_list))
        event_fd.close()


    # for process in branch_processes:
    #    process.terminate()
    logging.info(f"You can find the output for the customers in `{CUSTOMER_OUTPUT_FILENAME}`,  "
                 f"and the output for branches in `{BRANCH_OUTPUT_FILENAME}`, and the output for events in "
                 f"{EVENTS_OUTPUT_FILENAME}")
