from .constants import SERVICE_PROJECT_NAME
from modules.aws.ssm.param_name import SsmParamName, SsmParamNameComponent
from modules.terminal_ui.constants import ENVIRONMENT_OPTIONS

class SelectionRecorder:

    env_name: str = ""
    aws_env: str = ""
    param_prefix: str = ""

    proj_name: str = ""
    param_name: str = ""
    service_name: str = ""

    full_param_name: SsmParamName

    value: str = ""
    param_type: str = ""

    @classmethod
    def set_aws_env(cls):
        print(f"'SelectionRecorder.set_aws_env(): 'cls.env_name' is {cls.env_name}")
        cls.aws_env = ENVIRONMENT_OPTIONS.get_aws_env(env=cls.env_name)

    @classmethod
    def set_param_prefix(cls):
        cls.param_prefix = ENVIRONMENT_OPTIONS.get_prefix_from_env(env=cls.env_name)

    @classmethod
    def set_param_name(cls):
        cls.service_name = next(
            (service_name for service_name, project_name in SERVICE_PROJECT_NAME if project_name == cls.proj_name), ""
        )

        # automatically parse each parameter name component
        # into the right string format. This will:
        # - get rid of any '/' prefix & suffix
        # - Ensure that if parameter name contains only a single word,
        #   it won't have any '/' prefix in front of it
        cls.full_param_name = SsmParamName(
            [
                SsmParamNameComponent(cls.param_prefix),
                SsmParamNameComponent(cls.service_name),
                SsmParamNameComponent(cls.param_name)
            ]
        )

class SetparamSelectionRecorder(SelectionRecorder):
    pass

class SearchparamSelectionRecorder(SelectionRecorder):
    pass


