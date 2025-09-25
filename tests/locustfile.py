from locust import HttpUser, task, between

class APIUser(HttpUser):
    host = "http://127.0.0.1:8000/"
    wait_time = between(0.5, 1.5)

    @task
    def list_items(self):
        short_codes = ["yjfinN", "notexists", "OuZUgt"]
        for short_code in short_codes:
            self.client.get(f"/links/{short_code}")
            self.client.get(f"/links/{short_code}/stats")

