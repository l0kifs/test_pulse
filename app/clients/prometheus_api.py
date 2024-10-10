import requests


class PrometheusAPI:
    def __init__(self, url: str):
        self.url = url

    def get_metrics(self, query: str) -> dict:
        response = requests.get(f"{self.url}/api/v1/query", params={"query": query})
        return response.json()
