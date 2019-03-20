# Copyright (C) 2018 Intel Corporation
#
# SPDX-License-Identifier: MIT

from .base import *

import json
import os

DEBUG = False

INSTALLED_APPS += [
    'mod_wsgi.server',
]

MIDDLEWARE += [
    'basicauth.middleware.BasicAuthMiddleware',
]

BASICAUTH_USERS = os.getenv('BASICAUTH_USERS')
if os.getenv('RUN_ON_AWS') and not BASICAUTH_USERS:
    raise Exception("BASICAUTH_USERS envirionment variable required.")
# Remarks: Should skip json.load when called from collectstatic
if BASICAUTH_USERS:
    BASICAUTH_USERS = json.loads(BASICAUTH_USERS)

for key in RQ_QUEUES:
    RQ_QUEUES[key]['HOST'] = os.getenv('REDIS_HOST')

CACHEOPS_REDIS['host'] = os.getenv('REDIS_HOST')

# Django-sendfile:
# https://github.com/johnsensible/django-sendfile
SENDFILE_BACKEND = 'sendfile.backends.xsendfile'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DB_HOST'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'),
    }
}
