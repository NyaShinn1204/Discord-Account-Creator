import yaml, requests, time

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
            print(f"\t[*] Could not order the Number ({response.text})!\n")
            time.sleep(.3)
            fivesim.ordernumber()

        if response.status_code == 200:
            NUMBER, TZID = response.json()['phone'], response.json()["id"]
            print(f"\t[+] Sucessfully got Number {NUMBER}\n")
            return NUMBER, TZID