import logging
from typing import Any, Iterable
from datetime import timedelta
import enum
import httpx


class Source(enum.StrEnum):
    WHATSAPP = "whatsapp"
    WEBSITE = "website"

    @classmethod
    def is_valid(cls, source: str) -> bool:
        return source.upper() in cls.__members__


class AppointmentStatus(enum.StrEnum):
    SCHEDULED = "agendado"
    CONFIRMED = "confirmado"
    CANCELLED = "cancelado"
    COMPLETED = "concluído"

    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status.upper() in cls.__members__
    

class BusinessCategory(enum.StrEnum):
    C1 = "clínica médica"
    C2 = "clínica de psicologia"
    C3 = "clínica de estética"
    C4 = "clínica odontológica"
    C5 = "salão de beleza"
    C6 = "clínica de nutrição"
    C7 = "estúdio de arquitetura"

    @classmethod
    def is_valid(cls, category: str) -> bool:
        return category.upper() in cls.__members__


def fetch_cities() -> Iterable[dict[str, Any]]:
    logger = logging.getLogger(__name__)
    logger.info("Fetching Brazilian cities from IBGE...")
    client = httpx.Client(http2=True)
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response: httpx.Response = client.get(url)
    response.raise_for_status()
    logger.info(f"Successfully fetched {len(response.json())} cities from IBGE")
    return response.json()


def standardize_numeric_string(value: str) -> str:
    """
    Standardize a numeric string by removing
    non-numeric characters
    """
    return "".join(filter(str.isdigit, value))


def standardize_email(email: str) -> str:
    """
    Standardize an email address by removing spaces
    and converting to lowercase
    """
    return email.replace(" ", "").lower()


def timedelta_to_string(td: timedelta) -> str:
    """
    Convert a timedelta to a string in the format "HH:MM:SS"
    """
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
