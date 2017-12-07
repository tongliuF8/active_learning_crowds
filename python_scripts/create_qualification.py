from create_compensation_hit import get_client

def create_qualification_typeID(client):

    response = client.create_qualification_type(
        Name = "Worker ID Matching",
        Description = "Only workers affected by our system could work on this task.",
        QualificationTypeStatus = "Active",
        AutoGranted = True,
        AutoGrantedValue = 1)

    print("Your Qualification is created. Your Qualification Type ID is:")
    print(response['QualificationType']['QualificationTypeId'])

if __name__ == '__main__':
    client = get_client()
    create_qualification_typeID(client)

    # 3OVRYEBS3RAGB2XU0GMNUN7WP5V9DL
    # 37RZXPVRUCAHK9IR9K2HHRIN6ZO1L2