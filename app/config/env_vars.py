from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvVars(BaseSettings):
    prometheus_url: str
    jira_email: str
    jira_api_token: str
    qase_api_token: str
    github_token: str
    github_repo: str
        
    model_config = SettingsConfigDict(env_file='../.env')
