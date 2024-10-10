import json

from app.config.env_vars import EnvVars
from app.metrics.qase_collector import QaseCollector


def test_get_test_cases():
    collector = QaseCollector('https://api.qase.io', EnvVars().qase_api_token, 'MRCQA')
    result = collector._get_test_cases(type='smoke', status='actual', max_results=1)
    print(json.dumps(result, indent=4))


def test_get_number_of_test_cases():
    collector = QaseCollector('https://api.qase.io', EnvVars().qase_api_token, 'MRCQA')
    result = collector.get_number_of_test_cases(type='smoke', status='actual', automation='automated')
    print(result)
    
def test_get_all_test_cases():
    collector = QaseCollector('https://api.qase.io', EnvVars().qase_api_token, 'MRCQA')
    result = collector.get_all_test_cases(type='smoke', status='actual', automation='automated')
    print(len(result))