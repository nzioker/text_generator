import httpx
import time

url = "http://localhost:8000/generate"

def rate_limit_test():

    with httpx as client:
        for i in range(1,15):
            response = client.get(url)
            print(f"Request no: {i} | status code {response.status_code}| Response =  {response.text}")
    time.sleep(60)

    with httpx as client:
        response = client.get(url)
        print(f"Status code = {response.status_code} | Response = {response.text}")

if __name__ == "__main__":
    rate_limit_test()
