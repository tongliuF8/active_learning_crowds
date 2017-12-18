import sys

from helper_functions import get_timestamp, get_log_directory
from create_compensation_hit import get_client


FILE_NAME = "records"


def get_hit_info(client, hit_id_list):
    hit_info_list = list()
    for hit_id in hit_id_list:
        response = client.list_assignments_for_hit(
            HITId=hit_id,
            AssignmentStatuses=['Submitted'],
            MaxResults=10
        )

        assignments = response['Assignments']
        hit_info_list.append((hit_id, len(assignments)))

    for hit in hit_info_list:
        print("Number of assignments completed in HIT {}: {}".format(hit[0], hit[1]))


def get_hit_list(file_name):
    hit_id_list = list()
    with open(get_log_directory('HITs') + "/" + file_name) as input_file:
        line_number = 0
        for line in input_file:
            line_number += 1
            validation = line.strip().split(":")[0]
            if line_number % 2 == 1 and validation == "Your HIT ID is":
                hit_id = line.strip().split(":")[1]
                hit_id_list.append(hit_id.strip())

    return hit_id_list


def main():
    file_name = sys.argv[1]
    hit_id_list = get_hit_list(file_name)
    client = get_client('production')
    get_hit_info(client, hit_id_list)

if __name__ == '__main__':
    main()
