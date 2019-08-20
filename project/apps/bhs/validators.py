# Standard Library
from datetime import date
from uuid import UUID

# Django
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import URLValidator
from phonenumber_field.validators import validate_international_phonenumber
from django.core.validators import validate_email as val_email

def validate_bhs_id(value):
    if not 0 < value < 999999:  # Your conditions here
        raise ValidationError(
            "Must be between 0 and 999999"
        )
    return value

def validate_birth_date(value):
    if not date(1900, 1, 1) < value < date(2015, 1, 1):  # Your conditions here
        raise ValidationError(
            "The birthdate must be reasonable."
        )
    return value

validate_tin = RegexValidator(
    r'(9\d{2})([ \-]?)([7]\d|8[0-8])([ \-]?)(\d{4})',
    message="""
        Must be a Taxpayer Idenfication Number
        in the form `XX-XXXXXXXX`.
    """,
)

validate_nopunctuation = RegexValidator(
    r'/[\p{L}]/ui',
    message="""
        Must not use punctuation.
    """,
)

def validate_url(value):
    validator = URLValidator()
    try:
        validator(value)
    except ValidationError:
        return ''
    return value.lower()

def validate_uuid(value):
    try:
        UUID(value, version=4)
    except ValueError as e:
        raise e

def validate_phone(value):
    try:
        validate_international_phonenumber(value)
    except ValidationError:
        return ""
    return value


def validate_email(value):
    try:
        val_email(value)
    except ValidationError:
        return ""
    return value.lower()