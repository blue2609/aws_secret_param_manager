import subprocess
from simple_term_menu import TerminalMenu
from modules.boto_client import SsmClient

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

    ssm_client = SsmClient(profile_name)
    # print(ssm_client.get_parameter("/dev/api/claims/opb_dns"))
    print(ssm_client.get_parameter("/test/parameter/one"))


if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
