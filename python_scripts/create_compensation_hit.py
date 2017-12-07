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

TITLE = "Work tweets extension"
DESCRIPTION = 'Only workers affected by our system could work on this task.'
KEYWORDS = "Twitter, job and employment, employment status, annotation"
URL = "https://homanlab.org"
FRAME_HEIGHT = 700 # the height of the iframe holding the external hit
AMOUNT = 0.01


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
    requirement = [{
        'QualificationTypeId': '37RZXPVRUCAHK9IR9K2HHRIN6ZO1L2',
        'Comparator': 'EqualTo',
        'IntegerValues': [1],
        'RequiredToPreview': True
    }]

    return requirement


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

    requirement = get_requirement()
    question = get_xml_file()
    response = client.create_hit(
        Title = TITLE,
        Keywords = KEYWORDS,
        Description = DESCRIPTION,
        Reward = str(AMOUNT),
        MaxAssignments = 10,
        QualificationRequirements = requirement,
        LifetimeInSeconds = 259200,
        AssignmentDurationInSeconds = 600,
        AutoApprovalDelayInSeconds = 2592000,
        Question = question,
    )

    print "A new HIT has been created. You can preview it here:"
    print "https://workersandbox.mturk.com/mturk/preview?groupId=" + response['HIT']['HITGroupId']
    print "HITID = " + response['HIT']['HITId'] + " (Use to Get Results)"


if __name__ == '__main__':
    create_hit()