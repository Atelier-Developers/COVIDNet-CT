import prometheus_client
from prometheus_client import Histogram

inference_histogram = Histogram('inference_latency_seconds', 'Description of inference histogram')
is_up = prometheus_client.Gauge("app_is_up", "is the target url responding")

if __name__ == '__main__':
    PORT = 8090
    prometheus_client.start_http_server(PORT)

    while True:
        is_up.set(1)
