from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields.json import JSONField

from oauth2client.django_orm import CredentialsField
from south.modelsinspector import add_introspection_rules


add_introspection_rules([], ['oauth2client.django_orm.CredentialsField'])


class DriveCredential(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    user_info = JSONField()
    credential = CredentialsField()
