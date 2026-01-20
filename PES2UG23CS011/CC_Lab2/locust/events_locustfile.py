from locust import HttpUser, task, between
import random

class EventsUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1, 3)
    
    def on_start(self):
        """Initialize user with a unique username"""
        self.username = f"locust_user_{random.randint(1000, 9999)}"
        self.registered_events = []
    
    @task(5)
    def view_events(self):
        """View all available events - most common action"""
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
    
    @task(3)
    def register_for_event(self):
        """Register for a random event"""
        event_id = random.randint(1, 10)
        with self.client.get(
            f"/register_event/{event_id}",
            params={"user": self.username},
            name="/register_event/[id]",
            catch_response=True,
            allow_redirects=False
        ) as response:
            if response.status_code in [302, 200]:
                self.registered_events.append(event_id)
                response.success()
            else:
                response.failure(f"Failed to register for event {event_id}")
    
    @task(2)
    def view_my_events(self):
        """View user's registered events"""
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
    
    @task(1)
    def view_checkout(self):
        """Visit checkout page"""
        with self.client.get(
            "/checkout",
            name="/checkout",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}")
