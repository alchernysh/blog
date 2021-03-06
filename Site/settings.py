import os
from split_settings.tools import optional, include

include(
    'settings/other_settings.py',
    'settings/DATABASES.py',
    'settings/INSTALLED_APPS.py',
    'settings/MIDDLEWARE.py',
    'settings/TEMPLATES.py',
    'settings/AUTH_PASSWORD_VALIDATORS.py',
    'settings/CKEDITOR_CONFIGS.py',
    'settings/EMAIL.py'
)


