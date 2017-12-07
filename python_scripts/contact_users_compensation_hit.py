
"""
create_compensation_hit.py
create_qualification.py
assign_worker_qualification.py
"""

from create_compensation_hit import create_hit, get_client
from create_qualification import create_qualification_typeID
from insert_data_into_mongodb import get_data_path


def get_worker_id():
    worker_id_list = list()
    with open(get_data_path() + "/hit_report.csv") as input_file:
        header = next(input_file)
        for line in input_file:
            info = line.strip().split(", ")
            worker_id_list.append(info[1])
    return worker_id_list[: len(worker_id_list)-1]


def assign(client, worker_id, qualification_type_id, value=1):
    response = client.associate_qualification_with_worker(QualificationTypeId=qualification_type_id,
                                                          WorkerId=worker_id, IntegerValue=value,
                                                          SendNotification=False)


def union():
    client = get_client()
    qualification_type_id = create_qualification_typeID(client)
    # worker_id_list = get_worker_id()
    worker_id_list = ['A3VOSKJ5LS9WB', 'A2MGXHBK15GC8Y']
    for worker_id in worker_id_list:
        assign(client, worker_id, qualification_type_id)

    logfile = open(get_data_path() + '/CompensationHIT.txt', 'w')
    response = create_hit(qualification_type_id)
    # response = create_hit('3XPDWPNT8KOFEWRIJLNVWCHL9AW4D2')

    print("https://workersandbox.mturk.com/mturk/preview?groupId=" + response['HIT']['HITGroupId'] + "\n")
    print("HITID = " + response['HIT']['HITId'])
    logfile.write("https://workersandbox.mturk.com/mturk/preview?groupId=" + response['HIT']['HITGroupId'] + "\n")
    logfile.write("HITID = " + response['HIT']['HITId'])

if __name__ == '__main__':
    union()