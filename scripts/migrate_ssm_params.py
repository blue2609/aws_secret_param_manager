import boto3
import re
import argparse
import os


class MODE:
    SECRET = "secret"
    PARAM = "param"


def _set_args():
    args = argparse.ArgumentParser()
    args.add_argument(
        "-f",
        "--filepath",
        help="the file path to '.ini' file that contains params/secrets to migrate to AWS SSM parameter store"
    )
    args.add_argument(
        "-p",
        "--profile",
        help=f"Specify which AWS profile we want to use to run this script"
    )

    args.add_argument(
        "-k",
        "--kmskeyid",
        help=f"Specify the AWS KMS Key ID that will be used to create a new AWS SSM Parameter Store 'SecureString' parameters"
    )

    args.add_argument(
        "-m",
        "--prefix",
        help=f"Set a prefix that should be added to the beginning of each AWS SSM parameter name"
    )
    return args.parse_args()


def is_secret(line):
    # Check if the line contains the identifier for a secret
    return "(str, secret)" in line


def add_parameters_to_parameter_store(
        file_path: str,
        profile_name: str,
        kms_key_id: str,
        prefix: str = "",
):
    # Initialize a session using a specific profile
    session = boto3.Session(profile_name=profile_name)

    # Initialize boto3 client for SSM using the session
    ssm_client = session.client('ssm')

    # Open and read the INI file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Skip empty lines or lines without '='
            if '=' not in line or line.strip() == '':
                continue

            # Split the line into key-value pair and comment
            parts = line.split('=')

            description = ""
            key = f"{prefix}{parts[0].strip()}"
            value_comment_description = '='.join(parts[1:]).strip()
            value_comment_description = list(
                filter(
                    bool,
                    re.split(r'\s+#', value_comment_description)
                )
            )
            if len(value_comment_description) == 1:
                print(f"There are no comments set for this SSM parameter [{key}]! SSM parameter failed to be created!")
                continue
            elif len(value_comment_description) == 2:
                value = value_comment_description[0].strip('" ')
                comment = value_comment_description[1].strip('" ')
            elif len(value_comment_description) == 3:
                # value, comment, description = value_comment_description
                value = value_comment_description[0].strip('" ')
                comment = value_comment_description[1].strip('" ')
                description = value_comment_description[2].strip('" ')
            else:
                print(
                    f"invalid SSM parameter definition in the '.ini' file for SSM parameter [{key}], skipping the creation of this parameter")
                continue
            # description = re.split(r'\s+#', value_comment_description)[0].strip('" ')

            # Determine if it's a secret
            param_type = 'SecureString' if is_secret(line) else 'String'

            put_parameter_args = {
                "Name": key,
                "Value": value,
                "Type": param_type,
                "Overwrite": True,
                "Description": description
            }
            if param_type == "SecureString":
                put_parameter_args["KeyId"] = kms_key_id

            # Put parameter in AWS Parameter Store
            try:
                ssm_client.put_parameter(**put_parameter_args)
                print(f"Added {'secret' if param_type == 'SecureString' else 'non-secret'} parameter: {key}")
            except Exception as e:
                print(f"Error adding parameter {key}: {e}")


if __name__ == "__main__":
    args = _set_args()
    ini_file_path = os.path.abspath(
        os.path.expanduser(args.filepath)
    )
    # Replace 'your_ini_file.ini' with the path to your INI file
    # Replace 'your_profile_name' with the name of your AWS profile
    add_parameters_to_parameter_store(
        file_path=ini_file_path,
        profile_name=args.profile,
        kms_key_id=args.kmskeyid,
        prefix=args.prefix
    )
