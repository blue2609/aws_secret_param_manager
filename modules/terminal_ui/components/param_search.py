from textual.widgets import (
    Select,
    Input,
    Label,
    Button,
)

from modules.formatted_text.heading import Heading

from modules.terminal_ui.constants import (
    ENVIRONMENT_OPTIONS,
    SERVICE_PROJECT_NAME,
)

class SearchParamComponent:

    @staticmethod
    def section_header():
        # 6th Row
        yield Label("")
        yield Label(Heading("Search Param/Secret"), classes="box", id="label_datatable_header")
        yield Label("")

    @staticmethod
    def search_menu():
        yield Label("Choose Environment:", classes="box")
        yield Label("Choose Project Name", classes="box")
        yield Label("Parameter Name:", classes="box")

        # Second Row
        yield Select(
            [(env_id, env_name) for env_id, env_name in ENVIRONMENT_OPTIONS], classes="box",
            id="select_search_environment"
        )
        yield Select(
            [(service_name, project_name) for service_name, project_name in SERVICE_PROJECT_NAME],
            classes="box",
            id="select_search_project_name"
        )

        yield Input(
            placeholder="parameter name to search...",
            classes="box",
            id="input_search_param_name"
        )

        # Fifth Row
        yield Button("Search Param/Secret", classes="box", id="button_search_parameter")
