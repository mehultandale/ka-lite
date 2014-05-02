"""
Base classes to help test i18n functions
"""
import os
import urllib
from mock import patch

from django.core.management import call_command
from django.test import Client, TestCase

from .. import get_installed_language_packs


class I18nTestCase(TestCase):

    # TODO (ARON): move useful utility to either a module or TestCase subclass
    def is_language_installed(self, lang_code, force_reload=True):
        return lang_code in get_installed_language_packs(force=force_reload)

    @patch.object(urllib, 'urlretrieve')
    def install_language(self, lang_code, urlretrieve_method):
        test_zip_filepath = os.path.join(os.path.dirname(__file__), 'testzips', '%s.zip' % lang_code)
        urlretrieve_method.return_value = [test_zip_filepath, open(test_zip_filepath)]

        if not self.is_language_installed(lang_code):
            call_command('languagepackdownload', lang_code=lang_code)

    def setUp(self):
        self.client = Client()
        super(TestCase, self).setUp()
