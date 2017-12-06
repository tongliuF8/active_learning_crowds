from pymongo import MongoClient

COLLECTION_NAME = "activeTweet"


def validate(collection_name):
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    collection = db[collection_name]

    count = 0
    tweet_id_set = set()
    for document in collection.find():
        tweets = document['tweets']
        id_list = set()
        for doc in tweets:
            _id = doc['id']
            tweet_id_set.add(_id)
            id_list.add(_id)
        if len(id_list) != 10:
            count += 1

    print("Total number of HITs with invalid tweets: {}".format(count))
    print("Total unique tweets: {}".format(len(tweet_id_set)))

if __name__ == '__main__':
    validate(COLLECTION_NAME)