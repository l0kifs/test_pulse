from datetime import datetime
from clients.jira_api import JiraAPI, Status, StatusCategory
from clients.qase_api import CustomField, QaseAPI
from config.env_vars import EnvVars
from usecases import Usecases


qase_api = QaseAPI(
    base_url=EnvVars().QASE_URL,
    api_token=EnvVars().QASE_API_TOKEN,
    project_code=EnvVars().QASE_PROJECT_CODE
)
jira_api = JiraAPI(
    base_url=EnvVars().JIRA_URL, 
    email=EnvVars().JIRA_EMAIL, 
    api_token=EnvVars().JIRA_API_TOKEN
)
usecases = Usecases(qase_api=qase_api, jira_api=jira_api)


def get_number_of_smoke_tests(automated: bool) -> int:
    smoke_tests = usecases.get_smoke_tests(automated)
    number_of_tests = len(smoke_tests)
    return number_of_tests


def get_total_manual_execution_time_for_smoke_tests(automated: bool) -> float:
    """Get total manual execution time for current smoke tests in hours"""
    smoke_tests = usecases.get_smoke_tests(automated)
    total_execution_time = usecases.get_total_manual_execution_time_for_tests(smoke_tests)
    return total_execution_time


def get_total_manual_execution_time_for_blocked_manual_smoke_tests() -> float:
    smoke_manual_tests = usecases.get_smoke_tests(automated=False)
    automation_tasks = usecases.get_automation_tasks_for_tests(smoke_manual_tests)
    blocked_tests = []
    for task in automation_tasks:
        if task['fields']['status']['id'] == Status.DEVELOPMENT_BLOCKED.value:
            blocked_tests.append(next(test for test in smoke_manual_tests if CustomField.AUTOMATION_TASK.get_value(test) == usecases.get_jira_task_url(task['key'])))
    total_execution_time = usecases.get_total_manual_execution_time_for_tests(blocked_tests)
    return total_execution_time


def get_number_of_blocked_manual_smoke_tests() -> int:
    smoke_manual_tests = usecases.get_smoke_tests(automated=False)
    automation_tasks = usecases.get_automation_tasks_for_tests(smoke_manual_tests)
    blocked_tests = []
    for task in automation_tasks:
        if task['fields']['status']['id'] == Status.DEVELOPMENT_BLOCKED.value:
            blocked_tests.append(next(test for test in smoke_manual_tests if CustomField.AUTOMATION_TASK.get_value(test) == usecases.get_jira_task_url(task['key'])))
    number_of_tests = len(blocked_tests)
    return number_of_tests


def get_total_manual_execution_time_for_tests_without_automation_task() -> float:
    """Get total execution time for current manual smoke tests without automation task in hours"""
    smoke_manual_tests = usecases.get_smoke_tests(automated=False)
    tests_without_automation_task = []
    for test in smoke_manual_tests:
        if CustomField.AUTOMATION_TASK.get_value(test) == '':
            tests_without_automation_task.append(test)
    total_execution_time = usecases.get_total_manual_execution_time_for_tests(tests_without_automation_task)
    return total_execution_time


def get_number_of_tests_without_automation_task() -> int:
    """Get number of current smoke tests without automation task"""
    smoke_manual_tests = usecases.get_smoke_tests(automated=False)
    tests_without_automation_task = []
    for test in smoke_manual_tests:
        if CustomField.AUTOMATION_TASK.get_value(test) == '':
            tests_without_automation_task.append(test)
    number_of_tests = len(tests_without_automation_task)
    return number_of_tests


def get_smoke_automation_time_diff():
    issues = jira_api.get_all_issues(jql='labels IN (automation) AND labels IN (new_test) AND labels IN (smoke) AND statusCategory = Done')
    total_days_diff = 0
    total_expected_days = 0
    for issue in issues:
        if str(issue['fields']['status']['statusCategory']['id']) != StatusCategory.DONE.value:
            print(f'Issue {issue["key"]} status category is not id {StatusCategory.DONE.value} but {issue["fields"]["status"]["statusCategory"]["id"]}')
            continue
        if issue['fields']['duedate'] is None:
            print(f'Issue {issue["key"]} has no due date')
            continue
        due_date = datetime.fromisoformat(issue['fields']['duedate']).replace(tzinfo=None)
        status_change_date = datetime.fromisoformat(issue['fields']['statuscategorychangedate']).replace(tzinfo=None)
        difference_in_days = (due_date.date() - status_change_date.date()).days
        total_days_diff += difference_in_days
        
        changelog = usecases.get_jira_issue_changelog(issue['key'], 'status')
        def get_expected_automation_days():
            for change in changelog:
                for item in change['items']:
                    if item['field'] == 'status' and item['to'] == Status.IN_PROGRESS.value:
                        status_change_date = datetime.fromisoformat(change['created']).replace(tzinfo=None)
                        difference_in_days = (due_date.date() - status_change_date.date()).days + 1
                        return difference_in_days
        total_expected_days += get_expected_automation_days()
    return {
        'total_days_diff': total_days_diff,
        'total_expected_days': total_expected_days
    }
