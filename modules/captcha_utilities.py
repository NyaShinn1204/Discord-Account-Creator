import requests
from modules.console import printl

def get_balance(provider, apikey):
    try:
        resp = requests.post("https://api.{}/getBalance".format(provider), json={"clientKey": apikey})
        if resp.status_code == 200:
            return resp.json()["balance"]
        elif "ERROR_KEY_DOES_NOT_EXIST" in resp.text:
            printl("error", "Failed to get captcha balance")
            return 0.0
        else:
            printl("error", "Failed to get captcha balance")
            return 0.0
    except:
        printl("error", "Failed to get captcha balance")
        return 0.0