from django.forms.models import ModelForm
from allauth.account.forms import SignupForm, UserForm
import allauth.account.app_settings as app_settings
from .models import Track, Racer, Tournament, RaceType, Race


class RegisterForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
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
            'data-ng-change': 'trackPreview()',
            'accept': '.gpx, .GPX',
            'required': '',
            'data-maxsize': 512,
            'data-do-not-parse-if-oversize': '',
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


class RacerCreateForm(ModelForm):
    class Meta:
        model = Racer
        exclude = ("full_name",)

    def __init__(self, *args, **kwargs):
        super(RacerCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'data-ng-model': 'racerForm.data.first_name',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['last_name'].widget.attrs.update({
            'data-ng-model': 'racerForm.data.last_name',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['photo'].widget.attrs.update({
            'data-ng-model': 'racerForm.data.photo',
            'data-valid-file': '',
            'data-base-sixty-four-input': '',
            'accept': 'image/jpeg, image/jpg, image/png',
            'data-maxsize': 512,
        })
        self.fields['about'].widget.attrs.update({
            'data-ng-model': 'racerForm.data.about',
            'class': 'form-control',
        })


class RacerUpdateForm(RacerCreateForm):
    class Meta(RacerCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super(RacerUpdateForm, self).__init__(*args, **kwargs)


class TournamentCreateForm(ModelForm):
    class Meta:
        model = Tournament
        exclude = ("owner",)

    def __init__(self, *args, **kwargs):
        super(TournamentCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'data-ng-model': 'tournamentForm.data.name',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['sport'].widget.attrs.update({
            'data-ng-model': 'tournamentForm.data.sport',
            'class': 'form-control',
            'required': 'required',
        })


class TournamentUpdateForm(TournamentCreateForm):
    class Meta(TournamentCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super(TournamentUpdateForm, self).__init__(*args, **kwargs)


class RaceTypeCreateForm(ModelForm):
    class Meta:
        model = RaceType
        exclude = ("owner", "public")

    def __init__(self, *args, **kwargs):
        super(RaceTypeCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'data-ng-model': 'typeForm.data.name',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['fields'].widget.attrs.update({
            'data-ng-model': 'typeForm.data.fields',
            'class': 'form-control',
            'required': 'required',
        })


class RaceTypeUpdateForm(RaceTypeCreateForm):
    class Meta(RaceTypeCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super(RaceTypeUpdateForm, self).__init__(*args, **kwargs)


class RaceCreateForm(ModelForm):
    class Meta:
        model = Race
        exclude = ("end", "real_end", "real_start", "participants",)

    def __init__(self, *args, **kwargs):
        super(RaceCreateForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'data-ng-model': 'raceForm.data.name',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['tournament'].widget.attrs.update({
            'data-ng-model': 'raceForm.data.tournament',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['track'].widget.attrs.update({
            'data-ng-model': 'raceForm.data.track',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['projection'].widget.attrs.update({
            'data-ng-model': 'raceForm.data.projection',
            'class': 'form-control',
        })
        self.fields['type'].widget.attrs.update({
            'data-ng-model': 'raceForm.data.type',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['start'].widget.attrs.update({
            'data-ng-model': 'raceForm.data.start',
            'class': 'form-control',
            'required': 'required',
        })
        self.fields['estimated_duration'].widget.attrs.update({
            'data-ng-model': 'raceForm.data.estimated_duration',
            'pattern': '(0[0-9]|1[0-9]|2[0-3])(:[0-5][0-9]){2}',
            'class': 'form-control',
        })


class RaceUpdateForm(RaceCreateForm):
    class Meta(RaceCreateForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super(RaceUpdateForm, self).__init__(*args, **kwargs)
