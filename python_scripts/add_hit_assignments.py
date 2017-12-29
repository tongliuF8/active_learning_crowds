import sys
from datetime import datetime
# # boto2
# from create_hit import get_client
# boto3
from create_compensation_hit import get_client

def check_hit_status(client, hit_id):

    hit = client.get_hit(HITId=hit_id)
    # hit.keys() = [u'HIT', 'ResponseMetadata']

    # hit['HIT'].keys() = [u'HITGroupId', u'RequesterAnnotation', u'NumberOfAssignmentsCompleted', u'Description', u'MaxAssignments', u'Title', u'NumberOfAssignmentsAvailable', u'Question', u'CreationTime', u'AssignmentDurationInSeconds', u'HITTypeId', u'NumberOfAssignmentsPending', u'HITStatus', u'HITId', u'QualificationRequirements', u'Keywords', u'Expiration', u'Reward', u'HITReviewStatus', u'AutoApprovalDelayInSeconds']

    # hit['ResponseMetadata'].keys() = ['RetryAttempts', 'HTTPStatusCode', 'RequestId', 'HTTPHeaders']

    HITStatus = hit['HIT']['HITStatus']
    HITCreationTime = hit['HIT']['CreationTime'].strftime("%Y-%m-%d %H:%M:%S")
    HITExpiration = hit['HIT']['Expiration'].strftime("%Y-%m-%d %H:%M:%S")
    HITReviewStatus = hit['HIT']['HITReviewStatus']
    NumberOfAssignmentsPending = hit['HIT']['NumberOfAssignmentsPending']
    NumberOfAssignmentsAvailable = hit['HIT']['NumberOfAssignmentsAvailable']
    NumberOfAssignmentsCompleted = hit['HIT']['NumberOfAssignmentsCompleted']

    print(HITStatus, HITCreationTime, HITExpiration, HITReviewStatus, NumberOfAssignmentsPending, NumberOfAssignmentsAvailable, NumberOfAssignmentsCompleted)
    print

def update_date(client, hit_id):

    date_time_string = "2018-01-05 12:00:00"
    datetime_object = datetime.strptime(date_time_string, "%Y-%m-%d %H:%M:%S")
    print(datetime_object, type(datetime_object))

    # https://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.update_expiration_for_hit
    client.update_expiration_for_hit(
        HITId=hit_id,
        ExpireAt=datetime_object
    )

def create_additional_assignments_boto2(client, hit_id, additional_assignment_perHIT):
    # http://boto.cloudhackers.com/en/latest/ref/mturk.html#boto.mturk.connection.MTurkConnection.extend_hit
    status = client.extend_hit(
        hit_id=hit_id,
        assignments_increment=additional_assignment_perHIT
    )
    print(status)

def create_additional_assignments(client, hit_id, additional_assignment_perHIT):
    # https://boto3.readthedocs.io/en/latest/reference/services/mturk.html#MTurk.Client.create_additional_assignments_for_hit
    status = client.create_additional_assignments_for_hit(
        HITId=hit_id,
        NumberOfAdditionalAssignments=additional_assignment_perHIT
    )
    if status:
        print('HIT %s is extended by %s assignment\n' % (hit_id, additional_assignment_perHIT))

if __name__ == '__main__':
    environment = sys.argv[1]
    hit_id = sys.argv[2]
    additional_assignment_perHIT = 1
    client = get_client(environment)

    print(hit_id)
    check_hit_status(client, hit_id)
    # update_date(client, hit_id)

    # create_additional_assignments_boto2(client, hit_id, additional_assignment_perHIT)
    create_additional_assignments(client, hit_id, additional_assignment_perHIT)

    check_hit_status(client, hit_id)    