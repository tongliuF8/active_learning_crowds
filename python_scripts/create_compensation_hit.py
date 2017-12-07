"""
Create a Human Intelligence Task in Mechanical Turk
"""
import boto3

REGION_NAME = 'us-east-1'
AWS_KEY_FILE = "./AWS_key/credentials"
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

with open(AWS_KEY_FILE, "r") as credential_file:
    credentials = credential_file.read()
    AWS_ACCESS_KEY_ID = credentials.split('\n')[0]
    AWS_SECRET_ACCESS_KEY = credentials.split('\n')[1]
ENDPOINT_URL = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

TITLE = "ActiveLearning"
DESCRIPTION = "External survey"
KEYWORDS = "Testing"
AMOUNT = .00

SANDBOX_HOST = 'mechanicalturk.sandbox.amazonaws.com'
# real_host = 'mechanicalturk.amazonaws.com'


XML_FILE_PATH = "./xml_files/mturk.xml"


def get_client():
    """
    Function to get the mturk client
    :return: mturk client
    """
    client = boto3.client('mturk',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=REGION_NAME,
                         endpoint_url=ENDPOINT_URL
                         )
    return client


def get_requirement():
    """
    Function to set the requirements. This is optional.
    :return: list
    """
    local_requirements = [{
        'QualificationTypeId': '00000000000000000071',
        'Comparator': 'In',
        'LocaleValues': [{
            'Country': 'US'
        }, {
            'Country': 'CA'
        }],
        'RequiredToPreview': True
    }]
    return local_requirements


def get_xml_file():
    """
    Function to read and return file content
    :return: content of the file
    """
    question_file = open(XML_FILE_PATH, "r")
    return question_file.read()


def create_hit():
    """
    Function to create a Human Intelligence Task in mTurk
    :return: None
    """
    client = get_client()
    # requirements = get_requirement()
    question = get_xml_file()
    response = client.create_hit(
        Title=TITLE,
        Keywords= KEYWORDS,
        Description= DESCRIPTION,
        Reward='0.00',
        MaxAssignments=10,
        LifetimeInSeconds=100,
        AssignmentDurationInSeconds=100,
        AutoApprovalDelayInSeconds=10000,
        Question=question,
    )

    print "A new HIT has been created. You can preview it here:"
    print "https://workersandbox.mturk.com/mturk/preview?groupId=" + response['HIT']['HITGroupId']
    print "HITID = " + response['HIT']['HITId'] + " (Use to Get Results)"


if __name__ == '__main__':
    create_hit()