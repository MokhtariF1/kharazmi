import requests
import time
s = time.perf_counter()
count = 0
url = "http://127.0.0.1:8000/?text={}"
for i in range(1, 31):
    r = requests.get("https://api.keybit.ir/ayamidanid/").json()["text"]
    url = f"http://127.0.0.1:8000/send-message/?text={r}&peer_id=-69878697"
    response = requests.post(url)
    count += 1
    time.sleep(5)
e = time.perf_counter()

print(e - s)
print(count)