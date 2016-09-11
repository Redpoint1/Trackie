from allauth.account.forms import SignupForm
import allauth.account.app_settings as app_settings


class RegisterForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'data-ng-model': 'password1',
            'class': 'form-control',
            'required': 'required',
            'data-same-value-as': "id_password2",
            'pattern': ".{6,}",
        })
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields['password2'].widget.attrs.update({
                'data-ng-model': 'password2',
                'class': 'form-control',
                'required': 'required',
                'pattern': ".{6,}",
            })
        if self.username_required:
            self.fields['username'].widget.attrs.update({
                'data-ng-model': 'username',
                'class': 'form-control',
                'required': 'required',
            })
        self.fields['email'].widget.attrs.update({
            'data-ng-model': 'email',
            'class': 'form-control',
            'required': 'required',
        })
