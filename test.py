import requests
import time
s = time.perf_counter()
url = "http://127.0.0.1:8000/?text={}"
for i in range(1, 10):
    url = f"http://127.0.0.1:8000/send-message/?text=**تست** __{i}__&peer_id=-70896711"
    response = requests.post(url)
    print(response.json())
e = time.perf_counter()

print(e - s)