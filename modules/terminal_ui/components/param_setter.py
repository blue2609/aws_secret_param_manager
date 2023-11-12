from textual.widgets import (
    Select,
    Input,
    Label,
    Button,
)
from modules.formatted_text.heading import Heading
from modules.formatted_text.status_report import SetParamStatusReport
from modules.terminal_ui.constants import (
    ENVIRONMENT_OPTIONS,
    SERVICE_PROJECT_NAME,
    PARAMETER_TYPE
)
from modules.terminal_ui.custom_widgets.labels import SetParamResultLabel


class SetParamComponent:
    @staticmethod
    def section_header():
        # 1st Row
        yield Label("")
        yield Label(Heading("Setting Param/Secret"), classes="box", id="label_set_param")
        yield Label("")

    @staticmethod
    def creation_menu():
        # First Row
        yield Label("Choose Environment:", classes="box")
        yield Label("Choose Project Name", classes="box")
        yield Label("Parameter Name:", classes="box")

        # Second Row
        yield Select(
            [(env_id, env_name) for env_id, env_name in ENVIRONMENT_OPTIONS.CHOICES], classes="box",
            id="select_setparam_environment"
        )
        yield Select(
            [(service_name, project_name) for service_name, project_name in SERVICE_PROJECT_NAME],
            classes="box",
            id="select_setparam_project_name"
        )

        yield Input(
            placeholder="Write parameter name here...",
            classes="box",
            id="input_param_name"
        )

        # Third Row
        yield Label(
            "Parameter Value:",
            classes="box",
            id="label_param_value"
        )
        yield Label("Type:", classes="box", id="label_type")

        # Fourth Row
        yield Input(placeholder="Write value here...", classes="box", id="input_param_secret_value")

        # Fourth and Fifth Row
        yield Select(
            [(param_type, cloud_service_param_type) for param_type, cloud_service_param_type in PARAMETER_TYPE],
            classes="box",
            id="select_setparam_param_type"
        )

        # Fifth Row
        yield Button("Create | Update", classes="box", id="button_create_parameter")
        yield SetParamResultLabel(classes="box")