from create_compensation_hit import get_client
from insert_data_into_mongodb import get_data_path


def create_qualification_typeID(client):
    logfile = open(get_data_path() + '/Qualification.txt', 'w')
    response = client.create_qualification_type(
        Name = "7",
        Description = "Only workers affected by our system could work on this task.",
        QualificationTypeStatus = "Active",
        AutoGranted = True,
        AutoGrantedValue = 1)

    logfile.write("Your Qualification is created. Your Qualification Type ID is:\n")
    logfile.write(response['QualificationType']['QualificationTypeId'])
    return response['QualificationType']['QualificationTypeId']

if __name__ == '__main__':
    client = get_client()
    create_qualification_typeID(client)