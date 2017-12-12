
"""
Creates a document for new HIT created in mturk
"""

from pymongo import MongoClient, ASCENDING, DESCENDING
from random import randint, shuffle

COLLECTION_NAME = "crowdflowerAnnotations"
ACTIVE_TWEET_COLLECTION = "activeTweet"

# Will be replaced by query strategy

TWEET_NUMBER_FILE = "active_tweet_numbers"


def insert_document(collection_name, final_collection, hit_id, start, tweet_count):
    """
    Collects the tweets from text collection and inserts them to the collection used by the meteor application.
    :param collection_name:  collection with Crowdflower data
    :param final_collection: Collection use by meteor
    :param hit_id: HIT ID
    :param start: Starting number of the document
    :param tweet_count: Number of tweets in HIT
    :return: None
    """
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    collection = db[collection_name]
    final = db[final_collection]
    tweet_list = []

    i = 0
    for document in collection.find().skip(start).limit(tweet_count*5):
        if i % 5 == 0:
            tweet_list.append({
                'id': document['messageID'],
                'text': document['messageText'],
                'message_1': document['message-1'],
                'message_2': document['message-2'],
                'message_3': document['message-3'],
                'message1': document['message1'],
                'message2': document['message2'],
                'message3': document['message3'],
                'time_text': document['time_text'],
                'time_message_1': document['time_message-1'],
                'time_message_2': document['time_message-2'],
                'time_message_3': document['time_message-3'],
                'time_message1': document['time_message1'],
                'time_message2': document['time_message2'],
                'time_message3': document['time_message3'],
                })
        i += 1
    count = i
    random_number_list = list()

    if len(tweet_list) < 2:
        return count
    else:
        for i in range(2):
            random_number = randint(0, tweet_count-1)
            while random_number in random_number_list:
                random_number = randint(0, tweet_count-1)
            random_number_list.append(random_number)
            tweet_list.append(tweet_list[random_number])

    shuffle(tweet_list)
    final.insert_one({
        'hitID': hit_id,
        'tweets': tweet_list
    })

    return count

def create_crowdflower_document(hit_id, start_position, tweet_count):
    """
    Creates a new document with HIT id as key.
    :param hit_id: mturk HIT ID
    :param start_position: docuent start index
    :param tweet_count: Number of tweets in a HIT
    :return: None
    """
    return insert_document(COLLECTION_NAME, ACTIVE_TWEET_COLLECTION, hit_id, start_position, tweet_count)
