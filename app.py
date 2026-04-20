# Python health check app
import requests
def check_url(url):
    try:
        res = requests.get(url,timeout=5)
        return {"url": url, "status": "UP", "code": res.status_code}
    except Exception as e:
        return {"url": url, "status": "DOWN", "code": None}

if __name__ =="__main__":
    urls=["https://google.com","https://httpbin.org/status/50"]
    for url in urls:
        result = check_url(url)
        print(f"[{result['status']}] {result['url']}")
