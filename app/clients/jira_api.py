from enum import Enum
import json
import logging

import requests
from requests.auth import HTTPBasicAuth

# Jira API documentation: https://developer.atlassian.com/cloud/jira/platform/rest/v2/


class IssueType(Enum):
    TASK = '10002'
    
class Priority(Enum):
    LOW = '4'
    MEDIUM = '3'
    HIGH = '2'
    HIGHEST = '10003'
    LOWEST = '10002'
    
class LinkType(Enum):
    BLOCKS = '10000'
    
class TransitionStatus(Enum):
    DEVELOPMENT_BLOCKED = '191'
    DONE = '181'
    
class StatusCategory(Enum):
    TO_DO = '2'
    IN_PROGRESS = '4'
    DONE = '3'
    
class Status(Enum):
    TO_DO = '10000'
    IN_PROGRESS = '3'
    REVIEW = '10118'
    DONE = '10001'
    DEVELOPMENT_BLOCKED = '10160'
    
class CustomField(Enum):
    STORY_POINTS = 'customfield_10021'
    TEST_CASE_KEY = 'customfield_10341'


class JiraAPI:
    def __init__(
        self,
        base_url: str,
        email: str,
        api_token: str
    ):
        self._log = logging.getLogger(__name__)
        self._base_url = base_url
        self._email = email
        self._auth = HTTPBasicAuth(email, api_token)
        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
    def get_issue(
        self,
        issue_key: str,
        fields: list[str] = None
    ):
        self._log.info(f"Fetching issue: {issue_key}")
        url = f'{self._base_url}/rest/api/2/issue/{issue_key}'
        params = {}
        if fields:
            params['fields'] = fields
        response = requests.get(
            url=url, 
            params=params,
            headers=self._headers,
            auth=self._auth
        )
        response.raise_for_status()
        data = response.json()
        return data

    def get_issues(
        self,
        jql: str,
        max_results: int = 15,
        start_at: int = 0,
        fields: list[str] = None
    ):
        self._log.info(f"Fetching issues: {jql}")
        url = f'{self._base_url}/rest/api/2/search'
        payload = {
            "jql": jql,
            "maxResults": max_results,
            "startAt": start_at
        }
        if fields:
            payload['fields'] = fields
        response = requests.post(
            url=url, 
            headers=self._headers, 
            data=json.dumps(payload), 
            auth=self._auth
        )
        response.raise_for_status()
        data = response.json()
        return data

    def get_total_issues(
        self, 
        jql: str
    ) -> int:
        self._log.info(f"Fetching total issues: {jql}")
        return self.get_issues(jql, max_results=0)['total']

    def get_all_issues(
        self,
        jql: str,
        fields: list[str] = None
    ):
        self._log.info(f"Fetching all issues: {jql}")
        total = self.get_total_issues(jql)
        results_per_page = 50
        issues = []
        for start_at in range(0, total, results_per_page):
            issues.extend(self.get_issues(jql, results_per_page, start_at, fields)['issues'])
        return issues
    
    def create_issue(
        self,
        project_key: str,
        issue_type: IssueType,
        summary: str,
        description: str | None = None,
        labels: list[str] | None = None,
        assignee_id: str | None = None,
        priority: Priority | None = None,
        custom_fields: dict[CustomField, any] | None = None
    ):
        self._log.info(f"Creating issue: {summary}")
        url = f'{self._base_url}/rest/api/2/issue'
        payload = {
            "fields": {
                "project": { "key": project_key },
                "issuetype": { "id": issue_type.value },
                "summary": summary,
            }
        }
        if description:
            payload['fields']['description'] = description
        if labels:
            payload['fields']['labels'] = labels
        if assignee_id:
            payload['fields']['assignee'] = { "id": assignee_id }
        if priority:
            payload['fields']['priority'] = { "id": priority.value }
        if custom_fields:
            payload['fields'].update({
                str(custom_field.value): value
                for custom_field, value in custom_fields.items()
            })
        response = requests.post(
            url=url, 
            headers=self._headers, 
            data=json.dumps(payload), 
            auth=self._auth
        )
        response.raise_for_status()
        data = response.json()
        return data
    
    def get_issue_watchers(
        self,
        issue_key: str
    ):
        self._log.info(f"Fetching watchers for issue: {issue_key}")
        url = f'{self._base_url}/rest/api/2/issue/{issue_key}/watchers'
        response = requests.get(
            url=url, 
            headers=self._headers,
            auth=self._auth
        )
        response.raise_for_status()
        data = response.json()
        return data

    def add_issue_watcher(
        self,
        issue_key: str,
        watcher_id: str
    ):
        """Add issue watcher.

        Args:
            issue_key (str): Issue key.
            watcher_id (str): User account ID.
        """
        self._log.info(f"Adding issue watcher: {watcher_id}")
        url = f'{self._base_url}/rest/api/2/issue/{issue_key}/watchers'
        response = requests.post(
            url=url, 
            headers=self._headers, 
            data=json.dumps(watcher_id), 
            auth=self._auth
        )
        response.raise_for_status()
        return
    
    def add_issue_link(
        self,
        link_type: LinkType,
        inward_issue_key: str,
        outward_issue_key: str
    ):
        """Add issue link between two issues.

        Args:
            link_type (LinkType): Type of link.
            inward_issue_key (str): Example: Shows "blocks".
            outward_issue_key (str): Example: Shows "is blocked by".
        """
        self._log.info(f"Adding issue link: inward:{inward_issue_key} outward:{outward_issue_key}")
        url = f'{self._base_url}/rest/api/2/issueLink'
        payload = {
            "type": { "id": link_type.value },
            "inwardIssue": { "key": inward_issue_key },
            "outwardIssue": { "key": outward_issue_key }
        }
        response = requests.post(
            url=url, 
            headers=self._headers, 
            data=json.dumps(payload), 
            auth=self._auth
        )
        response.raise_for_status()
        return
    
    def get_issue_transitions(
        self,
        issue_key: str
    ):
        self._log.info(f"Fetching issue transitions: {issue_key}")
        url = f'{self._base_url}/rest/api/2/issue/{issue_key}/transitions'
        response = requests.get(
            url=url, 
            headers=self._headers,
            auth=self._auth
        )
        response.raise_for_status()
        data = response.json()
        return data
    
    def transition_issue(
        self,
        issue_key: str,
        status: TransitionStatus
    ):
        self._log.info(f"Transiting issue to status: {issue_key} {status}")
        url = f'{self._base_url}/rest/api/2/issue/{issue_key}/transitions'
        payload = {
            "transition": { "id": status.value }
        }
        response = requests.post(
            url=url, 
            headers=self._headers, 
            data=json.dumps(payload), 
            auth=self._auth
        )
        response.raise_for_status()
        return
    
    def add_issue_comment(
        self,
        issue_key: str,
        comment: str
    ):
        self._log.info(f"Adding comment to issue: {issue_key}")
        url = f'{self._base_url}/rest/api/2/issue/{issue_key}/comment'
        payload = {
            "body": comment
        }
        response = requests.post(
            url=url, 
            headers=self._headers, 
            data=json.dumps(payload), 
            auth=self._auth
        )
        response.raise_for_status()
        return
    
    def edit_issue(
        self, 
        issue_key: str, 
        summary: str | None = None,
        description: str | None = None,
    ):
        self._log.info(f"Editing issue: {issue_key}")
        url = f'{self._base_url}/rest/api/2/issue/{issue_key}'
        payload = {'fields': {}}
        if summary:
            payload['fields']['summary'] = summary
        if description:
            payload['fields']['description'] = description
        response = requests.put(
            url=url, 
            headers=self._headers, 
            data=json.dumps(payload), 
            auth=self._auth
        )
        response.raise_for_status()
        return
    
    def get_bulk_editable_fields(
        self,
        issue_ids_or_keys: str
    ):
        self._log.info("Fetching bulk editable fields")
        url = f'{self._base_url}/rest/api/3/bulk/issues/fields'
        params = {
            'issueIdsOrKeys': issue_ids_or_keys
        }
        response = requests.get(
            url=url, 
            params=params,
            headers=self._headers,
            auth=self._auth
        )
        response.raise_for_status()
        data = response.json()
        return data
    
    def get_changelogs(
        self,
        issue_key: str
    ):
        self._log.info(f"Fetching changelogs for issue: {issue_key}")
        url = f'{self._base_url}/rest/api/2/issue/{issue_key}/changelog'
        response = requests.get(
            url=url, 
            headers=self._headers,
            auth=self._auth
        )
        response.raise_for_status()
        data = response.json()
        return data
        