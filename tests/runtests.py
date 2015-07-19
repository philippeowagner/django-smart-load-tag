#!/usr/bin/env python
"""
This script is a trick to setup a fake Django environment, since this reusable
app will be developed and tested outside any specifiv Django project.
Via ``settings.configure`` you will be able to set all necessary settings
for your app and run the tests as if you were calling ``./manage.py test``.
"""

import sys
import django
from django.conf import settings


def setup():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }

    INSTALLED_APPS = [
        'smart_load_tag',
    ]
    if django.VERSION >= (1,6):
        TEST_RUNNER = 'django.test.runner.DiscoverRunner'
    else:
        TEST_RUNNER = 'django.test.simple.DjangoTestSuiteRunner'

    from django.conf import settings

    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=INSTALLED_APPS,
            DATABASES=DATABASES,
            TEST_RUNNER=TEST_RUNNER,
            ROOT_URLCONF='smart_load_tag.testproject.urls'
        )




def runtests(*test_args):

    if django.VERSION >= (1,7):
        django.setup()


    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=False, failfast=False)

    failures = test_runner.run_tests(test_args)

    sys.exit(failures)


if __name__ == '__main__':
    setup()
    runtests(*sys.argv[1:])
    
    
    

#!/bin/sh
#
#$CWD=`pwd`
#export PYTHONPATH=/..:$PYTHONPATH # add smart_load_tag app to path
#
#django-admin.py test testapp --settings=testproject.settings
