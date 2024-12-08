import requests


class PrometheusAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_metrics(self, query: str) -> dict:
        response = requests.get(f"{self.base_url}/api/v1/query", params={"query": query})
        return response.json()
