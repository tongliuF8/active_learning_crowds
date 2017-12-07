import boto3
import xml.etree.ElementTree as ET

region_name = 'us-east-1'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_KEY_FILE = "./AWS_key/credentials"

with open(AWS_KEY_FILE, "r") as credential_file:
    credentials = credential_file.read()
    AWS_ACCESS_KEY_ID = credentials.split('\n')[0]
    AWS_SECRET_ACCESS_KEY = credentials.split('\n')[1]
endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

# Uncomment this line to use in production
# endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

client = boto3.client(
  'mturk',
  endpoint_url=endpoint_url,
  region_name=region_name,
  aws_access_key_id=AWS_ACCESS_KEY_ID,
  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

hit_id = "3XAOZ9UYRYQ0OJBWADSVM2WIENWQ1Y"

hit = client.get_hit(HITId=hit_id)
print 'Hit {} status: {}'.format(hit_id, hit['HIT']['HITStatus'])

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
    print 'The Worker with ID {} submitted assignment {} and gave the answer {}'.format(WorkerId,assignmentId, answer)
    tree = ET.fromstring(answer)
    print("WorkerID: {}".format(WorkerId))
    print("AssignmentID: {}".format(assignmentId))
    # # print("Code: {}".format(tree[1][1].text))
    # if assignment['AssignmentStatus'] == 'Submitted':
    #     print 'Approving Assignment {}'.format(assignmentId)
    #     client.approve_assignment(
    #         AssignmentId=assignmentId,
    #         RequesterFeedback='good',
    #         OverrideRejection=False,
    #     )