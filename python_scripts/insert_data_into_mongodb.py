"""
Creates collections and inserts the document from the given JSON file
"""

from random import random
from pymongo import MongoClient, ASCENDING
import json
import os


TEXT_FILE_NAME = "new1year.json"
ID_FILE_NAME = "combinedAnnotation.json"
TEMP_ID_COLLECTION = "tempIDCollection"
TEMP_TEXT_COLLECTION = "tempTextCollection"


def get_data_path():
    """
    Function to get the data file path
    :return: path
    """
    current_directory_path = os.getcwd()
    path_array = current_directory_path.strip().split("/")
    path_array[len(path_array)-1] = 'data'
    return "/".join(path_array)


def insert_data(collection_name, id_collection):
    """
    Load the document from JSON file into the respective collections and creates indexes.
    :param collection_name: collection with tweet text
    :param id_collection: collection with twitter ID
    :return: None
    """
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    twitter_id_collection = db[id_collection]
    temp_collection = db[TEMP_ID_COLLECTION]
    id_file_path = get_data_path() + "/" + ID_FILE_NAME
    with open(id_file_path) as input_file:
        for line in input_file:
            document = json.loads(line)
            if document['topic_human'] == 'job' or document['topic_machine'] == 'job':
                twitter_id_collection.insert_one(document)
                temp_collection.insert_one(document)

    twitter_text_collection = db[collection_name]
    temp_collection = db[TEMP_TEXT_COLLECTION]
    data_file_path = get_data_path() + "/" + TEXT_FILE_NAME
    with open(data_file_path) as input_file:
        for line in input_file:
            document = json.loads(line)
            document['fitnessFuncValue'] = random()
            twitter_text_collection.insert_one(document)
            temp_collection.insert_one(document)

    twitter_id_collection.create_index([('tweet_id', ASCENDING)], unique=True)
    twitter_text_collection.create_index([('id', ASCENDING)], unique=True)


def extract_job_realted_tweets(text_collection, id_collection, final_collection):
    """
    Creates a new collection with job-related tweets.
    :param text_collection: collection with twitter text
    :param id_collection: collection with twiiter ID and job label
    :param final_collection: Collection used to store job related tweets
    :return: None
    """
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor

    tweet_id_temp_collection = db[id_collection]
    text_temp_collection = db[text_collection]
    final_coll = db[final_collection]
    tweet_id = []

    for tweet in tweet_id_temp_collection.find():
        tweet_id.append(tweet['tweet_id'])

    # print(tweet_id)

    count = 0
    missing_tweet = []
    for idx in tweet_id:
        data = text_temp_collection.find_one({"id": idx})
        try:
            text = data['text']
            final_coll.insert_one({
                'id': idx,
                'text': text,
                'fitnessFuncValue': random()
            })
        except TypeError:
            missing_tweet.append(idx)
            count += 1

    print(missing_tweet)
    print("Total missing tweets: {}".format(count))
    db.drop_collection(tweet_id_temp_collection)
    db.drop_collection(text_temp_collection)

if __name__ == '__main__':
    insert_data('newOneYear', 'combinedAnnotation')
    extract_job_realted_tweets(TEMP_TEXT_COLLECTION, TEMP_ID_COLLECTION, 'oneYearData')
