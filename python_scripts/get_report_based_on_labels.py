

from pymongo import MongoClient
from insert_data_into_mongodb import get_data_path

HIT_COLLECTION_NAME = 'hit'
WORKER_COLLECTION_NAME = 'worker'
LABEL_COLLECTION_NAME = 'label'

COMPLETED_HIT_COLLECTION = "completedHIT"
AMOUNT = 0.07


def get_hit_list():
    line_number = 0
    hit_id_list = list()
    with open(get_data_path() + '/HITs.txt') as input_file:
        for line in input_file:
            line_number += 1
            validation = line.strip().split(":")[0]
            if line_number%2 == 1 and validation == "Your HIT ID is":
                hit_id = line.strip().split(":")[1]
                hit_id_list.append(hit_id.strip())

    return hit_id_list


def get_worker_id_who_sent_email():
    file_path = get_data_path() + "/email_received_worker_id"
    worker_id_set = set()
    with open(file_path) as input_file:
        for line in input_file:
            worker_id_set.add(line.strip())

    return worker_id_set


def print_results_to_file(report, result):
    with open(get_data_path() + "/hit_report2.csv", 'w') as output_file:
        output_file.write("S.No, WorkerID, Total labels, Basic cost, Attempting bonus, Email bonus, CompHIT pay, Total cost\n")
        count = 1
        for info in report:
            output_file.write(str(count) + ", " + ", ".join(str(x) for x in info) + "\n")
            count += 1
        output_file.write(result)


def get_report(label_collection_name, worker_collection_name):
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    label_collection = db[label_collection_name]
    worker_collection = db[worker_collection_name]

    hit_id_list = get_hit_list()

    email_received_worker_id_set = get_worker_id_who_sent_email()

    worker_id_set = set()
    for document in worker_collection.find():
        worker_id_set.add(document['workerID'])

    worker_id_set.remove("")
    label_document = list()
    for document in label_collection.find():
        label_document.append(document)

    total_amount = 0
    report = list()
    production_hit_set = set()
    hit_set = set()
    total_attempt_bonus = 0
    total_email_bonus = 0
    total_labels = 0
    cost_without_bonus = 0
    total_compHIT_pay = 0
    for worker_id in worker_id_set:
        count = 0
        bonus = 0
        bonus_email = 0
        for document in label_document:
            hit_id = document['hitID']
            if document['workerID'] == worker_id and hit_id in hit_id_list:
                count += 1
                production_hit_set.add(hit_id)
            hit_set.add(hit_id)
        if worker_id in email_received_worker_id_set:
            bonus = 0.20
            bonus_email = 0.30
        else:
            bonus = 0.20

        total_attempt_bonus += bonus
        total_email_bonus += bonus_email

        label_amount = round(count * AMOUNT, 2)
        total_labels += count
        cost_without_bonus += label_amount

        compHIT_pay = 0.01 # minimum per policy
        total_compHIT_pay += compHIT_pay

        amount = round(label_amount + bonus + bonus_email - compHIT_pay, 2)
        report.append((worker_id, count, label_amount, bonus, bonus_email, compHIT_pay, amount))
        total_amount += amount

    sandbox_hit_set = hit_set - set(hit_id_list)

    report = sorted(report, key=lambda x: x[6])
    print("Workers report based on labels:\n")
    for info in report:
        print info

    print("Total amount for the labeling task: {}".format(total_amount))
    result = " , , {}, {}, {}, {}, {}, {}".format(total_labels, cost_without_bonus, total_attempt_bonus,
                                              total_email_bonus, total_compHIT_pay, total_amount)
    print_results_to_file(report, result)

if __name__ == '__main__':
    get_report(LABEL_COLLECTION_NAME, WORKER_COLLECTION_NAME)