from pydantic_settings import BaseSettings


class EnvVars(BaseSettings):
    jira_email: str
    jira_api_token: str
    qase_api_token: str
    github_token: str
    github_repo: str

    class Config:
        env_file = '../.env'


def get_env_vars():
    return EnvVars()