from datetime import datetime

from github import Github
from github.GithubObject import NotSet


class GithubCollector:
    def __init__(
            self,
            github_token: str,
            repo_name: str
    ):
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)

    def _get_commits(
            self,
            since: datetime = NotSet,
            until: datetime = NotSet,
            author: str = NotSet
    ):
        commits = self.repo.get_commits(
            since=since,
            until=until,
            author=author
        )
        return commits

    def _get_pulls(
            self,
            state: str = NotSet,
            base: str = NotSet,
            head: str = NotSet,
            sort: str = NotSet,
            direction: str = NotSet
    ):
        pulls = self.repo.get_pulls(
            state=state,
            base=base,
            head=head,
            sort=sort,
            direction=direction
        )
        return pulls
