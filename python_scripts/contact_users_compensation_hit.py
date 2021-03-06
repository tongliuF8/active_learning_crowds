
"""
create_compensation_hit.py
create_qualification.py
assign_worker_qualification.py
"""
import sys, csv

from create_compensation_hit import create_hit, get_client
from create_qualification import create_qualification_typeID
from insert_data_into_mongodb import get_data_path
from helper_functions import get_timestamp, get_log_directory
from AMT_parameters import get_URL_parameters

SUBJECT = "Apology and payment updates for \"Identify Work-Related Details Of Tweets\" HIT"

MESSAGE_Emailgroup = "Thank you for taking part in our tasks and providing useful feedback to us. We sincerely apologize for the inconvenience that is caused by our system. We appreciate your contributions and will pay you $0.07 for each data item you labeled, according to our records. Additionally, we will pay you extra $0.50 for your feedback to help improve our system. We warmly welcome you to participate in our future tasks. Wish you have a nice day!\n\nTo complete the payment process, please visit the provided URL in the message to submit a HIT designed specifically for you. Mechanical Turk will then process the payment in the form of the bonus as we promised. You will have 72 hours to complete the HIT. If you need more time or have any comments or feedback to our tasks, please feel free to leave us a message.\n\nRegards,\nChristopher M. Homan"

MESSAGE_others = "Thank you for taking part in our tasks. We sincerely apologize for the inconvenience that is caused by our system. We appreciate your contributions and will pay you $0.07 for each data item you labeled, according to our records. Additionally, we will pay you extra $0.20 for your troubles. We warmly welcome you to participate in our future tasks. Wish you have a nice day!\n\nTo complete the payment process, please visit the provided URL in the message to submit a HIT designed specifically for you. Mechanical Turk will then process the payment in the form of the bonus as we promised. You will have 72 hours to complete the HIT. If you need more time or have any comments or feedback to our tasks, please feel free to leave us a message.\n\nRegards,\nChristopher M. Homan"

def get_worker_id():

    worker_id_list = []

    with open(get_data_path() + "/hit_report2.csv") as csvfile:
        next(csvfile)
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if row[1].strip():
                worker_id_list.append(row[1].strip())

    return worker_id_list

def get_Emailgroup():
    
    Emailgroup = set()
    with open(get_data_path() + '/email_received_worker_id') as input_file:
        for line in input_file:
            Emailgroup.add(line.strip())

    return list(Emailgroup)

def assign(client, worker_id, qualification_type_id, value=1):
    # https://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.associate_qualification_with_worker
    response = client.associate_qualification_with_worker(QualificationTypeId=qualification_type_id,
                                                          WorkerId=worker_id, IntegerValue=value,
                                                          SendNotification=True)


def send_worker_message(client, worker_id, HIT_URL):

    if worker_id in get_Emailgroup():
        MESSAGE = MESSAGE_Emailgroup
    else:
        MESSAGE = MESSAGE_others

    worker_ids = [worker_id]
    message_text = MESSAGE + '\n\nYour HIT: ' + HIT_URL

    # https://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.notify_workers
    client.notify_workers(WorkerIds=worker_ids, Subject=SUBJECT, MessageText=message_text)


def main(environment):

    client = get_client(environment)

    qualification_type_id = create_qualification_typeID(client)

    # worker_id_list = get_worker_id()
    # worker_id_list = ['A2MGXHBK15GC8Y']
    # worker_id_list = ['A2MGXHBK15GC8Y', 'A3VOSKJ5LS9WB', 'A389861VXHBHWU']

    # create a HIT for A3O4TI9D8EPCL7, A1TGV7LT6LTIQU who made mistakes in compensation HIT
    worker_id_list = ['A3O4TI9D8EPCL7', 'A1TGV7LT6LTIQU']
    print(len(worker_id_list))

    logfile = open(get_log_directory('CompensationHIT') + get_timestamp() + '.txt', 'w')
    CompHITlog = open(get_log_directory('CompensationHIT') + '/records2.txt', 'w')
    response = create_hit(qualification_type_id, environment, len(worker_id_list))

    HIT_URL = get_URL_parameters(environment) + response['HIT']['HITGroupId']
    HIT_ID = response['HIT']['HITId']
    print(HIT_URL + "\n")
    print("HITID = " + HIT_ID)
    logfile.write(HIT_URL + "\n")
    logfile.write("HITID = " + HIT_ID)
    CompHITlog.write(HIT_ID)

    for worker_id in worker_id_list:
        assign(client, worker_id, qualification_type_id)
        send_worker_message(client, worker_id, HIT_URL)

if __name__ == '__main__':
    argument_length = len(sys.argv)
    if argument_length < 2:
        print("Enter the environment type in the argument ('sandbox' or 'production')\n"
              "example: python script.py sandbox")
        sys.exit(0)

    environment = sys.argv[1]
    main(environment)