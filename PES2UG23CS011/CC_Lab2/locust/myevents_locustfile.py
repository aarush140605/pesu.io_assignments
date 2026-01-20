from locust import HttpUser, task, between
import random

class MyEventsUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 3)
    
    def on_start(self):
        """Initialize user and register for some events"""
        self.username = f"locust_user_{random.randint(1000, 9999)}"
        # Pre-register for 2-3 events to test my-events page
        for _ in range(random.randint(2, 3)):
            event_id = random.randint(1, 10)
            self.client.get(
                f"/register_event/{event_id}",
                params={"user": self.username},
                name="/register_event/[id] (setup)",
                allow_redirects=False
            )
    
    @task(5)
    def view_my_events(self):
        """View registered events - primary action"""
        with self.client.get(
            "/my-events",
            params={"user": self.username},
            name="/my-events",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}")
    
    @task(2)
    def register_additional_event(self):
        """Register for more events"""
        event_id = random.randint(1, 10)
        with self.client.get(
            f"/register_event/{event_id}",
            params={"user": self.username},
            name="/register_event/[id]",
            catch_response=True,
            allow_redirects=False
        ) as response:
            if response.status_code in [302, 200]:
                response.success()
            else:
                response.failure(f"Failed to register for event {event_id}")
    
    @task(3)
    def view_all_events(self):
        """Browse available events"""
        with self.client.get(
            "/events",
            params={"user": self.username},
            name="/events",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}")
    
    @task(1)
    def view_checkout(self):
        """Check total cost"""
        with self.client.get(
            "/checkout",
            name="/checkout",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}")
