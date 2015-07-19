#!/usr/bin/env python
"""
This script is a trick to setup a fake Django environment, since this reusable
app will be developed and tested outside any specifiv Django project.
Via ``settings.configure`` you will be able to set all necessary settings
for your app and run the tests as if you were calling ``./manage.py test``.
"""
import sys

from django.conf import settings

from testproject import settings as test_settings

if not settings.configured:
    settings.configure(**test_settings.__dict__)

from django_nose import NoseTestSuiteRunner


class NoseCoverageTestRunner(NoseTestSuiteRunner):
    """Custom test runner that uses nose and coverage"""
    pass


def runtests(*test_args):
    import django
    if django.VERSION >= (1, 7):
        django.setup()
    failures = NoseCoverageTestRunner(verbosity=2, interactive=True).run_tests(test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
    
    
    

#!/bin/sh
#
#$CWD=`pwd`
#export PYTHONPATH=/..:$PYTHONPATH # add smart_load_tag app to path
#
#django-admin.py test testapp --settings=testproject.settings
