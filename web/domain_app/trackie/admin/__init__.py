""" Automatic registration of models """

import inspect

from django.contrib.admin.options import BaseModelAdmin
import django.contrib.admin.sites as contrib_admin

from . import models as trackie_admin_models

to_add_models = []  # pylint: disable=invalid-name

for attr in dir(trackie_admin_models):
    cls = getattr(trackie_admin_models, attr)
    if inspect.isclass(cls) and issubclass(cls, BaseModelAdmin):
        to_add_models.append(cls)

for admin_model in to_add_models:
    if admin_model.model not in contrib_admin.site._registry:
        contrib_admin.site.register(
            admin_model.model,
            admin_model
        )
