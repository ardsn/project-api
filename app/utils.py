import httpx
from typing import Any, Iterable



def fetch_cities() -> Iterable[dict[str, Any]]:
    client = httpx.Client(http2=True)
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
    response: httpx.Response = client.get(url)
    response.raise_for_status()
    return response.json()