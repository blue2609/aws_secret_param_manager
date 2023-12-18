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
AWS_ACCOUNTS = ['dev', 'stage', 'prod']


class BotoClient:

    def __init__(self, env: str, aws_service: str):
        """
        Initialise 'BotoClient' object with the chosen 'profile_name'

        Args:
            env (str): The AWS account environment that the client will be created for. Argument passed here must be either 'dev', 'stage' or 'prod'
            aws_service (str): the name of AWS service that we want to create client for
        """
        self.aws_service = aws_service
        self.env = env
        self._validate_env()
        self._init_client()

    def _validate_env(self):
        if self.env not in AWS_ACCOUNTS:
            raise ValueError(
                f"Wrong 'env' argument passed to 'BotoClient()'. Passed env is [{self.env}], expecting either 'dev', 'stage', 'prod'")

    def _init_client(self) -> None:
        """
        initialise boto3 client
        """
        try:
            aws_profile = os.environ[f"{self.env.upper()}_AWS_PROFILE"]
            session = boto3.session.Session(profile_name=aws_profile)

            # try to execute something with boto3 client
            # to make sure that the session token hasn't expired
            # if it has, the app will open web browser automatically
            # and force the user to renew their session token
            try:
                sts_client = session.client('sts')
                sts_client.get_caller_identity()
            except UnauthorizedSSOTokenError as ex:
                LOGGER.debug(ex)
                subprocess.run(["aws", "sso", "login", "--profile", aws_profile])

            self.client = session.client(self.aws_service)

        except KeyError as ex:
            LOGGER.info(
                "AWS_PROFILE env variables haven't been configured correctly! Exception",
                extra={"exc_message": ex}
            )
            raise


class SsmClient(BotoClient):
    def __init__(self, env: str):
        super().__init__(env=env, aws_service="ssm")

    def get_parameters_by_path(
            self,
            path: str,
            recursive: Optional[bool] = True,
            with_decryption: bool = True,
            param_type: str = None
    ):

        # Ensure that 'path' argument has '/' prefix
        if not path.startswith("/"):
            path = "/" + path

        kwargs = {
            "Path": path,
            "Recursive": recursive,
            "WithDecryption": with_decryption,
            "MaxResults": 10,
        }

        if param_type:
            kwargs["ParameterFilters"] = [
                {
                    "Key": "Type",
                    "Option": "Equals",
                    "Values": [
                        param_type
                    ]
                }
            ]

        response = self.client.get_parameters_by_path(**kwargs)
        all_params_list = []
        if isinstance(response, dict) and (param_list := response.get("Parameters")):
            for index, param_details in enumerate(param_list, start=1):
                all_params_list.append(
                    (
                        index,
                        param_details.get("Name"),
                        param_details.get("Type"),
                        param_details.get("Value"),
                        param_details.get("Version"),
                        param_details.get("LastModifiedDate").strftime("%d-%m-%Y")
                    )
                )
            next_token = response.get("NextToken")
            next_token_iteration = 1
            while next_token:
                kwargs["NextToken"] = next_token
                index_start = 10 * next_token_iteration + 1

                response = self.client.get_parameters_by_path(**kwargs)
                if isinstance(response, dict) and (param_list := response.get("Parameters")):
                    for index, param_details in enumerate(param_list, start=index_start):
                        all_params_list.append(
                            (
                                index,
                                param_details.get("Name"),
                                param_details.get("Type"),
                                param_details.get("Value"),
                                param_details.get("Version"),
                                param_details.get("LastModifiedDate").strftime("%d-%m-%Y")
                            )
                        )
                next_token_iteration += 1
                next_token = response.get("NextToken")

            return all_params_list

        return []

    def get_parameter(self, param_path):
        try:
            response = self.client.get_parameter(
                Name=param_path,
                WithDecryption=True
            )
            if isinstance(response, dict) and (param_details := response.get("Parameter")):
                return [
                    (
                        1,  # to indicate the first row
                        param_details.get("Name"),
                        param_details.get("Type"),
                        param_details.get("Value"),
                        param_details.get("Version"),
                        param_details.get("LastModifiedDate").strftime("%d-%m-%Y")
                    )
                ]

        except self.client.exceptions.ParameterNotFound as ex:
            LOGGER.info(f"no parameter with name {param_path} is found", extra={
                "exc_message": ex
            })
            return []
        except Exception as ex:
            return []

    def create_parameter(
            self,
            param_name: str,
            value: str,
            type: str,
            kms_key_id: str
    ):
        """
        Create a new SSM parameter in SSM parameter store

        Args:
            aws_env (str): The
            param_name (str): The parameter name of the new parameter created
            value (str): The value that will be set for new parameter created
            type (SSM_PARAMETER_TYPE): one of the 3 predefined types of SSM parameter store
        """
        put_param_args = {
            "Name": param_name,
            "Value": value,
            "Type": type,
            "Overwrite": True
        }
        if type == SSM_PARAMETER_TYPE.SECURE_STRING.value:
            put_param_args["KeyId"] = kms_key_id

        self.client.put_parameter(**put_param_args)


class KmsClient(BotoClient):

    def __init__(self, env: str):
        super().__init__(env=env, aws_service="kms")

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
