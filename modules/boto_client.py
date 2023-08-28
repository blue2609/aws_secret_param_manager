import boto3
import pprint

class BotoClient:
    def __init__(self, profile_name: str, aws_service: str):
        """
        Initialise 'BotoClient' object with the chosen 'profile_name'

        Args:
            profile_name (str): The chosen 'profile_name' that will be used to create this client object
            aws_service (str): the name of AWS service that we want to create client for
        """
        session = boto3.Session(profile_name=profile_name)
        self.client = session.client(aws_service)


class SsmClient(BotoClient):
    def __init__(self, profile_name: str):
        super().__init__(profile_name, "ssm")

    def get_parameter(self, param_path):
        param_value = self.client.get_parameter(
            Name=param_path,
            WithDecryption=True
        )
        return pprint.pformat(param_value)
