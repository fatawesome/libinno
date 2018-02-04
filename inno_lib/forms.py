from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import datetime


class RenewDocumentForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 3 weeks (default 2).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=3):
            raise ValidationError(_('Invalid date - renewal more than 3 weeks ahead'))

        return data
