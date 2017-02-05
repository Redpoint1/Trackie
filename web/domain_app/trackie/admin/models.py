""" DB models for administration """

import django.contrib.admin as contrib_admin

from .. import models as trackie_models


class TournamentAdmin(contrib_admin.ModelAdmin):
    """  Tournament """
    model = trackie_models.Tournament


class ParticipantsInline(contrib_admin.TabularInline):
    model = trackie_models.RacerInRace
    extra = 2 # how many rows to show


class RaceAdmin(contrib_admin.ModelAdmin):
    """ Race """
    model = trackie_models.Race
    inlines = (ParticipantsInline,)


class RaceTypeAdmin(contrib_admin.ModelAdmin):
    """ Race type """
    model = trackie_models.RaceType


class SportTypeAdmin(contrib_admin.ModelAdmin):
    """ Sport type """
    model = trackie_models.SportType


class TrackAdmin(contrib_admin.ModelAdmin):
    """ Track """
    model = trackie_models.Track


class RacerAdmin(contrib_admin.ModelAdmin):
    """ Racer """
    model = trackie_models.Racer
