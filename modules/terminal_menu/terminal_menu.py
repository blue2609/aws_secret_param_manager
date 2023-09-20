from simple_term_menu import TerminalMenu
from .constants.menu_selection import ENV_SELECTION
from modules.aws.ssm.constants.parameter_store import SSM_PARAMETER_TYPE
from enum import Enum


class ParameterSetupSelection:
    env_selection = [env.name for env in ENV_SELECTION]
    ssm_parameter_type_selection = [el.name for el in SSM_PARAMETER_TYPE]
    param_name = ""
    value = None

    @classmethod
    def show_and_record_selection(
        cls,
        options_list: list,
        enum_class: Enum,
        enum_class_name: str
    ):
        menu = TerminalMenu(options_list)
        selected_index = menu.show()
        selected = options_list[selected_index]
        setattr(
            cls,
            enum_class_name,
            getattr(enum_class, selected).value
        )
        print(f"{enum_class_name} value selected: {getattr(cls, enum_class_name)}")
        return selected

    @classmethod
    def set_key_from_user_input(cls, key: str):
        """
        Args:
            key (str): The 'key' that we want to set this value for
        """
        user_specified_key = input(f"What is the {key} you want to set parameter for? ")
        cls.param_name += f"/{user_specified_key}"
        print(f"parameter name: {cls.ENV_SELECTION}{cls.param_name}")
        return user_specified_key

    @classmethod
    def get_value_from_user(cls):
        user_specified_value = input("What is the value the parameter will store? ")
        cls.value = user_specified_value
        print(f"{cls.param_name} = {cls.value}")

    @classmethod
    def get_user_selection(cls):
        cls.show_and_record_selection(cls.env_selection, ENV_SELECTION, "ENV_SELECTION")
        cls.show_and_record_selection(cls.ssm_parameter_type_selection, SSM_PARAMETER_TYPE, "SSM_PARAMETER_TYPE")
        cls.set_key_from_user_input("service name")
        cls.set_key_from_user_input("name of the setting")
        cls.get_value_from_user()