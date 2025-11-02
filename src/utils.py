import requests
import time
import os
import json

def ensure_directories(dirs):
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

def safe_request(url, headers=None, params=None, retries=5, backoff=2, timeout=10):
    for _ in range(retries):
        try:
            r = requests.get(url, headers=headers, params=params, timeout=timeout)
            if r.status_code == 200:
                return r
            if r.status_code == 429:
                time.sleep(30)
                continue
            if 500 <= r.status_code < 600:
                time.sleep(backoff)
                continue
        except:
            time.sleep(backoff)
    return None
