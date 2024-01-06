import requests, httpx, time, yaml
from modules.console import printl

config = yaml.safe_load((open("config.yml", encoding="utf-8")))

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
    
def solve_captcha(sitekey, siteurl, address, port, username, password):
    client = httpx.Client(timeout=httpx.Timeout(20.0, read=20.0))
    startedSolving = time.time()
    url = "https://api.anti-captcha.com/createTask"
    data = {
        "clientKey": config["captcha_solver"]["apikey"],
        "task":
        {
            "type": "HCaptchaTask",
            "websiteURL": siteurl,
            "websiteKey": sitekey,
            "proxyType": "http",
            "proxyAddress": address,
            "proxyPort": port,
            "proxyLogin": username,
            "proxyPassword": password
        }
    }
    response = client.post(url,json=data)
    if response.json()['errorId'] == 0:
        task_id = response.json()['taskId']
        url = "https://api.anti-captcha.com/getTaskResult"
        data = {
            "clientKey": config["captcha_solver"]["apikey"],
            "taskId": task_id
        }
        response = client.post(url,json=data)
        while response.json()['status'] == 'processing':
            time.sleep(3)
            response = client.post(url,json=data)
        printl("info", f"Solved | {response.json()['solution']['gRecaptchaResponse'][-32:]} In {round(time.time()-startedSolving)}s")
        return response.json()['solution']['gRecaptchaResponse']
    else:
        printl("error", f"[{(response.json()['errorDescription'])}")
        return False