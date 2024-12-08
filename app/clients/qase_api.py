from enum import Enum
import logging
import requests

# Qase API documentation: https://developers.qase.io/reference/


class CustomField(Enum):
    AUTOMATION_TASK = 5
    MANUAL_EXECUTION_TIME = 6
    
    def get_value(self, test_case: dict) -> str:
        for custom_field in test_case['custom_fields']:
            if custom_field['id'] == self.value:
                return custom_field['value']
        return ''
    

class AutomationStatus(Enum):
    MANUAL = 0
    AUTOMATED = 2
    


class QaseAPI:
    def __init__(
        self,
        base_url: str,
        api_token: str,
        project_code: str
    ):
        self._log = logging.getLogger(__name__)
        self._base_url = base_url
        self._api_token = api_token
        self._project_code = project_code
        self._headers = {
            'Token': self._api_token,
            'Content-Type': 'application/json'
        }

    def _get_test_run_results(
            self,
            max_results: int = 10,
            start_result: int = 0
    ) -> dict:
        url = f'{self._base_url}/v1/result/{self._project_code}'
        params = {
            "limit": str(max_results),
            "offset": str(start_result)
        }
        response = requests.get(
            url=url, 
            headers=self._headers, 
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
        url = f'{self._base_url}/v1/case/{self._project_code}'
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
            headers=self._headers, 
            params=params
        )
        response.raise_for_status()
        data = response.json()
        return data
    
    def get_all_test_cases(
        self,
        type: str | None = None,
        status: str | None = None,
        automation: str | None = None,
    ) -> list:
        max_results = 100
        start_result = 0
        number_of_test_cases = self.get_number_of_test_cases(
            type=type,
            status=status,
            automation=automation
        )
        all_test_cases = []
        while start_result < number_of_test_cases:
            data = self._get_test_cases(
                type=type,
                status=status,
                automation=automation,
                max_results=max_results,
                start_result=start_result
            )
            all_test_cases += data['result']['entities']
            start_result += max_results
        return all_test_cases
    
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
    
    def get_test_case(
        self,
        case_id: int
    ) -> dict:
        url = f'{self._base_url}/v1/case/{self._project_code}/{case_id}'
        response = requests.get(
            url=url, 
            headers=self._headers
        )
        response.raise_for_status()
        return response.json()['result']
    
    def update_test_case(
        self,
        case_id: int,
        custom_fields: dict[CustomField, str]
    ) -> dict:
        url = f'{self._base_url}/v1/case/{self._project_code}/{case_id}'
        payload = {}
        if custom_fields:
            payload['custom_field'] = {
                str(custom_field.value): value
                for custom_field, value in custom_fields.items()
            }
        response = requests.patch(
            url=url, 
            headers=self._headers, 
            json=payload
        )
        response.raise_for_status()
        return response.json()
