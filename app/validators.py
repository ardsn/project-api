import re
from zoneinfo import ZoneInfo
from datetime import datetime, date, timedelta, time
from django.core.exceptions import ValidationError


SP_TZ = ZoneInfo('America/Sao_Paulo')


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
    now = datetime.now(tz=SP_TZ)
    if date < now.date():
        raise ValidationError(
            'The date cannot be in the past. Got: %(value)s, Actual: %(actual)s',
            params={'value': date, 'actual': now.date()}
        )
    

def validate_datetime(_datetime: datetime) -> None:
    """
    Validates if the datetime is not in the past.
    """
    now = datetime.now(tz=SP_TZ)
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


def validate_birth_date(birth_date: date) -> None:
    """
    Checks if the birth date is valid.
    The date must be in the past and the person must be at most 120 years old.
    """
    today = datetime.now(tz=SP_TZ).date()
    
    # Check if the date is not in the future
    if birth_date > today:
        raise ValidationError(
            'The birth date cannot be in the future. Received: %(value)s, Actual: %(actual)s',
            params={'value': birth_date, 'actual': today}
        )
    
    # Calculate the approximate age
    age = (
        today.year
        - birth_date.year
        - (
            (today.month, today.day)
            <
            (birth_date.month, birth_date.day)
        )
    )
    
    # Check if the age is reasonable (maximum 120 years)
    if age > 120:
        raise ValidationError(
            'The age cannot be greater than 120 years. Calculated age: %(age)s years',
            params={'age': age}
        )
    

def validate_schedule(
    schedule: dict[str, dict[str, str | list[dict[str, str]]]]
) -> None:
    """
    Validates the schedule.

    Expected format:
    {
        '0': {  # Sunday (0) to Saturday (6)
            'start': '08:00:00',
            'end': '18:00:00',
            'breaks': [
                {'start': '12:00:00', 'end': '13:00:00'}
            ]
        },
        ...
    }
    """
    def _validate_time_format(time_str: str, field_name: str) -> time:
        """
        Validates the string time format and returns a time object.
        """
        try:
            return time.fromisoformat(time_str)
        except ValueError:
            raise ValidationError(f'Invalid time format for {field_name}. Must be in ISO 8601 format (HH:MM).')
    
    for day_key, day_schedule in schedule.items():
        # Validate day key (0-6)
        try:
            day_num = int(day_key)
        except ValueError:
            raise ValidationError(f'Invalid day key: {day_key}. Must be a number between 0 and 6.')
        
        if day_num < 0 or day_num > 6:
            raise ValidationError(f'Invalid day: {day_num}. Must be between 0 and 6.')
        
        # Validate day schedule structure
        if not isinstance(day_schedule, dict):
            raise ValidationError(f'Day schedule {day_key} must be a dictionary.')
        
        required_fields = ['start', 'end']
        for field in required_fields:
            if field not in day_schedule:
                raise ValidationError(f'Required field "{field}" missing for day {day_key}.')
        
        # Validate start and end times
        start_time = _validate_time_format(day_schedule['start'], f'start of day {day_key}')
        end_time = _validate_time_format(day_schedule['end'], f'end of day {day_key}')
        
        if start_time >= end_time:
            raise ValidationError(f'Start time must be before end time for day {day_key}.')
        
        # Validate breaks (optional)
        if 'breaks' in day_schedule:
            if not isinstance(day_schedule['breaks'], list):
                raise ValidationError(f'Breaks for day {day_key} must be a list.')
            
            for i, break_period in enumerate(day_schedule['breaks']):
                if not isinstance(break_period, dict):
                    raise ValidationError(f'Break {i} for day {day_key} must be a dictionary.')
                
                if 'start' not in break_period or 'end' not in break_period:
                    raise ValidationError(f'Break {i} for day {day_key} must have "start" and "end".')
                
                break_start = _validate_time_format(
                    break_period['start'], 
                    f'start of break {i} of day {day_key}'
                )
                break_end = _validate_time_format(
                    break_period['end'], 
                    f'end of break {i} of day {day_key}'
                )
                
                if break_start >= break_end:
                    raise ValidationError(
                        f'Start time of break {i} for day {day_key} must be before end time.'
                    )
                
                # Validate if the break is within the business hours
                if break_start < start_time or break_end > end_time:
                    raise ValidationError(
                        f'Break {i} for day {day_key} must be within the business hours.'
                    )
                
