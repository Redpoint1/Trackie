import django.contrib.auth.forms as auth_forms

from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class RegisterForm(auth_forms.UserCreationForm):
    tos = auth_forms.forms.BooleanField(
        widget=auth_forms.forms.CheckboxInput,
        label=_('I have read and agree to the Terms of Service'),
        error_messages={
            'required': _("You must agree to the terms to register")}
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        fields = ("username", "email",)

    def clean_email(self):
        cleaned_value = self.cleaned_data['email']
        validator = EmailValidator()
        validator(cleaned_value)

        if User.objects.filter(email__iexact=cleaned_value):
            raise auth_forms.forms.ValidationError(_(
                "This email address is already in use. Please supply a "
                "different email address."))

        return cleaned_value
