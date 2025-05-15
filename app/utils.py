import httpx
import logging
from typing import Any, Iterable
from django.core.exceptions import ValidationError



def fetch_cities() -> Iterable[dict[str, Any]]:
    logger = logging.getLogger(__name__)
    logger.info("Fetching Brazilian cities from IBGE...")
    client = httpx.Client(http2=True)
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response: httpx.Response = client.get(url)
    response.raise_for_status()
    logger.info(f"Successfully fetched {len(response.json())} cities from IBGE")
    return response.json()


def validate_cpf(cpf: str) -> None:
    import re
    # Remove all non-numeric characters
    cpf: str = re.sub(r'\D', '', cpf)

    # Check if it has 11 digits or all digits aren't equal
    if len(cpf) != 11:
        raise ValidationError("Invalid CPF! It must have 11 digits.")
    
    if cpf == cpf[0] * 11:
        raise ValidationError("Invalid CPF! All digits are the same.")

    # Validation of the verifier digits
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            raise ValidationError("Invalid CPF! Verifier digits are invalid.")
    return


def standardize_numeric_string(value: str) -> str:
    return "".join(filter(str.isdigit, value))


def standardize_email(email: str) -> str:
    return email.replace(" ", "").lower()
