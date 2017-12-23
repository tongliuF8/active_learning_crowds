import sys

from create_compensation_hit import get_client
import xml.etree.ElementTree as ET


def get_hit_information(client, hit_id):
    hit = client.get_hit(HITId=hit_id)
    print(hit['HIT'])
    print 'Hit {} status: {}'.format(hit_id, hit['HIT']['HITStatus'])
    print 'Hit {} group: {}'.format(hit_id, hit['HIT']['HITGroupId'])
    print 'Hit {} CreationTime: {}'.format(hit_id, hit['HIT']['CreationTime'])
    print 'Hit {} QualificationRequirements: {}'.format(hit_id, hit['HIT']['QualificationRequirements'])
    print 'Hit {} NumberOfAssignmentsAvailable: {}'.format(hit_id, hit['HIT']['NumberOfAssignmentsAvailable'])
    print 'Hit {} NumberOfAssignmentsPending: {}'.format(hit_id, hit['HIT']['NumberOfAssignmentsPending'])
    response = client.list_assignments_for_hit(
        HITId=hit_id,
        AssignmentStatuses=['Submitted'],
        MaxResults=10
    )

    assignments = response['Assignments']
    print 'The number of submitted assignments is {}'.format(len(assignments))

    for assignment in assignments:
        WorkerId = assignment['WorkerId']
        assignmentId = assignment['AssignmentId']
        answer = assignment['Answer']
        submit_time = assignment['SubmitTime']
        # print 'The Worker with ID {} submitted assignment {} and gave the answer {}'.format(WorkerId, assignmentId,
        #                                                                                    answer)
        tree = ET.fromstring(answer)
        print("WorkerID: {}".format(WorkerId))
        print("AssignmentID: {}".format(assignmentId))
        print("submit_time: {}".format(submit_time))
        print


def main():
    environment = sys.argv[1]
    hit_id = sys.argv[2]
    client= get_client(environment)
    get_hit_information(client, hit_id)

if __name__ == '__main__':
    main()
