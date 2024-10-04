from prometheus_client import start_http_server, Gauge, CollectorRegistry
import time

from app.config.env_vars import EnvVars
from app.metrics.qase_collector import QaseCollector

registry = CollectorRegistry()
tests_automated_smoke = Gauge('tests_automated_smoke', 'Number of automated smoke tests', registry=registry)


def update_metrics():
    collector = QaseCollector('https://api.qase.io', EnvVars().qase_api_token, 'MRCQA')
    new_tests_automated_smoke = collector.get_number_of_test_cases(type='smoke', status='actual', automation='automated')
    tests_automated_smoke.set(new_tests_automated_smoke)


if __name__ == "__main__":
    start_http_server(8000, registry=registry)
    print("Prometheus server started on port 8000")
    
    while True:
        update_metrics()
        time.sleep(10)
