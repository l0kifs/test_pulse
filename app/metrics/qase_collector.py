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
        self.headers = {
            'Token': self.api_token,
            'Content-Type': 'application/json'
        }

    def _get_test_run_results(
            self,
            max_results: int = 10,
            start_result: int = 0
    ) -> dict:
        url = f'{self.base_url}/v1/result/{self.project_code}'
        params = {
            "limit": str(max_results),
            "offset": str(start_result)
        }
        response = requests.get(
            url=url, 
            headers=self.headers, 
            params=params
        )
        response.raise_for_status()
        data = response.json()
        return data
    
    def _get_test_cases(
        self,
        type: str | None = None,
        status: str | None = None,
        automation: str | None = None,
        max_results: int = 10,
        start_result: int = 0
    ) -> dict:
        url = f'{self.base_url}/v1/case/{self.project_code}'
        params = {
            "limit": str(max_results),
            "offset": str(start_result)
        }
        if type:
            params['type'] = type
        if status:
            params['status'] = status
        if automation:
            params['automation'] = automation
        response = requests.get(
            url=url, 
            headers=self.headers, 
            params=params
        )
        response.raise_for_status()
        data = response.json()
        return data
    
    def get_number_of_test_cases(
        self,
        type: str | None = None,
        status: str | None = None,
        automation: str | None = None
    ) -> int:
        data = self._get_test_cases(
            max_results=1, 
            type=type,
            status=status, 
            automation=automation
        )
        return data['result']['filtered']
