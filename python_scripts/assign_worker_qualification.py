from create_compensation_hit import get_client

def assign(client, worker_id, value=1):
    
    response = client.associate_qualification_with_worker(QualificationTypeId='37RZXPVRUCAHK9IR9K2HHRIN6ZO1L2', WorkerId=worker_id, IntegerValue=value, SendNotification=False)

if __name__ == '__main__':
    client = get_client()
    assign(client, 'A3VOSKJ5LS9WB', value=1)