from django.core.exceptions import ValidationError


def validate_school_email(value):
    if not ".edu" in value:
        raise ValidationError("A valid school email must be entered in")
    else:
        return value
