import sys
import xml.etree.ElementTree as ET
from create_compensation_hit import get_client
from helper_functions import get_timestamp, get_log_directory

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

def check_submissions(client, hit_id):

    hit = client.get_hit(HITId=hit_id)
    print 'HIT {} status: {}'.format(hit_id, hit['HIT']['HITStatus'])

    HITReviewStatus = hit['HIT']['HITReviewStatus']
    NumberOfAssignmentsPending = hit['HIT']['NumberOfAssignmentsPending']
    NumberOfAssignmentsAvailable = hit['HIT']['NumberOfAssignmentsAvailable']
    NumberOfAssignmentsCompleted = hit['HIT']['NumberOfAssignmentsCompleted']
    print(HITReviewStatus, NumberOfAssignmentsPending, NumberOfAssignmentsAvailable, NumberOfAssignmentsCompleted)

    response = client.list_assignments_for_hit(
        HITId=hit_id,
        AssignmentStatuses=['Submitted'],
    )
    assignments = response['Assignments']
    print 'The number of submitted assignments is {}'.format(len(assignments))

    for assignment in assignments:
        WorkerId = assignment['WorkerId']
        assignmentId = assignment['AssignmentId']
        assignmentStatus = assignment['AssignmentStatus']
        answer = assignment['Answer']
        answer_tree = ET.fromstring(answer)
        print(WorkerId, assignmentId, assignmentStatus)

if __name__ == '__main__':
    environment = sys.argv[1]
    client = get_client(environment)

    file_name = sys.argv[2]
    hit_id_list = read_HITs_log(file_name)

    for hit_id in hit_id_list:
        check_submissions(client, hit_id)
        print