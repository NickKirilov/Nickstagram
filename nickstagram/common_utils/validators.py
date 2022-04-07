import re
from datetime import date
from dateutil import relativedelta
from django.core.exceptions import ValidationError


def validate_date_of_birth(value):
    datetime1 = value
    datetime2 = date.today()

    time_difference = relativedelta.relativedelta(datetime2, datetime1)
    difference_in_years = time_difference.years
    if difference_in_years < 18:
        raise ValidationError('You must be at least 18 years old!')
    return None


def file_max_size_validator(value):
    file_size = value.file.size
    if file_size > 5 * 1024 * 1024:
        raise ValidationError('Max file size is 5 MB.')
    return None


def validate_first_name(value):
    first_name_error_pattern_message = 'The first name must contains only letters.'

    for ch in value:
        if not ch.isalpha():
            raise ValidationError(first_name_error_pattern_message)


def validate_last_name(value):
    pattern = r'[A-Za-z]+'
    last_name_error_pattern_message = 'The last name must contains only letters.'

    matches = re.findall(pattern, value)
    if len(matches) != 1:
        raise ValidationError(last_name_error_pattern_message)


class ValidatePassword:
    @staticmethod
    def validate(password, *args, **kwargs):
        must_have_upper = True
        must_have_lower = True
        for ch in password:
            if ch.isalpha() and ch.islower():
                must_have_lower = False
            if ch.isalpha() and ch.isupper():
                must_have_upper = False
        if password.isalpha():
            raise ValidationError("Password must not consists only of letters.")
        if must_have_lower:
            raise ValidationError("Password must contain at least one lower letter.")
        if must_have_upper:
            raise ValidationError("Password must contain at least one upper letter.")

    @staticmethod
    def get_help_text():
        return "Your password can't be entirely alphabetical."
