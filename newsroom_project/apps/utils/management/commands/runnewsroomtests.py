import sys

from django.core.management.base import BaseCommand
from utils import settings
from django.test.simple import run_tests

class Command(BaseCommand):
    option_list = BaseCommand.option_list + ()
    help = "Runs the tests related to the newsroom."
    # Validation is called explicitly each time the server is reloaded.
    requires_model_validation = False

    def handle(self, *args, **options):
        APP_TO_TEST = settings.NEWSROOM_TEST_SUITE
        print "The following apps is going to be tested : "
        for app in APP_TO_TEST:
            print "    * %s " % app
            
        failures = run_tests(APP_TO_TEST, verbosity=options["verbosity"])
        if failures:
            sys.exit(failures)
