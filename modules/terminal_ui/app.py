from .constants import ENVIRONMENT_OPTIONS, SERVICE_PROJECT_NAME, PARAMETER_TYPE
from .selection import SelectionRecorder
from textual import on
from textual.widgets import Select, Input, Label, Header, Button
from textual.app import App, ComposeResult
from modules.aws.boto_client import KmsClient, SsmClient

class SelectApp(App):
    CSS_PATH = "../../tui_style.tcss"

    def compose(self) -> ComposeResult:

        yield Header()

        # First Row
        yield Label("Choose Environment:", classes="box")
        yield Label("Choose Project Name", classes="box")
        yield Label("Parameter Name:", classes="box")

        # Second Row
        yield Select([(env_id, env_name) for env_id, env_name in ENVIRONMENT_OPTIONS], classes="box",
                     id="select_environment")
        yield Select([(service_name, project_name) for service_name, project_name in SERVICE_PROJECT_NAME],
                     classes="box", id="select_project_name")
        yield Input(placeholder="Write parameter name here...", classes="box", id="input_param_name")

        # Third Row
        yield Label("Parameter Value:", classes="box", id="label_param_value")
        yield Label("Type:", classes="box", id="label_type")

        # Fourth Row
        yield Input(placeholder="Write value here...", classes="box", id="input_param_secret_value")

        # Fourth and Fifth Row
        yield Select(
            [(param_type, cloud_service_param_type) for param_type, cloud_service_param_type in PARAMETER_TYPE],
            classes="box",
            id="select_param_type"
        )

        # Fifth Row
        yield Button("Create Parameter", classes="box", id="button_create_parameter")

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "select_environment":
            SelectionRecorder.env_name = event.value
        if event.select.id == "select_project_name":
            SelectionRecorder.proj_name = event.value
        if event.select.id == "select_param_type":
            SelectionRecorder.param_type = event.value

        self.title = SelectionRecorder.get_param_name()

    @on(Input.Changed)
    def input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "input_param_name":
            SelectionRecorder.param_name = event.value
            self.title = SelectionRecorder.get_param_name()
        if event.input.id == "input_param_secret_value":
            SelectionRecorder.value = event.value

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        kms_client = KmsClient()
        ssm_client = SsmClient()

        ssm_client.create_parameter(
            param_name=SelectionRecorder.get_param_name(),
            value=SelectionRecorder.value,
            type=SelectionRecorder.param_type,
            kms_key_id=kms_client.get_kms_key_with_alias("app-key")
        )