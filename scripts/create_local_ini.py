from helpers.path import add_root_dir_to_search_path
from helpers.local_ini import LocalIni

add_root_dir_to_search_path()

import argparse
from dotenv import load_dotenv
from modules.aws.boto_client import SsmClient
from modules.terminal_ui.constants import AWS_ENV
from modules.aws.ssm.constants.parameter_store import SSM_PARAMETER_TYPE


def set_args():
    args = argparse.ArgumentParser()
    args.add_argument(
        "-p",
        "--prefixes",
        nargs="*",
        help="The list of prefixes in the order of precedence you want to use to generate the '.ini' file. Will default to ['/local', '/']",
        default=["/local", "/"]
    )
    args.add_argument(
        "-e",
        "--env",
        choices=AWS_ENV.values(),
        help="the AWS account that you want to extract parameters from. Possible options are 'dev', 'stage' and 'prod'. Will default to 'dev'",
        default="dev"
    )
    args.add_argument(
        "-o",
        "--outputfile",
        help="path to the output '.ini' file (can be relative path)",
        required=True
    )
    return args.parse_args()


def load_parameters(prefix: str, aws_env: str) -> list[tuple]:
    """
    Args:
        prefix (str): string such as '/claims', '/raptor' that prefix SSM parameter names we want to search for
        aws_env (str): The AWS account we want to load SSM parameters from. Must be either 'dev', 'stage' or 'prod'
    Returns:
        list[tuple]: A list of parameter names and values in the format of [('param_name', 'value'), ('param_name', 'value')]
    """
    # prefix = f"/platform" if prefix == '/' else prefix
    ssm_client = SsmClient(aws_env)
    param_list = ssm_client.get_parameters_by_path(
        path="/platform" if prefix == '/' else prefix,
        param_type=SSM_PARAMETER_TYPE.STRING.value
    )
    final_param_list = list()
    for param in param_list:
        param_name = param[1].removeprefix(prefix).strip("/")
        if "/" in param_name:
            param_name = "/" + param_name

        value = param[3]
        final_param_list.append((param_name, value))
    return final_param_list


def main():
    load_dotenv()
    args = set_args()

    local_ini = LocalIni(args.outputfile)

    if args.prefixes:
        for prefix in args.prefixes:
            param_list = load_parameters(prefix, args.env)
            for param in param_list:
                local_ini.add_param(param_name=param[0], value=param[1])

    local_ini.export_to_ini()


if __name__ == "__main__":
    main()
