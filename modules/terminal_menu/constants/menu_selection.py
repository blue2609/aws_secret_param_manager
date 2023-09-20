from enum import Enum


class ENV_SELECTION(Enum):
    DEV_CLAIMS = "/dev/claims"
    DEV_SALES = "/dev/sales"
    DEV_RAPTOR = "/dev/raptor"
    DEV_INFRA = "/dev/infra"
    DEV = "/dev"
    STAGE = "/stage"
    PROD = "/prod"
