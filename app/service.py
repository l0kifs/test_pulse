from prometheus_client import start_http_server, Gauge, CollectorRegistry
import time

from metrics.metrics import get_number_of_smoke_tests


registry = CollectorRegistry()
automated_smoke_tests = Gauge('automated_smoke_tests', 'Number of automated smoke tests', registry=registry)
manual_smoke_tests = Gauge('manual_smoke_tests', 'Number of manual smoke tests', registry=registry)


def update_metrics():
    automated_smoke_tests.set(get_number_of_smoke_tests(automated=True))
    manual_smoke_tests.set(get_number_of_smoke_tests(automated=False))


if __name__ == "__main__":
    start_http_server(8000, registry=registry)
    print("Prometheus server started on port 8000")
    
    while True:
        update_metrics()
        time.sleep(1800)
