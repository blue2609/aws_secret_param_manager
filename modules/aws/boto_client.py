import boto3
import pprint
import os
from ..aws.ssm.constants.parameter_store import SSM_PARAMETER_TYPE
from botocore.exceptions import UnauthorizedSSOTokenError
from typing import Optional
import subprocess
from dotenv import load_dotenv
import logging

load_dotenv()

LOGGER = logging.getLogger(__name__)


class BotoClient:
    def __init__(self, aws_service: str):
        """
        Initialise 'BotoClient' object with the chosen 'profile_name'

        Args:
            profile_name (str): The chosen 'profile_name' that will be used to create this client object
            aws_service (str): the name of AWS service that we want to create client for
        """
        try:
            sts = boto3.client('sts')
            sts.get_caller_identity()
        except UnauthorizedSSOTokenError as ex:
            LOGGER.debug(ex)
            subprocess.run(["aws", "sso", "login", "--profile", os.getenv("AWS_PROFILE")])
        self.client = boto3.client(aws_service)


class SsmClient(BotoClient):
    def __init__(self):
        super().__init__("ssm")

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
        put_param_args = {
            "Name": param_name,
            "Value": value,
            "Type": type
        }
        if type == SSM_PARAMETER_TYPE.SECURE_STRING.value:
            put_param_args["KeyId"] = kms_key_id

        self.client.put_parameter(**put_param_args)


class KmsClient(BotoClient):

    def __init__(self):
        super().__init__("kms")

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
