from create_compensation_hit import get_client
from insert_data_into_mongodb import get_data_path
from helper_functions import get_timestamp, get_log_directory

def create_qualification_typeID(client):

    logfile = open(get_log_directory('Qualification') + get_timestamp() + '.txt', 'w')
    response = client.create_qualification_type(
        Name = get_timestamp(),
        Description = "Only workers affected by our system could work on this task.",
        QualificationTypeStatus = "Active",
        AutoGranted = True,
        AutoGrantedValue = 1)

    logfile.write("Your Qualification is created. Your Qualification Type ID is:\n")
    logfile.write(response['QualificationType']['QualificationTypeId'])

    # assign(client, 'A2MGXHBK15GC8Y', response['QualificationType']['QualificationTypeId'])
    # assign(client, 'A3VOSKJ5LS9WB', response['QualificationType']['QualificationTypeId'])
    # assign(client, 'A2BA16GUOB0DT5', response['QualificationType']['QualificationTypeId'])
    # assign(client, 'A3D1A336ZEGP79', response['QualificationType']['QualificationTypeId'])

    return response['QualificationType']['QualificationTypeId']


def create_qualification_typeID_boto2(client):

    logfile = open(get_log_directory('Qualification_boto2') + get_timestamp() + '.txt', 'w')
    response = client.create_qualification_type(
        name = get_timestamp(),
        description = "Only workers affected by our system could work on this task.",
        status = "Active",
        auto_granted = True,
        auto_granted_value = 1)

    logfile.write("Your Qualification is created. Your Qualification Type ID is:\n")
    logfile.write(response[0].QualificationTypeId)

    # client.assign_qualification(response[0].QualificationTypeId, 'A2MGXHBK15GC8Y', value=1, send_notification=True)
    # client.assign_qualification(response[0].QualificationTypeId, 'A2BA16GUOB0DT5', value=1, send_notification=True)
    # client.assign_qualification(response[0].QualificationTypeId, 'A3D1A336ZEGP79', value=1, send_notification=True)

    return response[0].QualificationTypeId

# if __name__ == '__main__':
#     client = get_client('sandbox')
#     create_qualification_typeID(client)