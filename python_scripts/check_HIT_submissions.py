import sys
from create_compensation_hit import get_client
from helper_functions import get_timestamp, get_log_directory

MAX_ASSIGNMENTS = 5

def read_HITs_log(file_name):

    hit_id_list = list()
    with open(get_log_directory('HITs') + "/" + file_name) as input_file:
        line_number = 0
        for line in input_file:
            line_number += 1
            validation = line.strip().split(":")[0]
            if line_number % 2 == 1 and validation == "Your HIT ID is":
                hit_id = line.strip().split(":")[1]
                hit_id_list.append(hit_id.strip())
    print(len(hit_id_list))

    return hit_id_list

def check_submissions_MTurk(client, hit_id):

    hit = client.get_hit(HITId=hit_id)
    print 'HIT {} status: {}'.format(hit_id, hit['HIT']['HITStatus'])

    HITReviewStatus = hit['HIT']['HITReviewStatus']
    NumberOfAssignmentsPending = hit['HIT']['NumberOfAssignmentsPending']
    NumberOfAssignmentsAvailable = hit['HIT']['NumberOfAssignmentsAvailable']
    NumberOfAssignmentsCompleted = hit['HIT']['NumberOfAssignmentsCompleted']

    response = client.list_assignments_for_hit(
        HITId=hit_id,
    )
    assignments = response['Assignments']

    if len(assignments) != MAX_ASSIGNMENTS:
        for assignment in assignments:
            WorkerId = assignment['WorkerId']
            assignmentId = assignment['AssignmentId']
            assignmentStatus = assignment['AssignmentStatus']
            print(hit_id, HITReviewStatus, NumberOfAssignmentsPending, NumberOfAssignmentsAvailable, NumberOfAssignmentsCompleted)
            print(WorkerId, assignmentId, assignmentStatus)
    else:
        print 'The assignments are fully Submitted: {}'.format(len(assignments))

if __name__ == '__main__':
    client = get_client('production')

    file_name = sys.argv[1]
    hit_id_list = read_HITs_log(file_name)

    for hit_id in hit_id_list:
        check_submissions_MTurk(client, hit_id)
        print