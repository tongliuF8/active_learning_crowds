import sys
import boto
from create_hit import get_client

AMOUNT = .00


def message_worker(client, worker_id):
    # http://boto.cloudhackers.com/en/latest/ref/mturk.html#boto.mturk.connection.MTurkConnection.grant_bonus
    client.grant_bonus(worker_id=worker_id, assignment_id="", bonus_price=boto.mturk.price.Price(amount=AMOUNT))


if __name__ == '__main__':
    client = get_client()
    worker_id = int(sys.argv[1])
    message_worker(client, worker_id)