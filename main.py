import prometheus_client
from prometheus_client import Histogram

inference_histogram = Histogram('inference_latency_seconds', 'Description of inference histogram')
inference_histogram.observe(4.7)

if __name__ == '__main__':
    PORT = 8090
    prometheus_client.start_http_server(PORT)

    while True:
        pass
