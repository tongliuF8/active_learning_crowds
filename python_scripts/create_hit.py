"""
Create a Human Intelligence Task in Mechanical Turk
"""
import boto3
import boto.mturk.connection
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, LocaleRequirement
import datetime

import sys

from create_hit_document import create_document
from create_crowdflower_hit_document import create_crowdflower_document

# REGION_NAME = 'us-east-1'
AWS_KEY_FILE = "./AWS_key/credentials"
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

with open(AWS_KEY_FILE, "r") as credential_file:
    credentials = credential_file.read()
    AWS_ACCESS_KEY_ID = credentials.split('\n')[0]
    AWS_SECRET_ACCESS_KEY = credentials.split('\n')[1]
# ENDPOINT_URL = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

TITLE = "Identify Work-Related Details Of Tweets"
# DESCRIPTION = "External survey"
KEYWORDS = "Twitter, job and employment, employment status, annotation"
URL = "https://homanlab.org"
FRAME_HEIGHT = 700 # the height of the iframe holding the external hit
AMOUNT = .84

HOST = 'mechanicalturk.sandbox.amazonaws.com'
# HOST = 'mechanicalturk.amazonaws.com'


TOTAL_CROWDFLOWER_TWEETS = 2000
XML_FILE_PATH = "./xml_files/mturk.xml"


def get_client():
    """
    Function to get the mturk client
    :return: mturk client
    """
    client = boto.mturk.connection.MTurkConnection(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        host=HOST
    )
    return client


def get_requirement():
    """
    Function to set the requirements. This is optional.
    :return: list
    """
    qualifications = Qualifications()
    qualifications.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan", integer_value="90"))
    qualifications.add(LocaleRequirement("EqualTo", "US"))
    return qualifications


def get_xml_file():
    """
    Function to read and return file content
    :return: content of the file
    """
    question_file = open(XML_FILE_PATH, "r")
    return question_file.read()


def create_hit(start_position=None, tweet_count=None):
    """
    Function to create a Human Intelligence Task in mTurk
    :return: None
    """

    argument_length = len(sys.argv)
    client = get_client()
    qualifications = get_requirement()
    # question = get_xml_file()
    questionform = boto.mturk.question.ExternalQuestion(URL, FRAME_HEIGHT)
    response = client.create_hit(
        title=TITLE,
        # description=DESCRIPTION,
        keywords=KEYWORDS,
        question=questionform,
        max_assignments=5,
        qualifications=qualifications,
        reward=boto.mturk.price.Price(amount=AMOUNT),
        lifetime=datetime.timedelta(minutes=4320),
        duration=datetime.timedelta(minutes=120),
        response_groups=('Minimal', 'HITDetail'),
    )

    hit_info = response[0]
    hit_type_id = hit_info.HITTypeId
    hit_id = hit_info.HITId
    if start_position is None:
        create_document(hit_id)
    else:
        create_crowdflower_document(hit_id, start_position, tweet_count)
    # print("Your HIT has been created. You can see it at this link:")
    print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
    print("Your HIT ID is: {}".format(hit_id))
    print

if __name__ == '__main__':
    argument_length = len(sys.argv)

    if argument_length == 1:
        create_hit()
    else:
        tweet_count = int(sys.argv[1])
        for i in range((TOTAL_CROWDFLOWER_TWEETS/tweet_count)):
            create_hit(i*tweet_count, tweet_count)
