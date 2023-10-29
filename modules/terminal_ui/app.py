from .selection import SetparamSelectionRecorder, SearchparamSelectionRecorder
from textual import on
from textual.widgets import Select, Input, Header, Button, DataTable
from textual.app import App, ComposeResult
from modules.aws.boto_client import KmsClient, SsmClient
from .components.param_setter import SetParamComponent
from .components.param_search import SearchParamComponent


class SelectApp(App):
    CSS_PATH = "../../tui_style.tcss"

    def compose(self) -> ComposeResult:
        yield Header()

        # Render "Set Parameter/Secret" Components
        for component in SetParamComponent.section_header():
            yield component
        for component in SetParamComponent.creation_menu():
            yield component

        # Render "Search Parameter/Secret" Components
        for component in SearchParamComponent.section_header():
            yield component
        for component in SearchParamComponent.search_menu():
            yield component

        yield DataTable(classes="box", id="param_secret_table")

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