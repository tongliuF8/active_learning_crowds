import sys
from datetime import datetime
from dateutil.tz import tzlocal
# # boto2
# from create_hit import get_client
# boto3
from create_compensation_hit import get_client

def update_date(client, hit_id):

    date_time_string = "2018-01-05 00:00:00"
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

    # Get HIT expiration datetime
    hit = client.get_hit(HITId=hit_id)
    HITExpiration = hit['HIT']['Expiration']

    # Get current datetime
    dateutil_tz = tzlocal()
    current_datetime = datetime.now(dateutil_tz)

    diff = HITExpiration - current_datetime
    # Guarantee 5 days for each HIT
    if diff.days < 5:
        update_date(client, hit_id)

    # create_additional_assignments_boto2(client, hit_id, additional_assignment_perHIT)
    create_additional_assignments(client, hit_id, additional_assignment_perHIT)