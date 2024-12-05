from locust import LoadTestShape
import json
from locust import HttpUser, task, between, events
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import json

response_times = []
response_timestamps = []


@events.request.add_listener
def on_request(request_type, name, response_time, response_length, response, context, exception, **kwargs):
    response_times.append(response_time)
    response_timestamps.append(datetime.now())


class APIUser(HttpUser):
    wait_time = between(1, 5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_endpoints = self.load_api_endpoints()
        self.auth_token = None  #FIXME for using the token

    def load_api_endpoints(self):
        api_file_path = os.path.join(os.path.dirname(__file__), "api_endpoints.json")
        try:
            with open(api_file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: api_endpoints.json not found at {api_file_path}")
            return []

    def on_start(self):
        pass

    @task
    def test_apis(self):
        if not self.api_endpoints:
            print("No API endpoints loaded. Skipping test.")
            return
        # FIXME for updating any random headers
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        for endpoint in self.api_endpoints:
            method = endpoint.get("method", "GET").upper()
            url = endpoint["path"]
            name = endpoint["name"]
            data = endpoint.get("data", None)

            with self.client.request(
                    method=method,
                    url=url,
                    name=name,
                    headers=headers,
                    json=data,
                    catch_response=True
            ) as response:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Expected status 200, got {response.status_code}")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    generate_percentile_graphs()


def generate_percentile_graphs():
    if not response_times:
        print("No response times recorded. Cannot generate percentile graphs.")
        return

    p50 = np.percentile(response_times, 50)
    p90 = np.percentile(response_times, 90)
    p99 = np.percentile(response_times, 99)
    print(f"Overall p50 Response Time: {p50:.2f}ms")
    print(f"Overall p90 Response Time: {p90:.2f}ms")
    print(f"Overall p99 Response Time: {p99:.2f}ms")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    graph_filename = f"percentile_graphs_{timestamp}.png"
    report_dir = "PATH_TO_SAVE_FILE" #FIXME for saving the image
    graph_path = os.path.join(report_dir, graph_filename)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

    # Response Time Distribution
    ax1.hist(response_times, bins=50, alpha=0.75, label="Response Times")
    ax1.axvline(p50, color='g', linestyle='dashed', linewidth=1, label=f'p50: {p50:.2f}ms')
    ax1.axvline(p90, color='y', linestyle='dashed', linewidth=1, label=f'p90: {p90:.2f}ms')
    ax1.axvline(p99, color='r', linestyle='dashed', linewidth=1, label=f'p99: {p99:.2f}ms')
    ax1.set_xlabel('Response Time (ms)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Response Time Distribution with Percentiles')
    ax1.legend()

    # Percentiles vs Datetime
    window_size = 100
    rolling_p50 = [np.percentile(response_times[max(0, i - window_size):i + 1], 50) for i in range(len(response_times))]
    rolling_p90 = [np.percentile(response_times[max(0, i - window_size):i + 1], 90) for i in range(len(response_times))]
    rolling_p99 = [np.percentile(response_times[max(0, i - window_size):i + 1], 99) for i in range(len(response_times))]

    ax2.plot(response_timestamps, rolling_p50, label='Rolling p50', color='g')
    ax2.plot(response_timestamps, rolling_p90, label='Rolling p90', color='y')
    ax2.plot(response_timestamps, rolling_p99, label='Rolling p99', color='r')
    ax2.set_xlabel('Datetime')
    ax2.set_ylabel('Response Time (ms)')
    ax2.set_title('Percentile Response Times vs Datetime')
    ax2.legend()
    plt.gcf().autofmt_xdate()

    plt.tight_layout()
    plt.savefig(graph_path)
    print(f"Percentile graphs saved at {graph_path}")
    plt.close()


class StagesShape(LoadTestShape):
    # FIXME for handling the load
    stages = [
        {"duration": 5, "users": 10, "spawn_rate": 0.2},
        {"duration": 10, "users": 20, "spawn_rate": 1},
        {"duration": 5, "users": 10, "spawn_rate": -0.1},
        {"duration": 5, "users": 10, "spawn_rate": -1}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None