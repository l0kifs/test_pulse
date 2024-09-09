from datetime import datetime

from app.config.env_vars import EnvVars
from app.metrics.github_collector import GithubCollector


def test_github_collector():
    collector = GithubCollector(EnvVars().github_token, EnvVars().github_repo)
    pulls = collector._get_pulls()
    for pull in pulls:
        print(pull)