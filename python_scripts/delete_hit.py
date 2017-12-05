
from create_hit import get_client
from insert_data_into_mongodb import get_data_path


def delete_hit(client, hit_id):
    client.disable_hit(hit_id=hit_id)


def main():
    client = get_client()
    line_number = 0
    hit_id_list = list()
    with open(get_data_path() + '/HITs.txt') as input_file:
        for line in input_file:
            line_number += 1
            if line_number%3 == 2:
                hit_id = line.strip().split(":")[1]
                hit_id_list.append(hit_id.strip())

    for hit_id in hit_id_list:
        delete_hit(client, hit_id)

if __name__ == '__main__':
    main()