import sys

from create_compensation_hit import get_client

def create_additional_assignments(client, hit_id, additional_assignment_perHIT):
    client.create_additional_assignments_for_hit(
        HITId=hit_id,
        NumberOfAdditionalAssignments=additional_assignment_perHIT
    )

if __name__ == '__main__':
    environment = sys.argv[1]
    hit_id = sys.argv[2]
    additional_assignment_perHIT = 1
    client = get_client(environment)
    create_additional_assignments(client, hit_id, additional_assignment_perHIT)