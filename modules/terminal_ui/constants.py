from modules.aws.ssm.constants.parameter_store import SSM_PARAMETER_TYPE
from typing import Union


class AWS_ENV:
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"

    @classmethod
    def values(cls):
        return [
            getattr(cls, attr)
            for attr in dir(cls)
            if not attr.startswith("__") and type(getattr(cls, attr)) is str
        ]


class ENVIRONMENT_OPTIONS:
    DEV = "dev"
    DEV_CLAIMS = "dev_claims"
    DEV_INFRA = "dev_infra"
    DEV_RAPTOR = "dev_raptor"
    DEV_SALES = "dev_sales"
    DEV_REX = "dev_rex"

    STAGE = "stage"
    PROD = "prod"

    DATA = dict()

    DATA[DEV] = {
        "param_prefix": "",
        "aws_env": AWS_ENV.DEV
    }

    DATA[DEV_CLAIMS] = {
        "param_prefix": "claims",
        "aws_env": AWS_ENV.DEV
    }
    DATA[DEV_INFRA] = {
        "param_prefix": "infra",
        "aws_env": AWS_ENV.DEV
    }

    DATA[DEV_RAPTOR] = {
        "param_prefix": "raptor",
        "aws_env": AWS_ENV.DEV
    }

    DATA[DEV_SALES] = {
        "param_prefix": "sales",
        "aws_env": AWS_ENV.DEV
    }

    DATA[DEV_REX] = {
        "param_prefix": "rex",
        "aws_env": AWS_ENV.DEV
    }

    DATA[STAGE] = {
        "param_prefix": "",
        "aws_env": AWS_ENV.STAGE
    }

    DATA[PROD] = {
        "param_prefix": "",
        "aws_env": AWS_ENV.PROD
    }

    CHOICES = [(env_name, env_name) for env_name in DATA]

    @classmethod
    def get_prefix_from_env(cls, env: str) -> Union[str | None]:
        return cls.DATA.get(env, {}).get("param_prefix")

    @classmethod
    def get_aws_env(cls, env: str):
        if isinstance(env, list):
            raise ValueError(f"'env' is a list: {env}")
        return cls.DATA.get(env, {}).get("aws_env")


SERVICE_PROJECT_NAME = [
    ('api', 'open-platform'),
    ('api-aggregator', 'service-aggregator'),
    ('api-solera', 'solera-services'),
    ('api-enrichment', 'enrichment-services'),
]

PARAMETER_TYPE = [
    ('parameter', SSM_PARAMETER_TYPE.STRING.value),
    ('secret', SSM_PARAMETER_TYPE.SECURE_STRING.value)
]
