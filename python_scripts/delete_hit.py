import sys

from create_hit import get_client
from insert_data_into_mongodb import get_data_path


def delete_hit(client, hit_id):
    response = client.disable_hit(hit_id=hit_id)


def delete_all_hits(client):
    response = client.get_all_hits()
    hit_id_list = list()
    for hit in response:
        hit_id_list.append(hit.HITId)

    for hit_id in hit_id_list:
        delete_hit(client, hit_id)


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

if __name__ == '__main__':
    client = get_client()
    argument_length = len(sys.argv)
    if argument_length == 1:
        delete_hits_from_file(client)
    else:
        delete_all_hits(client)