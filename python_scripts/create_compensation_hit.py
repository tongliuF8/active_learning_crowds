"""
Create a Human Intelligence Task in Mechanical Turk
"""
import boto3
from AMT_parameters import get_boto3_parameters

REGION_NAME = 'us-east-1'
AWS_KEY_FILE = "./AWS_key/credentials"
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''


with open(AWS_KEY_FILE, "r") as credential_file:
    credentials = credential_file.read()
    AWS_ACCESS_KEY_ID = credentials.split('\n')[0]
    AWS_SECRET_ACCESS_KEY = credentials.split('\n')[1]



TITLE = "Work tweets extension"
DESCRIPTION = 'Only workers affected by our system could work on this task.'
KEYWORDS = "Twitter, job and employment, employment status, annotation"
URL = "https://homanlab.org"
FRAME_HEIGHT = 700 # the height of the iframe holding the external hit
AMOUNT = 0.01


XML_FILE_PATH = "./xml_files/mturk.xml"


def get_client(environment):
    """
    Function to get the mturk client
    :return: mturk client
    """
    client = boto3.client('mturk',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                         region_name=REGION_NAME,
                         endpoint_url=get_boto3_parameters(environment)
                         )
    return client

def get_requirement(qualification_type_id):
    """
    Function to set the requirements. This is optional.
    :return: list
    """
    requirement = [{
        'QualificationTypeId': qualification_type_id,
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


def create_hit(qualification_type_id, environment):
    """
    Function to create a Human Intelligence Task in mTurk
    :return: None
    """
    client = get_client(environment)

    requirement = get_requirement(qualification_type_id)
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

    return response


if __name__ == '__main__':
    create_hit()