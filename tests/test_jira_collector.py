import json

from app.config.env_vars import EnvVars
from app.metrics.jira_collector import JiraCollector


def test_jira_collector():
    collector = JiraCollector('https://mercuryo.atlassian.net/', EnvVars().jira_email, EnvVars().jira_api_token)
    issues = collector._get_issues('project = MRC', max_results=0)
    print(json.dumps(issues, indent=4))
