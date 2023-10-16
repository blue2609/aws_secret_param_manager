from .constants import SERVICE_PROJECT_NAME

class SelectionRecorder:
    env_name: str = ""
    proj_name: str = ""
    param_name: str = ""
    service_name: str = ""

    value: str = ""

    button_pressed: str = ""
    param_type: str = ""

    @classmethod
    def get_param_name(cls):
        cls.service_name = next(
            (service_name for service_name, project_name in SERVICE_PROJECT_NAME if project_name == cls.proj_name), ""
        )
        return f"/{cls.env_name}/{cls.service_name}/{cls.param_name}"

