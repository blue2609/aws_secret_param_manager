import subprocess
from simple_term_menu import TerminalMenu
from modules.aws.boto_client import SsmClient
from modules.terminal_menu.terminal_menu import ParameterSetupSelection
from botocore.exceptions import UnauthorizedSSOTokenError
from modules.aws.ssm.constants.parameter_store import SSM_PARAMETER_TYPE


def get_aws_profiles_list() -> list:
    """
    Returns:
        list: The list of AWS profiles stored on the machine where this program is running
    """
    aws_profiles_list_str = subprocess.run(
        ["aws", "configure", "list-profiles"],
        capture_output=True
    )
    decoded_str = aws_profiles_list_str.stdout.decode("UTF-8")
    return list(filter(None, decoded_str.split("\n")))


def main():

    options = get_aws_profiles_list()
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
    # print(ssm_client.get_parameter("/dev/api/claims/opb_dns"))


if __name__ == "__main__":
    main()

