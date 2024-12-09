from app.config.env_vars import EnvVars
from app.clients.github_api import GithubCollector


def test_github_collector():
    collector = GithubCollector(EnvVars().github_token, EnvVars().github_repo)
    pulls = collector._get_pulls()
    for pull in pulls:
        print(pull)