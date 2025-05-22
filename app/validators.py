import re
from .utils import Source, AppointmentStatus, BusinessCategory
from zoneinfo import ZoneInfo
from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError


def validate_cpf(cpf: str) -> None:
    """
    Validates if the CPF is valid.
    """
    # Remove all non-numeric characters
    cpf: str = re.sub(r'\D', '', cpf)

    # Check if it has 11 digits or all digits aren't equal
    if len(cpf) != 11:
        raise ValidationError("Invalid CPF! It must have 11 digits.")
    
    if cpf == cpf[0] * 11:
        raise ValidationError("Invalid CPF! All digits are the same.")

    # Validation of the verifier digits
    for i in range(9, 11):
        _sum = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digit = ((_sum * 10) % 11) % 10
        if digit != int(cpf[i]):
            raise ValidationError("Invalid CPF! Verifier digits are invalid.")


def validate_date(date: date) -> None:
    """
    Validates if the date is not in the past.
    """
    sp_tz = ZoneInfo('America/Sao_Paulo')
    now = datetime.now(tz=sp_tz)
    if date < now.date():
        raise ValidationError(
            'The date cannot be in the past. Got: %(value)s, Actual: %(actual)s',
            params={'value': date, 'actual': now.date()}
        )
    

def validate_datetime(_datetime: datetime) -> None:
    """
    Validates if the datetime is not in the past.
    """
    sp_tz = ZoneInfo('America/Sao_Paulo')
    now = datetime.now(tz=sp_tz)
    if _datetime < now:
        raise ValidationError(
            'The datetime cannot be in the past. Got: %(value)s, Actual: %(actual)s',
            params={'value': _datetime, 'actual': now}
        )


def validate_price(price: float) -> None:
    """
    Validates if the price is greater than or equal to 0.
    """
    if price < 0:
        raise ValidationError(
            'The price must be greater than or equal to 0. Got: %(value)s',
            params={'value': price}
        )
    

def validate_duration(duration: timedelta) -> None:
    """
    Validates if the duration is greater than or equal to 60 seconds.
    """
    if duration < timedelta(seconds=60):
        raise ValidationError(
            'The duration must be greater or equal to 1 minute. Got: %(value)s',
            params={'value': duration}
        )


def validate_source(source: str) -> None:
    """
    Validates if the source is valid.
    """
    if not Source.is_valid(source):
        raise ValidationError(
            'The source must be one of the following: %(choices)s. Got: %(value)s',
            params={'choices': [source.name for source in Source], 'value': source}
        )


def validate_status(status: str) -> None:
    """
    Validates if the status is valid.
    """
    if not AppointmentStatus.is_valid(status):
        raise ValidationError(
            'The status must be one of the following: %(choices)s. Got: %(value)s',
            params={'choices': [status.name for status in AppointmentStatus], 'value': status}
        )
    

def validate_business_category(category: str) -> None:
    """
    Validates if the business category is valid.
    """
    if not BusinessCategory.is_valid(category):
        raise ValidationError(
            'The category must be one of the following: %(choices)s. Got: %(value)s',
            params={'choices': [category.name for category in BusinessCategory], 'value': category}
        )


def validate_phone_number(value):
    """
    Validates Brazilian phone numbers in the format DDD + number.
    Accepts 10 or 11 digits (with or without mask).
    """
    # Remove non-numeric characters
    phone = re.sub(r'\D', '', str(value))

    if len(phone) not in [10, 11]:
        raise ValidationError('Phone number must have 10 or 11 digits.')

    # Basic DDD validation (optional, can be removed)
    ddd = phone[:2]
    if not ddd.isdigit() or int(ddd) < 11 or int(ddd) > 99:
        raise ValidationError('Invalid area code (DDD).')

    # Number start validation (9 for mobile, 2-5 for landline)
    if len(phone) == 11 and not phone[2] == '9':
        raise ValidationError('Mobile numbers must start with 9 after the area code.')
    if len(phone) == 10 and not phone[2] in '2345':
        raise ValidationError('Landline numbers must start with 2, 3, 4, or 5 after the area code.')

