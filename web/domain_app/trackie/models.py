import uuid

import django.db.models as db_models
import django.contrib.auth as contrib_auth


class Organizator(contrib_auth.models.User):
    
    api_key = db_models.UUIDField(
        default  = uuid.uuid4,
        editable = False
    )