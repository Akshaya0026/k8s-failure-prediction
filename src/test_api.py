import urllib.request
import urllib.parse
import json
import sys

def test_prediction():
    url = "http://127.0.0.1:8000/predict/"
    params = {
        "cpu_usage": 80,
        "memory_usage": 90,
        "disk_io": 50,
        "network_io": 30
    }
    
    # The FastAPI endpoint expects a JSON body for a POST request
    data = json.dumps(params).encode('utf-8')
    
    print(f"Sending POST request to: {url} with data: {data}")
    
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"Status Code: {response.getcode()}")
            print("Response:", result)
    except urllib.error.URLError as e:
        print(f"Error: Could not connect to server. Is it running? ({e})")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_prediction()
