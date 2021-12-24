import prometheus_client
import os
from prometheus_client import CollectorRegistry, multiprocess, start_http_server, push_to_gateway, REGISTRY
from prometheus_client import Histogram, Counter, Summary


def create_collector():
    """
    Create a global registry collector
    """
    multiprocess.MultiProcessCollector(REGISTRY, path="/app/COVIDNet-CT/multiprocess_metrics")


inference_histogram = Summary('inference_latency_seconds', 'Description of inference histogram', registry=REGISTRY)

if __name__ == '__main__':
    create_collector()
    PORT = 8090
    prometheus_client.start_http_server(PORT, registry=REGISTRY)

    while True:
        pass
