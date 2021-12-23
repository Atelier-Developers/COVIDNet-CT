import prometheus_client
from prometheus_client import Histogram, Counter, Summary

inference_histogram = Summary('inference_latency_seconds', 'Description of inference histogram')
inference_count = Counter('inference_count', 'Number of inferences')

if __name__ == '__main__':
    PORT = 8090
    prometheus_client.start_http_server(PORT)

    while True:
        pass
