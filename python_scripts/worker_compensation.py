import sys
from create_compensation_hit import get_client
from check_hitinfo_payment import get_workerid_assignmentid
from insert_data_into_mongodb import get_data_path
from store_worker_feedback import store_feedback_in_db
from helper_functions import get_timestamp, get_log_directory

MESSAGE = "Please receive our payment for your contributions in our \"Identify Work-Related Details Of Tweets\" tasks. We apologize again for the inconvenience and thank you!\n\nRegards,\nChristopher M. Homan"


def pay_worker_bonus(client, worker_id, total_money, logfile):

    workerid_assignmentid_dict = get_workerid_assignmentid(client)

    assignment_id = workerid_assignmentid_dict[worker_id]['assignmentID']
    feedback = workerid_assignmentid_dict[worker_id]['feedback']

    # https://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.send_bonus
    client.send_bonus(WorkerId=worker_id, AssignmentId=assignment_id, BonusAmount=total_money, Reason=MESSAGE)

    store_feedback_in_db(worker_id, assignment_id, feedback, total_money, get_timestamp())
    logfile.write('Paid worker %s for AssignmentId %s: $%s at %s\n' % (worker_id, assignment_id, total_money, get_timestamp()))

def check_money_right(worker_id, total_money):

    with open(get_data_path() + "/hit_report2.csv") as input_file:
        header = next(input_file)
        for line in input_file:
            info = line.strip().split(", ")
            workerid = info[1]
            money = info[7]

            if (worker_id == workerid) and (total_money == money):
                print('Paid worker %s: $%s\n' % (worker_id, total_money))
                return True

        print('Your input does not match our calculation.\nPlease re-enter!!')
        sys.exit(1)

if __name__ == '__main__':
    environment = sys.argv[1]
    worker_id = sys.argv[2]
    total_money = sys.argv[3]

    client = get_client(environment)

    if check_money_right(worker_id, total_money):
        with open(get_log_directory('CompHIT_payment') + '/records.txt', 'a') as logfile:
            pay_worker_bonus(client, worker_id, total_money, logfile)