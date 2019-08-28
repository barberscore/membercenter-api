import os
from django.utils.deconstruct import deconstructible
from django.db.models import EmailField
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

@deconstructible
class ImageUploadPath():

    def __init__(self, name):
        self.name = name

    def __call__(self, instance, filename):
        return os.path.join(
            instance._meta.app_label,
            instance._meta.model_name,
            self.name,
            str(instance.id),
        )

class LowerEmailField(EmailField):
    def from_db_value(self, value, expression, connection):
        try:
            validate_email(value)
        except ValidationError:
            return None
        return value.lower()

