import subprocess
from simple_term_menu import TerminalMenu

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
    print(f"You have selected {options[menu_entry_index]}!")

if __name__ == "__main__":
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
