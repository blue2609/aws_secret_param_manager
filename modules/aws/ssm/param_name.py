class SsmParamNameComponent:
    def __init__(self, component_value):
        self.raw_str = component_value if bool(component_value) else ""
        self.normalised_str = ""

        self.set_normalised_str()

    def set_normalised_str(self):
        self.normalised_str = self.raw_str.strip("/")

    def __add__(self, name_component):
        return SsmParamNameComponent(f"{self.normalised_str}/{name_component.normalised_str}")

    def __repr__(self):
        return f"<{self.__class__.__name__}> raw: {self.raw_str}, normalised: {self.normalised_str}"


class SsmParamName:
    def __init__(self, components: list[SsmParamNameComponent]):
        self.components = components
        self.param_name = ""
        self.is_hierarchical = False
        self._construct_param_name()

    def _decide_if_name_is_hierarchical(self, param_name) -> None:
        """
        Args:
            param_name (str): the full parameter name

        Returns:
            bool: 'True' if parameter contains hierarchical structure. Otherwise, returns 'False'
        """
        hierarchy_list = list(
            filter(lambda el: el != "", param_name.split("/"))
        )
        self.is_hierarchical = False if len(hierarchy_list) <= 1 else True

    def _construct_param_name(self):
        param_name = SsmParamNameComponent("")
        for component in self.components:
            param_name += component

        self._decide_if_name_is_hierarchical(param_name.normalised_str)

        if self.is_hierarchical:
            self.param_name = "/" + param_name.normalised_str
            return

        self.param_name = param_name.normalised_str

    def __str__(self):
        return self.param_name


param_name = SsmParamName(
    [
        SsmParamNameComponent("dev")
    ]
)

print(param_name, param_name.is_hierarchical)

