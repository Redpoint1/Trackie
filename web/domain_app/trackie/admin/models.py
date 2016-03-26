""" DB models for administration """

import django.contrib.admin as contrib_admin

from .. import models as trackie_models


class TournamentAdmin(contrib_admin.ModelAdmin):
    """  Tournament """
    model = trackie_models.Tournament


class RaceAdmin(contrib_admin.ModelAdmin):
    """ Race """
    model = trackie_models.Race


class RaceTypeAdmin(contrib_admin.ModelAdmin):
    """ Race tyoe """
    model = trackie_models.RaceType


class SportTypeAdmin(contrib_admin.ModelAdmin):
    """ Sport type """
    model = trackie_models.SportType
