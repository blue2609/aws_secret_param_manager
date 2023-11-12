from .selection import SetparamSelectionRecorder, SearchparamSelectionRecorder
from textual import on
from textual.widgets import Select, Input, Header, Button, DataTable, Label
from modules.terminal_ui.custom_widgets.labels import SearchErrorLabel
from textual.app import App, ComposeResult
from modules.aws.boto_client import KmsClient, SsmClient
from .components.param_setter import SetParamComponent
from .components.param_search import SearchParamComponent
from botocore.exceptions import ParamValidationError


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

        yield SearchErrorLabel()
        yield DataTable(classes="box", id="param_secret_table")

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("id", "Name", "Type", "Value", "Version", "Last Modified Date")

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        if "setparam" in event.select.id:
            if event.select.id == "select_setparam_environment":
                SetparamSelectionRecorder.env_name = event.value
                SetparamSelectionRecorder.set_aws_env()
                SetparamSelectionRecorder.set_param_prefix()
            if event.select.id == "select_setparam_project_name":
                SetparamSelectionRecorder.proj_name = event.value
            if event.select.id == "select_setparam_param_type":
                SetparamSelectionRecorder.param_type = event.value

            SetparamSelectionRecorder.set_param_name()
            self.title = str(SetparamSelectionRecorder.full_param_name)

        if "search" in event.select.id:
            if event.select.id == "select_search_environment":
                SearchparamSelectionRecorder.env_name = event.value
                SearchparamSelectionRecorder.set_aws_env()
                SearchparamSelectionRecorder.set_param_prefix()
            if event.select.id == "select_search_project_name":
                SearchparamSelectionRecorder.proj_name = event.value

            SearchparamSelectionRecorder.set_param_name()


    @on(Input.Changed)
    def input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "input_param_name":
            SetparamSelectionRecorder.param_name = event.value
            SetparamSelectionRecorder.set_param_name()
            self.title = str(SetparamSelectionRecorder.full_param_name)
        if event.input.id == "input_param_secret_value":
            SetparamSelectionRecorder.value = event.value
        if event.input.id == "input_search_param_name":
            SearchparamSelectionRecorder.param_name = event.value
            SearchparamSelectionRecorder.set_param_name()

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "button_create_parameter":
            set_param_result_label = self.query_one("SetParamResultLabel")
            full_param_name = str(SetparamSelectionRecorder.full_param_name)

            try:
                kms_client = KmsClient(env=SetparamSelectionRecorder.aws_env)
                ssm_client = SsmClient(env=SetparamSelectionRecorder.aws_env)


                ssm_client.create_parameter(
                    param_name=full_param_name,
                    value=SetparamSelectionRecorder.value,
                    type=SetparamSelectionRecorder.param_type,
                    kms_key_id=kms_client.get_kms_key_with_alias("app-key")
                )
            except Exception as ex:
                set_param_result_label.update(
                    f"Failed to create/update [b]{full_param_name}]\nException: [{ex}][/b]"
                )

        if event.button.id == "button_search_parameter":
            ssm_client = SsmClient(env=SearchparamSelectionRecorder.aws_env)

            full_param_name = SearchparamSelectionRecorder.full_param_name

            # Always try to check if there's a parameter with the exact name
            # as the one selected by the user first
            # if there's none, then return all parameters under the parameter
            # hierarchical path
            try:
                rows = ssm_client.get_parameter(str(full_param_name))
                if not rows:
                    rows = ssm_client.get_parameters_by_path(str(full_param_name))

                table = self.query_one(DataTable)
                table.clear()
                table.add_rows(rows)
            except ParamValidationError as ex:
                label_error = self.query_one("SearchErrorLabel")
                label_error.update(f"Please Ensure that the parameter/secret name is correct\n[b]{ex}[/b]")




