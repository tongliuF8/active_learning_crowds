import sys

from create_hit import get_client


SUBJECT = "Subject"
MESSAGE = "Test"


def message_worker(client, worker_ids):
    # http://boto.cloudhackers.com/en/latest/ref/mturk.html#boto.mturk.connection.MTurkConnection.notify_workers
    client.notify_workers(worker_ids, SUBJECT, MESSAGE)


if __name__ == '__main__':
    client = get_client()
    worker_ids = []
    worker_ids = worker_ids.append(sys.argv[1])
    message_worker(client, worker_ids)
