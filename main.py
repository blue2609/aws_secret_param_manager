from simple_term_menu import TerminalMenu
from modules.aws.boto_client import SsmClient, KmsClient
from modules.terminal_menu.terminal_menu import ParameterSetupSelection
from helpers.profiles import get_aws_profiles


def main():

    aws_profile_list = get_aws_profiles()
    terminal_menu = TerminalMenu(aws_profile_list)
    menu_entry_index = terminal_menu.show()
    profile_name = aws_profile_list[menu_entry_index]

    ParameterSetupSelection.get_user_selection()

    kms_client = KmsClient(profile_name)

    ssm_client = SsmClient(profile_name)
    ssm_client.create_parameter(
        param_name=ParameterSetupSelection.param_name,
        value=ParameterSetupSelection.value,
        type=ParameterSetupSelection.SSM_PARAMETER_TYPE,
        kms_key_id=kms_client.get_kms_key_with_alias("app-key")
    )
    print("{ssm_param_name}:{ssm_param_type} = {ssm_param_value}".format(
       ssm_param_name=ParameterSetupSelection.param_name,
       ssm_param_type=ParameterSetupSelection.SSM_PARAMETER_TYPE,
       ssm_param_value=ParameterSetupSelection.value
    ))


if __name__ == "__main__":
    main()

