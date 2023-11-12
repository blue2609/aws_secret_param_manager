from textual.widgets import Static
from modules.formatted_text.status_report import SetParamStatusReport

class SearchErrorLabel(Static):
    def on_mount(self) -> None:
        self.update("...display search error...")

class SetParamResultLabel(Static):
    def on_mount(self) -> None:
        self.update(SetParamStatusReport("-- SET PARAMETER STATUS -- "))
