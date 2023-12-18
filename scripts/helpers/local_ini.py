import os

class LocalIni():
    def __init__(self, file_path: str):
        """
        Args:
            file_path (str): The file path to the '.ini' file on local machine
        """
        self.param_names: list[str] = list()
        self.param_list: list[tuple[str, str]] = list()
        self.file_path = os.path.abspath(os.path.expanduser(file_path))

    def add_param(self, param_name: str, value: str):
        # check if param has already been added
        if param_name in self.param_names:
            return
        self.param_names.append(param_name)
        self.param_list.append((param_name, value))

    def export_to_ini(self):
        if not os.path.exists(self.file_path):
            try:
                os.makedirs(os.path.dirname(self.file_path))
            except FileExistsError:
                pass

        with open(self.file_path, "w") as output_ini:
            for param_name, value in self.param_list:
                output_ini.write("{param_name}={value}\n".format(
                    param_name=param_name,
                    value=value
                ))
