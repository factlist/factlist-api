import os

from django.core.checks import Error, register
from django.core.checks import Tags as DjangoTags


class Tags(DjangoTags):
    environment = 'environment'


@register(Tags.environment)
def check_environment_variables(app_configs, **kwargs):
    errors = []
    variables = [
        'CLIENT_HOST',
        'TWITTER_CONSUMER_SECRET',
        'TWITTER_CONSUMER_KEY',
        'CLIENT_ADDRESS',
        'AWS_SNS_ARN',
        'AWS_STORAGE_BUCKET_NAME',
        'AWS_ACCESS_KEY_ID',
        'AWS_SECRET_ACCESS_KEY',
        'EMBEDLY_API_KEY',
    ]
    for variable in variables:
        if os.environ.get(variable) is None:
            errors.append(
                Error(
                    'Environment variable ' + variable + ' is not set',
                    id='core.E001'
                )
            )
    return errors
