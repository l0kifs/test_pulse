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
    ):
        url = f'{self.base_url}/v1/result/{self.project_code}'
        params = {
            "limit": max_results,
            "offset": start_result
        }
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    
    def _get_test_cases(
        self,
        type: str | None = None,
        status: str | None = None,
        max_results: int = 10,
        start_result: int = 0
    ):
        url = f'{self.base_url}/v1/case/{self.project_code}'
        params = {
            "limit": max_results,
            "offset": start_result
        }
        if type:
            params['type'] = type
        if status:
            params['status'] = status
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data
    
    

# class QaseCollectorDemo:
#     def __init__(self, base_url, api_token, project_code):
#         self.base_url = base_url
#         self.api_token = api_token
#         self.project_code = project_code
#         self.headers = {
#             'Token': self.api_token,
#             'Content-Type': 'application/json'
#         }

#     def get_test_cases(self):
#         """Fetch all test cases for the project."""
#         url = f'{self.base_url}/case/{self.project_code}'
#         response = requests.get(url, headers=self.headers)
#         response.raise_for_status()
#         return response.json()['result']['cases']

#     def filter_smoke_cases(self, cases):
#         """Filter test cases with type 'smoke'."""
#         smoke_cases = [case for case in cases if case.get('type') == 'smoke']
#         return smoke_cases

#     def get_smoke_cases_creation_or_change(self):
#         """Get cases that are newly created as 'smoke' or changed to 'smoke'."""
#         cases = self.get_test_cases()
#         smoke_cases = self.filter_smoke_cases(cases)
#         # Additional logic to filter for recently created or changed cases would go here
#         return smoke_cases

#     def get_smoke_cases_transitioned_to_automated(self):
#         """Get cases transitioned from manual to automated with smoke type."""
#         cases = self.get_test_cases()
#         automated_smoke_cases = []
#         for case in cases:
#             if case.get('type') == 'smoke' and case.get('status') == 'automated' and case.get('previous_status') == 'manual':
#                 automated_smoke_cases.append(case)
#         return automated_smoke_cases

#     def count_smoke_cases_by_user(self):
#         """Count smoke cases transitioned to automated by the user who changed them."""
#         automated_smoke_cases = self.get_smoke_cases_transitioned_to_automated()
#         user_case_count = {}
#         for case in automated_smoke_cases:
#             user = case.get('updated_by', 'Unknown')
#             if user not in user_case_count:
#                 user_case_count[user] = 0
#             user_case_count[user] += 1
#         return user_case_count
