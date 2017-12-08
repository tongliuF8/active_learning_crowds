
"""
create_compensation_hit.py
create_qualification.py
assign_worker_qualification.py
"""

from create_compensation_hit import create_hit, get_client
from create_qualification import create_qualification_typeID
from insert_data_into_mongodb import get_data_path

SUBJECT = "Test"
MESSAGE = "Please visit this URL: \n"

def get_worker_id():
    worker_id_list = list()
    with open(get_data_path() + "/hit_report.csv") as input_file:
        header = next(input_file)
        for line in input_file:
            info = line.strip().split(", ")
            worker_id_list.append(info[1])
    return worker_id_list[: len(worker_id_list)-1]


def assign(client, worker_id, qualification_type_id, value=1):
    # https://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.associate_qualification_with_worker
    response = client.associate_qualification_with_worker(QualificationTypeId=qualification_type_id,
                                                          WorkerId=worker_id, IntegerValue=value,
                                                          SendNotification=False)


def send_worker_message(client, worker_id, HIT_URL):

    worker_ids = [worker_id]
    message_text = MESSAGE + HIT_URL

    # http://boto.cloudhackers.com/en/latest/ref/mturk.html#boto.mturk.connection.MTurkConnection.notify_workers
    client.notify_workers(worker_ids, SUBJECT, message_text)


def main():

    client = get_client()

    qualification_type_id = create_qualification_typeID(client)

    logfile = open(get_data_path() + '/CompensationHIT.txt', 'w')
    response = create_hit(qualification_type_id)
    HIT_URL = "https://workersandbox.mturk.com/mturk/preview?groupId=" + response['HIT']['HITGroupId']
    HIT_ID = response['HIT']['HITId']
    print(HIT_URL + "\n")
    print("HITID = " + HIT_ID)
    logfile.write(HIT_URL + "\n")
    logfile.write("HITID = " + HIT_ID)

    # worker_id_list = get_worker_id()
    worker_id_list = ['A3VOSKJ5LS9WB', 'A2MGXHBK15GC8Y']

    for worker_id in worker_id_list:
        assign(client, worker_id, qualification_type_id)
        send_worker_message(client, worker_id, HIT_URL)

if __name__ == '__main__':
    main()