import json

from app.config.env_vars import EnvVars
from app.metrics.qase_collector import QaseCollector


def test_qase_collector():
    collector = QaseCollector('https://api.qase.io', EnvVars().qase_api_token, 'DEMO')
    results = collector.get_test_run_results()
    print(json.dumps(results, indent=4))
