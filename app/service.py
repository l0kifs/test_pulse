from prometheus_client import start_http_server, Gauge, CollectorRegistry
import time

from config.env_vars import EnvVars
from metrics.qase_collector import QaseCollector

registry = CollectorRegistry()
tests_automated_smoke = Gauge('tests_automated_smoke', 'Number of automated smoke tests', registry=registry)
tests_manual_smoke = Gauge('tests_manual_smoke', 'Number of manual smoke tests', registry=registry)


def update_metrics():
    qase_collector = QaseCollector('https://api.qase.io', EnvVars().qase_api_token, 'MRCQA')
    new_tests_automated_smoke = qase_collector.get_number_of_test_cases(type='smoke', status='actual', automation='automated')
    tests_automated_smoke.set(new_tests_automated_smoke)
    new_tests_manual_smoke = qase_collector.get_number_of_test_cases(type='smoke', status='actual', automation='is-not-automated,to-be-automated')
    tests_manual_smoke.set(new_tests_manual_smoke)


if __name__ == "__main__":
    start_http_server(8000, registry=registry)
    print("Prometheus server started on port 8000")
    
    while True:
        update_metrics()
        time.sleep(600)
