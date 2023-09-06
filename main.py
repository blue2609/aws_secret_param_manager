from simple_term_menu import TerminalMenu
from modules.aws.boto_client import SsmClient
from modules.terminal_menu.terminal_menu import ParameterSetupSelection
from botocore.exceptions import UnauthorizedSSOTokenError
from modules.aws.ssm.constants.parameter_store import SSM_PARAMETER_TYPE
from helpers.profiles import get_aws_profiles


def main():

    options = get_aws_profiles()
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    profile_name = options[menu_entry_index]

    ParameterSetupSelection.get_user_selection()

    ssm_client = SsmClient(profile_name)
    ssm_client.create_parameter(
        param_name=ParameterSetupSelection.param_name,
        value=ParameterSetupSelection.value,
        type=SSM_PARAMETER_TYPE.STRING
    )


if __name__ == "__main__":
    main()

