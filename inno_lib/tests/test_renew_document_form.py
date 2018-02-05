from django.test import TestCase
from django.utils import timezone

from inno_lib.forms import RenewDocumentForm

import datetime


class RenewDocumentFormTest(TestCase):

    def test_renew_form_date_field_label(self):
        form = RenewDocumentForm()
        self.assertTrue(
            form.fields['renewal_date'].label is None or form.fields['renewal_date'].label == 'renewal_date')

    def test_renew_form_date_field_help_text(self):
        form = RenewDocumentForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 3 weeks (default 2).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'renewal_date': date}
        form = RenewDocumentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=3, days=1)
        form_data = {'renewal_date': date}
        form = RenewDocumentForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form_data = {'renewal_date': date}
        form = RenewDocumentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=3)
        form_data = {'renewal_date': date}
        form = RenewDocumentForm(data=form_data)
        self.assertTrue(form.is_valid())