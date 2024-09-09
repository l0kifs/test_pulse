import requests

# Qase API documentation: https://developers.qase.io/reference/


class QaseCollector:
    def __init__(
        self,
        base_url: str,
        api_token: str,
        project_code: str
    ):
        self.base_url = base_url
        self.api_token = api_token
        self.project_code = project_code

    def _get_test_run_results(
            self,
            max_results: int = 10,
            start_at: int = 0
    ):
        url = f'{self.base_url}/v1/result/{self.project_code}'
        headers = {
            'Accept': 'application/json',
            'Token': self.api_token
        }
        params = {
            "limit": max_results,
            "offset": start_at
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data