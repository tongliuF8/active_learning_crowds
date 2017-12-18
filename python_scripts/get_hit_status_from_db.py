import sys
from pymongo import MongoClient

from get_hit_status import get_hit_list

HIT_COLLECTION = 'hit'


def get_info(hit_id_list, hit_collection):
    for hit_id in hit_id_list:
        print("{} : {}".format(hit_id, hit_collection.find({'hitID': hit_id}).count()))


def main():
    file_name = sys.argv[1]
    hit_id_list = get_hit_list(file_name)
    mongo_client = MongoClient('localhost', 8081)
    db = mongo_client.meteor
    hit_collection = db[HIT_COLLECTION]
    get_info(hit_id_list, hit_collection)

if __name__ == '__main__':
    main()