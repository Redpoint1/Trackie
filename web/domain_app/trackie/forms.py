from django.forms.models import ModelForm
from allauth.account.forms import SignupForm, UserForm
import allauth.account.app_settings as app_settings
from .models import Track


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


class ProfileForm(UserForm):

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)


class TrackCreateForm(ModelForm):
    class Meta:
        model = Track
        exclude = ["owner"]

    def __init__(self, *args, **kwargs):
        super(TrackCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'data-ng-model': 'trackForm.data.name',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['file'].widget.attrs.update({
            'data-ng-model': 'trackForm.data.file',
            'data-valid-file': '',
            'data-base-sixty-four-input': '',
        })
        self.fields['public'].widget.attrs.update({
            'data-ng-model': 'trackForm.data.public',
        })


class TrackUpdateForm(TrackCreateForm):
    class Meta(TrackCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super(TrackUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('file')
