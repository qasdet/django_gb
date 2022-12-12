from locust import HttpUser, task

SERVER_IP_ADDR = '37.140.197.43'


class LoadTestingBrainiacLMS(HttpUser):
    @task
    def test_some_pages_open(self):
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/courses/')
        self.client.get(f'http://{SERVER_IP_ADDR}/mainapp/courses/1')
        self.client.get(f'http://{SERVER_IP_ADDR}/authapp/register/')
        self.client.get(f'http://{SERVER_IP_ADDR}/authapp/login/')