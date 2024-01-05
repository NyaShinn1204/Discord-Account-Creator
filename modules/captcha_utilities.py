import requests

def get_balance(provider, apikey):
    resp = requests.post(f"https://api.{provider}/getBalance", json={"clientKey": {apikey}})
    if resp.status_code == 200:
        balance = resp.json()["balance"]
        if balance == 0.0:
            print(f"[+] Working Key: {apikey[:10]}  But Balance 0.0$")
        else:
            print(f"[+] Working Key: {apikey[:10]}  Balance: {balance}$")
        return resp.json()["balance"]
    elif "ERROR_KEY_DOES_NOT_EXIST" in resp.text:
        print(f"[-] Invalid Key: {apikey[:10]}")
        return 0.0
    else:
        print(f"[-] Invalid Key Or Exception Error   Key: {apikey[:10]} Status Code: {resp.status_code}")
        return 0.0