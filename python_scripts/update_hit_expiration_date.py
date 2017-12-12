import sys
from datetime import datetime

from create_compensation_hit import get_client


def update_date(client, datetime_object):
    client.update_expiration_for_hit(
        HITId='3V7ICJJAZ9FUCC6QEDH86FOQ0KQ4B2',
        ExpireAt=datetime_object
    )
    print(datetime_object)

if __name__ == '__main__':
    environment = sys.argv[1]
    date_time_string = sys.argv[2]
    client = get_client(environment)
    datetime_object = datetime.strptime(date_time_string, '%Y-%m-%d-%I:%M%p')
    update_date(client, datetime_object)