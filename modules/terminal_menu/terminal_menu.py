from simple_term_menu import TerminalMenu
from .constants.menu_selection import EnvSelection


class ParameterSetupSelection:
    env_selection = [env.name for env in EnvSelection]
    param_name = ""
    value = None

    @classmethod
    def show_and_record_selection(cls, options_list: list):
        menu = TerminalMenu(options_list)
        selected_index = menu.show()
        selected = options_list[selected_index]
        cls.param_name += eval(f"EnvSelection.{selected}.value")
        print(f"parameter name: {cls.param_name}")
        return selected

    @classmethod
    def set_key_from_user_input(cls, key: str):
        """
        Args:
            key (str): The 'key' that we want to set this value for
        """
        user_specified_key = input(f"What is the {key} you want to set parameter for? ")
        cls.param_name += f"/{user_specified_key}"
        print(f"parameter name: {cls.param_name}")
        return user_specified_key

    @classmethod
    def get_value_from_user(cls):
        user_specified_value = input("What is the value the parameter will store? ")
        cls.value = user_specified_value
        print(f"{cls.param_name} = {cls.value}")


    @classmethod
    def get_user_selection(cls):
        cls.show_and_record_selection(cls.env_selection)
        cls.set_key_from_user_input("service name")
        cls.set_key_from_user_input("variable name")
        cls.get_value_from_user()

