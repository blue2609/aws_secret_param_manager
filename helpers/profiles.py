import boto3

def get_aws_profiles() -> list[str]:
    """
    Get a list of AWS profiles set on the machine.
    This method assumes that all AWS profiles have been properly setup in
    '~/.aws/config' and '~/.aws/credentials' files

    Returns:
        list:  A list of AWS profiles available on the machine
    """
    return boto3.session.Session().available_profiles

