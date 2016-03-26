import django.db.models as db_models
import django.contrib.auth.models as auth_model

from django.utils.translation import ugettext_lazy as _


class Tournament(db_models.Model):

    class Meta:
        verbose_name = _("Tournament")
        verbose_name_plural = _("Tournaments")

    name = db_models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of the Tournament")
    )

    owner = db_models.ForeignKey(
        auth_model.User,
        null=False,
        blank=False,
        on_delete=db_models.CASCADE,
        verbose_name=_("Owner"),
        help_text=_("Administrator of the Tournament"),
    )

    def __str__(self):
        return self.name


class RaceType(db_models.Model):

    class Meta:
        verbose_name = _("Race type")
        verbose_name_plural = _("Race types")

    type = db_models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=255,
        verbose_name=_("Type"),
        help_text=_("Type of the race")
    )

    icon = db_models.ImageField(
        upload_to="static/images/race/",
        null=True,
        blank=False,
        verbose_name=_("Icon"),
        help_text=_("Choose icon")
    )

    def __str__(self):
        return self.type


class SportType(db_models.Model):

    class Meta:
        verbose_name = _("Sport type")
        verbose_name_plural = _("Sport types")

    name = db_models.CharField(
        blank=False,
        null=False,
        unique=True,
        max_length=255,
        verbose_name=_("Sport name"),
        help_text=_("Name of the sport")
    )

    icon = db_models.ImageField(
        upload_to="static/images/sport/",
        null=True,
        blank=False,
        verbose_name=_("Icon"),
        help_text=_("Choose icon")
    )

    def __str__(self):
        return self.name


class Race(db_models.Model):

    class Meta:
        verbose_name = _("Race")
        verbose_name_plural = _("Races")

    name = db_models.CharField(
        null=False,
        blank=False,
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Name of the race")
    )

    tournament = db_models.ForeignKey(
        Tournament,
        null=False,
        blank=False,
        related_name="races",
        verbose_name=_("Tournament"),
        help_text=_("Select under which tournament is assigned")
    )

    type = db_models.ForeignKey(
        RaceType,
        null=True,
        blank=False,
        on_delete=db_models.SET_NULL,
        verbose_name=_("Type"),
        help_text=_("Determine race type")
    )

    def __str__(self):
        return self.name
