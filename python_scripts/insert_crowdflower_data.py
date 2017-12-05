import csv
from random import random
from pymongo import MongoClient
from insert_data_into_mongodb import get_data_path

FILE_NAME = "f1011589.csv"

q3_options = ['getting_hiredjob_seeking',
            'getting_fired',
            'quitting_a_job',
            'losing_job_some_other_way',
            'getting_promotedraised',
            'getting_cut_in_hours',
            'complaining_about_work',
            'offering_support',
            'going_to_work',
            'coming_home_from_work',
            'none_of_the_above_but_jobrelated',
            'not_jobrelated']


def get_data_from_file(file_path):
    infile = open(file_path)
    reader = csv.reader(infile)
    data = list(reader)

    header = data[0]
    tuple_list = []
    for item in data[1:]:
        if len(item) != len(header):
            print(item)
        else:
            message_id = item[header.index('message_id_0')]
            message_text = item[header.index('message-0')]
            unit_id = item[header.index('_unit_id')]
            message_1_before = item[header.index('message-1')]
            message_2_before = item[header.index('message-2')]
            message_3_before = item[header.index('message-3')]
            message_time = item[header.index('time-0')]
            message_1_before_time = item[header.index('relative_time_diff-1')]
            message_2_before_time = item[header.index('relative_time_diff-2')]
            message_3_before_time = item[header.index('relative_time_diff-3')]

            message_1_after = item[header.index('message1')]
            message_2_after = item[header.index('message2')]
            message_3_after = item[header.index('message3')]

            message_1_after_time = item[header.index('relative_time_diff1')]
            message_2_after_time = item[header.index('relative_time_diff2')]
            message_3_after_time = item[header.index('relative_time_diff3')]

            _id = item[header.index('_id')]

            q1_pov = item[header.index(
                'which_of_the_following_items_could_best_describe_the_point_of_view_of_jobemployment_topics_in_the_target_tweet')]
            q2_status = item[header.index(
                'which_of_the_following_items_could_best_describe_the_employment_status_of_the_subject_in_the_tweet')]
            q3_idea = item[
                header.index('what_are_the_main_ideas_of_this_tweet_as_it_relates_to_jobswork_choose_all_that_apply')]
            tuple_list.append((unit_id, message_id,  message_text, _id, message_1_before, message_2_before,
                               message_3_before, message_1_after, message_2_after, message_3_after,
                               q1_pov, q2_status, q3_idea, message_time, message_1_before_time, message_2_before_time,
                               message_3_before_time, message_1_after_time, message_2_after_time, message_3_after_time))

    return tuple_list


def insert_data(collection_name):
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor

    file_path = get_data_path() + "/" + FILE_NAME
    data = get_data_from_file(file_path)

    new_collection = db[collection_name]

    for record in data:
        q3 = (record[6]).strip().split("\n")
        q3_labels = dict()
        for i in range(len(q3_options)):
            if q3_options[i] in q3:
                q3_labels[q3_options[i]] = 1
            else:
                q3_labels[q3_options[i]] = -1

        document = {
            'unitID': record[0],
            'messageID': record[1],
            'messageText': record[2],
            'ID': record[3],
            'message-1': record[4],
            'message-2': record[5],
            'message-3': record[6],
            'message1': record[7],
            'message2': record[8],
            'message3': record[9],
            'q1': record[10],
            'q2': record[11],
            'q3': q3_labels,
            'time_text': record[13],
            'time_message-1': record[14],
            'time_message-2': record[15],
            'time_message-3': record[16],
            'time_message1': record[17],
            'time_message2': record[18],
            'time_message3': record[19],
            'fitnessFuncValue': random()

        }

        new_collection.insert_one(document)


if __name__ == '__main__':
    insert_data("crowdflowerAnnotations")
