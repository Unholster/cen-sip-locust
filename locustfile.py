import json
from locust import HttpLocust, TaskSet, task


def is_v1_endpoint(url):
    return url.startswith('/api/v1/')


class UserBehavior(TaskSet):
    endpoints = []

    def on_start(self):
        with open('endpoint_urls', 'r') as endpoints_file:
            self.endpoints = json.load(endpoints_file)

    @task(1)
    def api_v1_json(self):
        for endpoint in self.endpoints:
            if is_v1_endpoint(endpoint):
                response = self.client.get(endpoint,
                                           headers={'Accept': 'application/json',
                                                    'Origin': 'https://www.coordinador.cl',
                                                    'Referer': 'https://www.coordinador.cl'})
                print(response.content)

    @task(1)
    def api_v1_tsv(self):
        for endpoint in self.endpoints:
            if is_v1_endpoint(endpoint):
                response = self.client.get(endpoint,
                                           headers={'Origin': 'https://www.coordinador.cl',
                                                    'Referer': 'https://www.coordinador.cl/',
                                                    'Accept': 'text/tab-separated-values-data'})
                print(response.content)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 3000