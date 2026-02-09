import subprocess
import time
import requests
import sys

print("Testing Django development server...")

# Start server in background
server = subprocess.Popen(
    ['python', 'manage.py', 'runserver'],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
time.sleep(3)

try:
    # Test if server is running
    response = requests.get('http://127.0.0.1:8000/', timeout=5)
    if response.status_code == 200:
        print("✅ Server is running successfully!")
        print("✅ Home page is accessible")
    else:
        print(f"⚠️  Server returned status code: {response.status_code}")
except Exception as e:
    print(f"❌ Could not connect to server: {e}")
finally:
    # Stop server
    server.terminate()
    server.wait()
    print("✅ Server test completed")
