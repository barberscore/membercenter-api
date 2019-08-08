# Standard Library
import os
import string
from datetime import date

# Third-Party
import phonenumbers
import pytz
import six
from rest_framework_json_api import serializers

# Django
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import EmailField
from django.utils.deconstruct import deconstructible


class ValidatedPhoneField(CharField):
    def from_db_value(self, value, expression, connection):
        try:
            value = phonenumbers.parse(value, 'US')
        except phonenumbers.NumberParseException:
            return ""
        return phonenumbers.format_number(value, phonenumbers.PhoneNumberFormat.E164)


class LowerEmailField(EmailField):
    def from_db_value(self, value, expression, connection):
        try:
            validate_email(value)
        except ValidationError:
            return None
        return value.lower()


class VoicePartField(CharField):
    def from_db_value(self, value, expression, connection):
        part_map = {
            'tenor': 'tenor',
            'lead': 'lead',
            'baritone': 'baritone',
            'bass': 'bass',
        }
        try:
            return part_map[value.lower().strip()]
        except AttributeError:
            return None
        except KeyError:
            return None



class ReasonableBirthDate(DateField):
    def from_db_value(self, value, expression, connection):
        if value == date(1900, 1, 1) or value == date(2018, 11, 13):
            return None
        return value



class GenderField(CharField):
    def from_db_value(self, value, expression, connection):
        gender_map = {
            'men': 'male',
            'women': 'female',
            'mixed': 'mixed',
        }
        try:
            return gender_map[value.lower()]
        except AttributeError:
            return None
        except KeyError:
            return None


@deconstructible
class ImageUploadPath(object):

    def __init__(self, name):
        self.name = name

    def __call__(self, instance, filename):
        return os.path.join(
            instance._meta.app_label,
            instance._meta.model_name,
            self.name,
            str(instance.id),
        )



class NoPunctuationCharField(CharField):
    def from_db_value(self, value, expression, connection):
        if not value:
            return ""
        return value.translate(
            value.maketrans('', '', '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~')
        ).strip()


class TimezoneField(serializers.Field):
    def to_representation(self, obj):
        return six.text_type(obj)

    def to_internal_value(self, data):
        try:
            return pytz.timezone(str(data))
        except pytz.exceptions.UnknownTimeZoneError:
            raise ValidationError('Unknown timezone')