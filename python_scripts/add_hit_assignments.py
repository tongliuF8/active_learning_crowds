import sys

from create_hit import get_client

def create_additional_assignments(client, hit_id, additional_assignment_perHIT):
    # http://boto.cloudhackers.com/en/latest/ref/mturk.html#boto.mturk.connection.MTurkConnection.extend_hit
    client.extend_hit(
        hit_id=hit_id,
        assignments_increment=additional_assignment_perHIT
    )

if __name__ == '__main__':
    environment = sys.argv[1]
    hit_id = sys.argv[2]
    additional_assignment_perHIT = 1
    client = get_client(environment)
    create_additional_assignments(client, hit_id, additional_assignment_perHIT)