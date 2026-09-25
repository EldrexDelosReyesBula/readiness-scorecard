import requests

def fetch_data():
    # Dangerous unprotected network call
    resp = requests.get("https://api.example.com/data")
    return resp.json()

def save_data(data):
    # Dangerous unprotected file write
    f = open("output.txt", "w")
    f.write(data)
    f.close()
