from modules.aws.ssm.constants.parameter_store import SSM_PARAMETER_TYPE

ENVIRONMENT_OPTIONS = [
    ('dev', 'dev'),
    ('dev-claims', 'claims'),
    ('dev-raptor', 'raptor'),
    ('dev-sales', 'sales'),
    ('dev-rex', 'rex'),
    ('dev-infra', 'infra'),
    ('stage', 'stage'),
    ('prod', 'prod')
]

SERVICE_PROJECT_NAME = [
    ('api', 'open-platform'),
    ('api-aggregator', 'service-aggregator'),
    ('api-solera', 'solera-services'),
    ('api-enrichment', 'enrichment-services'),
]

PARAMETER_TYPE = [
    ('parameter', SSM_PARAMETER_TYPE.STRING.value),
    ('secret', SSM_PARAMETER_TYPE.SECURE_STRING.value)
]

