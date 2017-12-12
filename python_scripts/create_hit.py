"""
Create a Human Intelligence Task in Mechanical Turk
"""
import boto3
import boto.mturk.connection
from boto.mturk.qualification import Qualifications, PercentAssignmentsApprovedRequirement, LocaleRequirement, Requirement
import datetime
from AMT_parameters import get_boto2_parameters, get_URL_parameters
import sys

from create_hit_document import create_document
from create_crowdflower_hit_document import create_crowdflower_document

from insert_data_into_mongodb import get_data_path
from helper_functions import get_timestamp, get_log_directory
from create_qualification import create_qualification_typeID_boto2

AWS_KEY_FILE = "./AWS_key/credentials"
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

with open(AWS_KEY_FILE, "r") as credential_file:
    credentials = credential_file.read()
    AWS_ACCESS_KEY_ID = credentials.split('\n')[0]
    AWS_SECRET_ACCESS_KEY = credentials.split('\n')[1]

TITLE = "Identify Work-Related Details Of Tweets"
KEYWORDS = "Twitter, job and employment, employment status, annotation"
URL = "https://homanlab.org"
FRAME_HEIGHT = 700 # the height of the iframe holding the external hit
AMOUNT = .84

TOTAL_CROWDFLOWER_TWEETS = 100
XML_FILE_PATH = "./xml_files/mturk.xml"


def get_client(environment):
    """
    Function to get the mturk client
    :return: mturk client
    """
    client = boto.mturk.connection.MTurkConnection(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        host=get_boto2_parameters(environment)
    )
    return client


def get_requirement(qualification_type_id):
    """
    Function to set the requirements. This is optional.
    :return: list
    """
    qualifications = Qualifications()
    qualifications.add(PercentAssignmentsApprovedRequirement(comparator="GreaterThan", integer_value="90"))
    qualifications.add(LocaleRequirement("EqualTo", "US"))
    qualifications.add(Requirement(qualification_type_id=qualification_type_id, comparator="EqualTo", integer_value="1"))
    return qualifications


def create_hit(client, logfile, data_type, qualification_type_id=None, start_position=None, tweet_count=None):
    """
    Function to create a Human Intelligence Task in mTurk
    :return: None
    """

    qualifications = get_requirement(qualification_type_id)
    # question = get_xml_file()
    questionform = boto.mturk.question.ExternalQuestion(URL, FRAME_HEIGHT)
    response = client.create_hit(
        title=TITLE,
        keywords=KEYWORDS,
        question=questionform,
        max_assignments=5,
        qualifications=qualifications,
        reward=boto.mturk.price.Price(amount=AMOUNT),
        lifetime=datetime.timedelta(minutes=14400),
        duration=datetime.timedelta(minutes=120),
        approval_delay= datetime.timedelta(minutes=14400),
        response_groups=('Minimal', 'HITDetail'),
        annotation='good'
    )

    hit_info = response[0]
    hit_type_id = hit_info.HITTypeId
    hit_id = hit_info.HITId
    number_of_tweets =0
    if data_type is None:
        create_document(hit_id)
    if data_type == "crowdflower":
        number_of_tweets = create_crowdflower_document(hit_id, start_position, tweet_count)

    logfile.write("Your HIT ID is: {}\n\n".format(hit_id))

    return hit_type_id, number_of_tweets


if __name__ == '__main__':
    argument_length = len(sys.argv)

    logfile = open(get_log_directory('HITs') + get_timestamp() + '.txt', 'w')

    hit_type_id = ""
    if argument_length < 4:
        print("4 arguments required ....\n"
              "example: python script.py sandbox crowdflower 5 10..")
        sys.exit(0)

    environment = sys.argv[1]
    client = get_client(environment)
    if sys.argv[2] == 'unlabeled':
        hit_type_id = create_hit(client, logfile, environment)

    if sys.argv[2] == 'crowdflower':

        qualification_type_id = create_qualification_typeID_boto2(client)
        with open(get_log_directory("HITcreation") +"/test_log", 'a+') as input_file:
            line = ""
            for line in input_file:
                pass
            last_data_index = 0
            counter_value = 0
            if line != "":
                end = line.strip().split(" ")[2]
                value = end.split(":")[1]
                last_data_index = int(value.split("-")[0]) + 1

                counter = line.strip().split(" ")[3]
                counter_value = int(counter.split(":")[1])


            total_tweet_used_in_batch = 0
            start_index = last_data_index
            number_of_hits = int(sys.argv[3])
            tweet_count = int(sys.argv[4])

            for i in range(number_of_hits):
                hit_type_id, number_of_tweets = create_hit(client, qualification_type_id, logfile,
                                                           sys.argv[2], 5* i * (last_data_index + tweet_count),
                                                           tweet_count)
                last_data_index += tweet_count
                total_tweet_used_in_batch += number_of_tweets
            end_index = last_data_index - 1

            input_file.write("timestamp:{} start:{}-0 end:{}-4 counter:{}\n".format(
                get_timestamp(), str(start_index), str(end_index),
                counter_value+total_tweet_used_in_batch))

    logfile.write(get_URL_parameters(environment) + "{}\n".format(hit_type_id))
