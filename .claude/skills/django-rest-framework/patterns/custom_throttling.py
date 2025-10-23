# patterns/custom_throttling.py

# This file demonstrates how to implement custom throttling classes in Django REST Framework.
# Throttling is used to control the rate of requests that clients can make to an API,
# preventing abuse and ensuring fair usage.

from rest_framework.throttling import BaseThrottle, SimpleRateThrottle
import time
from datetime import datetime, timedelta

# --- 1. Simple Custom Throttling (based on IP address) ---
# This example limits each IP address to 3 requests per minute.

VISIT_HISTORY = {}

class CustomIPThrottle(BaseThrottle):
    rate = 3 # requests
    duration = 60 # seconds

    def allow_request(self, request, view):
        # Get the client's IP address
        ip = request.META.get('REMOTE_ADDR')
        if not ip:
            return True # Or handle as an error

        now = time.time()

        # Get the history of requests for this IP
        history = VISIT_HISTORY.get(ip, [])

        # Remove old requests from history
        while history and history[-1] < now - self.duration:
            history.pop()

        # Check if the number of requests exceeds the rate limit
        if len(history) >= self.rate:
            return False # Request not allowed

        # Add current request to history
        history.insert(0, now)
        VISIT_HISTORY[ip] = history
        return True # Request allowed

    def wait(self):
        # Calculate how long the client needs to wait
        ip = self.request.META.get('REMOTE_ADDR')
        history = VISIT_HISTORY.get(ip, [])
        if history:
            # Time until the oldest request in history expires
            return self.duration - (time.time() - history[-1])
        return None

# --- 2. Custom Throttling using SimpleRateThrottle (recommended for most cases) ---
# SimpleRateThrottle is a more robust base class that handles the history management for you.
# You just need to define `scope` and `get_cache_key`.

class BurstRateThrottle(SimpleRateThrottle):
    scope = 'burst'
    rate = '10/minute' # 10 requests per minute

    def get_cache_key(self, request, view):
        # Use user ID for authenticated users, or IP for anonymous users
        if request.user.is_authenticated:
            return request.user.pk
        return self.get_ident(request) # Fallback to IP address

class SustainedRateThrottle(SimpleRateThrottle):
    scope = 'sustained'
    rate = '100/day' # 100 requests per day

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return request.user.pk
        return self.get_ident(request)

# --- myapp/views.py (example usage) ---
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .throttling import CustomIPThrottle, BurstRateThrottle, SustainedRateThrottle # Assuming throttling classes are defined

class ExampleAPIView(APIView):
    # Apply custom throttling classes to the view
    throttle_classes = [BurstRateThrottle, SustainedRateThrottle] # Can apply multiple throttles

    def get(self, request, format=None):
        # Simulate some work
        return Response({"message": "Hello from throttled API!"}, status=status.HTTP_200_OK)

# --- Example Usage (conceptual) ---
# To test this conceptually, you'd simulate multiple requests.
# In a real Django project:
# 1. Add 'rest_framework.throttling.AnonRateThrottle' and 'rest_framework.throttling.UserRateThrottle'
#    to DEFAULT_THROTTLE_CLASSES in settings.py for global throttling.
# 2. Define your custom throttles in a file like `myapp/throttling.py`.
# 3. Apply them to views using `throttle_classes = [...]`.

# Example of simulating requests (not actual HTTP requests)
class MockRequest:
    def __init__(self, ip_addr, user=None):
        self.META = {'REMOTE_ADDR': ip_addr}
        self.user = user if user else MockUser('anonymous', is_authenticated=False)

class MockUser:
    def __init__(self, username, is_authenticated=True, pk=None):
        self.username = username
        self.is_authenticated = is_authenticated
        self.pk = pk if pk else 1 # Primary key for user

class MockView:
    pass

print("--- CustomIPThrottle Demonstration ---")
ip_throttle = CustomIPThrottle()
mock_view = MockView()

# Simulate 5 requests from the same IP within a minute
for i in range(1, 6):
    mock_request = MockRequest(ip_addr='192.168.1.1')
    allowed = ip_throttle.allow_request(mock_request, mock_view)
    if allowed:
        print(f"Request {i} from 192.168.1.1: {COLOR_GREEN}ALLOWED{COLOR_RESET}")
    else:
        wait_time = ip_throttle.wait()
        print(f"Request {i} from 192.168.1.1: {COLOR_RED}DENIED{COLOR_RESET}. Wait for {wait_time:.2f} seconds.")

# Reset history for next demo
VISIT_HISTORY = {}

print("\n--- BurstRateThrottle (conceptual) Demonstration ---")
# SimpleRateThrottle uses Django's cache backend. For this conceptual example,
# we can't fully simulate it without a running Django app and cache.
# However, the logic is that it would allow 10 requests per minute per user/IP.

burst_throttle = BurstRateThrottle()

# Simulate requests from an authenticated user
auth_user = MockUser('testuser', pk=1)
for i in range(1, 12):
    mock_request = MockRequest(ip_addr='192.168.1.2', user=auth_user)
    # In a real scenario, SimpleRateThrottle would interact with Django's cache
    # For this demo, we'll just show the setup.
    # print(f"Request {i} from {auth_user.username}: {burst_throttle.allow_request(mock_request, mock_view)}")
    pass # Cannot run without cache

print("BurstRateThrottle and SustainedRateThrottle rely on Django's cache backend.")
print("To fully test, integrate into a running Django project with cache configured.")
