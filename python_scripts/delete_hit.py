import sys

from create_hit import get_client
from insert_data_into_mongodb import get_data_path
from helper_functions import get_timestamp, get_log_directory

from tqdm import tqdm

def delete_hit(client, hit_id):
    response = client.disable_hit(hit_id=hit_id)


def delete_all_hits(client):
    logfile = open(get_log_directory('DeletionLog') + get_timestamp() + '.txt', 'w')
    logfile.write("HITs deleted in this batch:\n")
    response = client.get_all_hits()
    hit_id_list = list()
    for hit in response:
        hit_id_list.append(hit.HITId)

    for hit_id in tqdm(hit_id_list):
        delete_hit(client, hit_id)
        logfile.write(hit_id + "\n")

"""
def delete_hits_from_file(client):
    line_number = 0
    hit_id_list = list()
    with open(get_data_path() + '/HITs.txt') as input_file:
        for line in input_file:
            line_number += 1
            validation = line.strip().split(":")[0]
            if line_number%2 == 1 and validation == "Your HIT ID is":
                hit_id = line.strip().split(":")[1]
                hit_id_list.append(hit_id.strip())

    for hit_id in hit_id_list:
        delete_hit(client, hit_id)
"""

if __name__ == '__main__':
    environment = sys.argv[1]
    client = get_client(environment)
    delete_all_hits(client)
