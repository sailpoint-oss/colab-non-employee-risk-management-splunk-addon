
import ta_sailpoint_nerm_auditevent_add_on_declare

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    SingleModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunk_aoblib.rest_migration import ConfigMigrationHandler

util.remove_http_proxy_env_vars()


fields = [
    field.RestField(
        'username',
        required=True,
        encrypted=False,
        default=None,
        validator=validator.String(
            min_len=1, 
            max_len=200, 
        )
    ), 
    field.RestField(
        'password',
        required=True,
        encrypted=True,
        default=None,
        validator=validator.String(
            min_len=1, 
            max_len=8192, 
        )
    ),
    field.RestField(
        'tenant_url',
        required=True,
        encrypted=False,
        default=None
    )
]
model = RestModel(fields, name=None)


endpoint = SingleModel(
    'ta_sailpoint_nerm_auditevent_add_on_account',
    model,
)


if __name__ == '__main__':
    admin_external.handle(
        endpoint,
        handler=ConfigMigrationHandler,
    )
