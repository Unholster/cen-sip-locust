import json
from locust import HttpLocust, TaskSet, task


def is_v1_endpoint(url):
    return url.startswith('/api/v1/')


class RequestTSVFiles(TaskSet):
    endpoints = []
    media_type = 'text/tab-separated-values-data'

    def on_start(self):
        with open('endpoint_urls', 'r') as endpoints_file:
            self.endpoints = json.load(endpoints_file)

    @task
    def api_v1(self):
        for endpoint in self.endpoints:
            if is_v1_endpoint(endpoint):
                response = self.client.get(endpoint,
                                           headers={'Origin': 'https://www.coordinador.cl',
                                                    'Referer': 'https://www.coordinador.cl/',
                                                    'Accept': self.media_type})
                print(response.content)


class WebsiteUser(HttpLocust):
    task_set = RequestTSVFiles
    min_wait = 0
    max_wait = 3000