from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvVars(BaseSettings):
    PROMETHEUS_URL: str
    JIRA_URL: str
    JIRA_EMAIL: str
    JIRA_API_TOKEN: str
    QASE_URL: str
    QASE_API_TOKEN: str
    QASE_PROJECT_CODE: str
    GITHUB_TOKEN: str
    GITHUB_REPO: str
        
    model_config = SettingsConfigDict(env_file='../.env')
