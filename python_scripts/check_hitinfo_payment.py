import xml.etree.ElementTree as ET
from create_compensation_hit import get_client
from helper_functions import get_timestamp, get_log_directory

with open(get_log_directory('CompensationHIT') + '/records2.txt', 'r') as f:
    hit_id = f.readline().strip()

def get_workerid_assignmentid(client):

    hit = client.get_hit(HITId=hit_id)
    # print 'HIT {} status: {}'.format(hit_id, hit['HIT']['HITStatus'])

    response = client.list_assignments_for_hit(
        HITId=hit_id,
        AssignmentStatuses=['Submitted'],
    )

    assignments = response['Assignments']
    # print 'The number of submitted assignments is {}'.format(len(assignments))

    workerid_assignmentid_dict = {}

    for assignment in assignments:
        WorkerId = assignment['WorkerId']
        assignmentId = assignment['AssignmentId']
        answer = assignment['Answer']
        # print 'The Worker with ID {} submitted assignment {} and gave the answer {}'.format(WorkerId,assignmentId, answer)
        tree = ET.fromstring(answer)
        feedback = tree[1][1].text
        # print("WorkerID: {}".format(WorkerId))
        # print("AssignmentID: {}".format(assignmentId))
        document = {
            'assignmentID': assignmentId,
            'feedback': feedback
        }
        workerid_assignmentid_dict[WorkerId] = document
        # # print("Code: {}".format(tree[1][1].text))
        # if assignment['AssignmentStatus'] == 'Submitted':
        #     print 'Approving Assignment {}'.format(assignmentId)
        #     client.approve_assignment(
        #         AssignmentId=assignmentId,
        #         RequesterFeedback='good',
        #         OverrideRejection=False,
        #     )

    # print('The number of workers is {}'.format(len(workerid_assignmentid_dict)))

    # print(len(workerid_assignmentid_dict) == len(assignments))

    return workerid_assignmentid_dict