import requests

def fetch_data():
    try:
        resp = requests.get("https://api.example.com/data", timeout=10)
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def save_data(data):
    try:
        with open("output.txt", "w") as f:
            f.write(data)
    except OSError as e:
        return False
    return True
