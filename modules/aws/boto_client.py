import boto3
import pprint
from ..aws.ssm.constants.parameter_store import SSM_PARAMETER_TYPE
from botocore.exceptions import UnauthorizedSSOTokenError
from typing import Optional
import subprocess


class BotoClient:
    def __init__(self, profile_name: str, aws_service: str):
        """
        Initialise 'BotoClient' object with the chosen 'profile_name'

        Args:
            profile_name (str): The chosen 'profile_name' that will be used to create this client object
            aws_service (str): the name of AWS service that we want to create client for
        """
        session = boto3.Session(profile_name=profile_name)
        try:
            sts = session.client('sts')
            sts.get_caller_identity()
        except UnauthorizedSSOTokenError as ex:
            subprocess.run(["aws", "sso", "login", "--profile", profile_name])
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

    def create_parameter(self, param_name: str, value: str, type: str, kms_key_id: str):
        """
        Create a new SSM parameter in SSM parameter store

        Args:
            param_name (str): The parameter name of the new parameter created
            value (str): The value that will be set for new parameter created
            type (SSM_PARAMETER_TYPE): one of the 3 predefined types of SSM parameter store
        """
        self.client.put_parameter(
            Name=param_name,
            Value=value,
            Type=type,
            KeyId=kms_key_id
        )


class KmsClient(BotoClient):

    def __init__(self, profile_name: str):
        super().__init__(profile_name, "kms")

    def get_kms_key_with_alias(
            self,
            alias: str,
            next_marker: Optional[str] = None,
            limit: Optional[int] = 100
    ):
        response = self.client.list_aliases(Limit=limit)
        next_marker = response.get("NextMarker")
        truncated = response.get("Truncated")
        key_id = next(
            (
                alias_details.get("TargetKeyId")
                for alias_details in response.get('Aliases', [])
                if alias_details.get("AliasName") == f"alias/{alias}"
            ),
            None
        )
        if key_id:
            return key_id
        if truncated and next_marker:
            return self.get_kms_key_with_alias(alias=alias, next_marker=next_marker)
