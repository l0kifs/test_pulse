import json

import requests
from requests.auth import HTTPBasicAuth

# Jira API documentation: https://developer.atlassian.com/cloud/jira/platform/rest/v2/


class JiraCollector:
    def __init__(
        self,
        base_url: str,
        email: str,
        api_token: str
    ):
        self.base_url = base_url
        self.email = email
        self._auth = HTTPBasicAuth(email, api_token)

    def _get_issues(
        self,
        jql: str,
        max_results: int = 15,
        start_at: int = 0,
        fields: list[str] = None
    ):
        url = f'{self.base_url}/rest/api/2/search'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        payload = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": start_at
        }
        if fields:
            payload['fields'] = fields
        response = requests.post(url, headers=headers, data=json.dumps(payload), auth=self._auth)
        response.raise_for_status()
        data = response.json()
        return data

    def _get_total_issues(self, jql: str) -> int:
        return self._get_issues(jql, max_results=0)['total']

    def _get_all_issues(
        self,
        jql: str,
        fields: list[str] = None
    ):
        total = self._get_total_issues(jql)
        results_per_page = 50
        issues = []
        for start_at in range(0, total, results_per_page):
            issues.extend(self._get_issues(jql, results_per_page, start_at, fields)['issues'])
        return issues
