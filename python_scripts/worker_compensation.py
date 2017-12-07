import sys
import boto
from create_hit import get_client

UNIT_PRICE = 0.07

MESSAGE = 'text'

def pay_worker_bonus(client, worker_id, assignment_id, labels_count):

    AMOUNT = UNIT_PRICE * labels_count

    # http://boto.cloudhackers.com/en/latest/ref/mturk.html#boto.mturk.connection.MTurkConnection.grant_bonus
    client.grant_bonus(worker_id=worker_id, assignment_id=assignment_id, bonus_price=boto.mturk.price.Price(amount=AMOUNT), reason=MESSAGE)


if __name__ == '__main__':
    client = get_client()
    # worker_id = sys.argv[1]
    worker_id = 'A3VOSKJ5LS9WB'
    assignment_id = '3483FV8BEEIGQ6824AJC90LCHZX62M'
    pay_worker_bonus(client, worker_id, assignment_id, 1)