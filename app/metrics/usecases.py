from datetime import datetime
import logging

from clients.jira_api import StatusCategory, JiraAPI
from clients.jira_api import CustomField as JiraCustomField
from clients.qase_api import QaseAPI
from clients.qase_api import CustomField as QaseCustomField


class Usecases:
    def __init__(
        self, 
        qase_api: QaseAPI | None = None, 
        jira_api: JiraAPI | None = None, 
    ):
        self._log = logging.getLogger(__name__)
        
        self._qase_api = qase_api
        self._jira_api = jira_api
    
    def get_qase_test_url(
        self, 
        qase_url: str,
        qase_project_code: str,
        test_id: int
    ) -> str:
        qase_url = f'{qase_url}/case/{qase_project_code}-{str(test_id)}'
        return qase_url

    def get_jira_task_url(
        self, 
        jira_url: str,
        task_key: str
    ) -> str:
        jira_url = f'{jira_url}/browse/{task_key}'
        return jira_url
    
    def get_smoke_tests(
        self, 
        automated: bool
    ) -> int:
        automation = 'automated' if automated else 'is-not-automated,to-be-automated'
        tests = self._qase_api.get_all_test_cases(
            type='smoke', 
            status='actual',
            automation=automation
        )
        return tests

    def get_all_finished_new_test_tasks(self):
        jql = 'labels in (automation) AND labels in (new_test) AND labels in (smoke) AND status = Done AND resolution = Done'
        issues = self._jira_api.get_all_issues(jql)
        return issues
        
    def get_automation_tasks_for_tests(self, tests: list) -> list:
        automation_task_keys = []
        for test in tests:
            automation_task_url = QaseCustomField.AUTOMATION_TASK.get_value(test)
            if not automation_task_url:
                print(f'No AUTOMATION_TASK for {self.get_qase_test_url(test["id"])}')
                continue
            automation_task_keys.append(automation_task_url.split('/')[-1])
        automation_tasks = self._jira_api.get_all_issues(f'key in ({",".join(automation_task_keys)})')
        return automation_tasks

    def find_automation_tasks_without_required_labels(self):
        smoke_tests = self._qase_api.get_all_test_cases(
            type='smoke', 
            status='actual'
        )
        for test in smoke_tests:
            if not QaseCustomField.AUTOMATION_TASK.get_value(test):
                # print(f'Empty AUTOMATION_TASK {test["id"]}')
                continue
            automation_task_key = QaseCustomField.AUTOMATION_TASK.get_value(test).split('/')[-1]
            jira_task_labels = self._jira_api.get_issue(automation_task_key)['fields']['labels']
            if not all(label in jira_task_labels for label in ['automation', 'new_test', 'smoke']):
                print(f'No required labels {automation_task_key}. Labels: {jira_task_labels}')

    def get_due_date_status_change_diff_days(
        self,
        jira_issue: dict, 
        status_category: StatusCategory
    ) -> int:
        if jira_issue['fields']['status']['statusCategory']['id'] != status_category.value:
            raise Exception(f'Issue status category is not {status_category.name}')
        if jira_issue['fields']['duedate'] is None:
            raise Exception('Issue has no due date')
        due_date = datetime.fromisoformat(jira_issue['fields']['duedate']).replace(tzinfo=None)
        status_change_date = datetime.fromisoformat(jira_issue['fields']['statuscategorychangedate']).replace(tzinfo=None)
        days_diff = (due_date - status_change_date).days
        return days_diff

    def get_jira_issue_changelog(
        self,
        issue_key: str, 
        field: str
    ) -> list:
        issue_changes = self._jira_api.get_changelogs(issue_key)
        filtered_changes = []
        for value in issue_changes['values']:
            for item in value['items']:
                if item['field'] == field:
                    filtered_changes.append(value)
        return filtered_changes

    def get_total_manual_execution_time_for_tests(
        self, 
        tests: list
    ) -> float:
        """Get total execution time for tests in hours

        Args:
            tests (list): list of test cases from Qase API

        Returns:
            float: total execution time in hours
        """
        total_execution_time = 0
        for test in tests:
            execution_time = QaseCustomField.MANUAL_EXECUTION_TIME.get_value(test)
            if not execution_time:
                self._log.warning(f'Test case {test["id"]} does not have manual execution time')
                continue
            total_execution_time += int(execution_time) / 60
        total_execution_time = round(total_execution_time, 1)
        return total_execution_time