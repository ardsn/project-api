import httpx
import logging
from typing import Any, Iterable

logger = logging.getLogger(__name__)

def fetch_cities() -> Iterable[dict[str, Any]]:
    logger.info("Fetching Brazilian cities from IBGE...")
    client = httpx.Client(http2=True)
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response: httpx.Response = client.get(url)
    response.raise_for_status()
    logger.info(f"Successfully fetched {len(response.json())} cities from IBGE")
    return response.json()