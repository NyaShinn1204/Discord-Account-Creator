import yaml, requests, time, tls_client
from modules.console import printl

config = yaml.safe_load((open("config.yml", encoding="utf-8")))

headers = {
    "Authorization": f'Bearer {config["phone_verify"]["apikey"]}',
    "Accept": "application/json"
}

class fivesim:
    def ordernumber():
        url = f'https://5sim.net/v1/user/buy/activation/{config["phone_verify"]["country"]}/any/discord'
        with requests.Client(headers=headers) as client: response = client.get(url)
        if response.status_code == 400:
            printl("error", f"\t[*] Could not order the Number ({response.text})!")
            time.sleep(.3)
            fivesim.ordernumber()

        if response.status_code == 200:
            NUMBER, TZID = response.json()['phone'], response.json()["id"]
            printl("info", f"\t[+] Sucessfully got Number {NUMBER}")
            return NUMBER, TZID

    def deletenumber(TZID, phone_headers):
        url = f"https://5sim.net/v1/user/cancel/{TZID}"
        with requests.Client(headers=phone_headers) as client: response = client.get(url).json()
        if response["status"] != "CANCELED": printl("error", f"Could not delete the Number ({response['status']})!")

    def getcode(NUMBER, TZID, phone_headers):
        waitcount = 0
        session = tls_client.Session(client_identifier="safari_ios_16_0")
        url = f"https://5sim.net/v1/user/check/{TZID}"
        discordurl = "https://discord.com/api/v9/users/@me/phone"

        ratelimited = False
        ratelimit_duration = None
        with requests.Client(headers=phone_headers) as client: response = client.get(url).json()
        while response["sms"] == []:
            waitcount += 1

            printl("info", f"Discord haven't sent the SMS so far... {waitcount}/120!")
            with requests.Client(timeout=requests.Timeout(20.0, read=None)) as client:
                response = client.get(url, headers=phone_headers).json()
                time.sleep(.3)

                if ratelimited:
                    time.sleep(int(ratelimit_duration))

            if waitcount % 5 == 0: # run every x time to request a new sms from discord
                data = {"phone": NUMBER, "change_phone_reason": "user_action_required"}

                discordresponse = session.post(
                    url=discordurl,
                    json=data,
                    headers=phone_headers
                ).json()

                if "message" in discordresponse:
                    if "message" == "The resource is being rate limited.":
                        ratelimit_duration = discordresponse['retry_after']
                        printl("error", f"Ratelimited for requesting a new SMS ({str(ratelimit_duration)} Seconds!) We now try to get the SMS without requesting a new one...")
                        ratelimited = True

            if waitcount >= 120:
                return "TIMEOUT", False

        VERIFYCODE = response["sms"][0]["code"] if response["status"] == "FINISHED" else None # FINISHED may need to be changed to RECEIVED if verification failed error happen after sms got delivered
        return waitcount, VERIFYCODE