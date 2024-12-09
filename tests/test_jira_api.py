import json

from app.config.env_vars import EnvVars
from app.clients.jira_api import JiraAPI


def test_jira_collector():
    collector = JiraAPI(EnvVars().JIRA_URL, EnvVars().JIRA_EMAIL, EnvVars().JIRA_API_TOKEN)
    issues = collector._get_issues('project = MRC', max_results=0)
    print(json.dumps(issues, indent=4))
