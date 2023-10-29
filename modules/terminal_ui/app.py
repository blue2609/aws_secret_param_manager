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

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("id", "Name", "Type", "Value", "Version", "Last Modified Date")

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if "setparam" in event.select.id:
            if event.select.id == "select_setparam_environment":
                SetparamSelectionRecorder.env_name = event.value
            if event.select.id == "select_setparam_project_name":
                SetparamSelectionRecorder.proj_name = event.value
            if event.select.id == "select_setparam_param_type":
                SetparamSelectionRecorder.param_type = event.value

            self.title = SetparamSelectionRecorder.get_param_name()

        if "search" in event.select.id:
            if event.select.id == "select_search_environment":
                SearchparamSelectionRecorder.env_name = event.value
            if event.select.id == "select_search_project_name":
                SearchparamSelectionRecorder.proj_name = event.value


    @on(Input.Changed)
    def input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "input_param_name":
            SetparamSelectionRecorder.param_name = event.value
            self.title = SetparamSelectionRecorder.get_param_name()
        if event.input.id == "input_param_secret_value":
            SetparamSelectionRecorder.value = event.value

        if event.input.id == "input_search_param_name":
            SearchparamSelectionRecorder.param_name = event.value

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        kms_client = KmsClient()
        ssm_client = SsmClient()

        if event.button.id == "button_create_parameter":
            ssm_client.create_parameter(
                param_name=SetparamSelectionRecorder.get_param_name(),
                value=SetparamSelectionRecorder.value,
                type=SetparamSelectionRecorder.param_type,
                kms_key_id=kms_client.get_kms_key_with_alias("app-key")
            )

        if event.button.id == "button_search_parameter":
            rows = ssm_client.get_parameters_by_path(SearchparamSelectionRecorder.get_param_name())

            table = self.query_one(DataTable)
            table.clear()
            table.add_rows(rows)

