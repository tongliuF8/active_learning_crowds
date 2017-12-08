

def get_boto2_parameters(environment):
    if environment == 'sandbox':
        return "mechanicalturk.sandbox.amazonaws.com"
    if environment == 'production':
        return "mechanicalturk.amazonaws.com"

    raise RuntimeError("Enter the environment type in the argument ('sandbox' or 'production')\n"
                       "example: python script.py sandbox ..")


def get_boto3_parameters(environment):
    if environment == 'sandbox':
        return "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
    if environment == 'production':
        return "https://mturk-requester.us-east-1.amazonaws.com"

    raise RuntimeError("Enter the environment type in the argument ('sandbox' or 'production')\n"
                       "example: python script.py sandbox ..")