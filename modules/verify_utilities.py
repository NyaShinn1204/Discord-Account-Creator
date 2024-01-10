import requests, time, yaml, re, random
from modules.utilities import get_session
from modules.captcha_utilities import solve_captcha
from modules.phone_utilities import fivesim
from modules.console import printl
from bs4 import BeautifulSoup

config = yaml.safe_load((open("config.yml", encoding="utf-8")))

temp_header = {'Accept': '*/*','Sec-Ch-Ua-Mobile': '?0','Sec-Ch-Ua-Platform': '"Windows"','Sec-Fetch-Dest': 'empty','Sec-Fetch-Mode': 'cors','Sec-Fetch-Site': 'same-origin','X-Debug-Options': 'bugReporterEnabled','X-Discord-Locale': 'ja','X-Discord-Timezone': 'Asia/Tokyo',}

#Email Verify
## 注意: メールを既読してしまうと取得ができてもurlが取得できません
def verify_email(headers, email, password, proxie, proxy_host, proxy_port, proxy_username, proxy_password):
    poipoi_session = requests.session()
    # poipoi_sessionの初期設定
    poipoi_session.cookies.set('cookie_csrf_token', config["email_verify"]["m.kuku.lu_token"])
    poipoi_session.cookies.set('cookie_sessionhash', config["email_verify"]["m.kuku.lu_sessionhash"])
    # 未読の指定したメールが来るまで2秒間隔で検索を繰り返す
    while True:
        response = poipoi_session.get(f'https://m.kuku.lu/recv._ajax.php?&q={email} メールアドレスを確認してください&csrf_token_check={config["email_verify"]["m.kuku.lu_token"]}')
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.find('span', attrs={'class':'view_listcnt'}).contents[0] == '1':
            break
        time.sleep(2)
    soup = BeautifulSoup(response.text, 'html.parser')
    mail_element = soup.find('div', attrs={'class':'main-content'}).find('div', attrs={'style':'z-index:99;'})
    script_element = mail_element.parent.find_all('script')[2]
    parsed_javascript = re.findall(r'\'.*\'', script_element.string)
    num = parsed_javascript[1].split(',')[0].replace('\'', '')
    key = parsed_javascript[1].split(',')[1].replace('\'', '').replace(' ', '')
    
    response = poipoi_session.post('https://m.kuku.lu/smphone.app.recv.view.php', data={'num':num, 'key':key})
    soup = BeautifulSoup(response.text, 'html.parser')
    verify_redirect_url = soup.find('a', text='\n            Verify Email\n          ').attrs['href']
    response = requests.get(verify_redirect_url, headers=temp_header, proxies={"http":f"http://{proxie}"})
    soup = BeautifulSoup(response.text, 'html.parser')
    script_element = soup.find('script')
    # verify_urlの取得
    verify_url = script_element.contents[0].replace('\n', '').replace('\t', '').replace('setTimeout(function(){location.href = "', '').replace('";}, 1);', '')
    response = requests.get(verify_url, headers=temp_header, proxies={"http":f"http://{proxie}"})
    verify_token = response.request.url.replace('https://discord.com/verify#token=', '')
    request_data = {"token": verify_token}
    # Emailの認証
    response = requests.post('https://discord.com/api/v9/auth/verify', headers=headers, proxies={"http":f"http://{proxie}"}, json=request_data)
    if response.status_code == 200:
        token = response.json()['token']
        #printl("info", f"Email Verifed {email}:{password}:{token}")
        headers['Authorization'] = token
    elif response.status_code == 400:
        print(response.status_code, response.json())
        if 'captcha_sitekey' in response.json().keys():
            printl("info", "Email Captcha Solving...")
            captcha_sitekey = response.json()['captcha_sitekey']
            captcha_result = solve_captcha(captcha_sitekey, "https://discord.com/verify", proxy_host, proxy_port, proxy_username, proxy_password)
            if captcha_result:
                headers['X-Captcha-Key'] = captcha_result
                response = requests.post('https://discord.com/api/v9/auth/verify', headers=headers, json=request_data, proxies={"http":f"http://{proxie}"})
                if response.status_code == 200 or response.status_code == 201:
                    token = response.json()['token']
                    #printl("info", f"Email Verifed {email}:{password}:{token}")
                    headers['Authorization'] = token
                    headers.pop('X-Captcha-Key')
                else:
                    return
            else:
                return
        else:
            return
    response = requests.get("https://discordapp.com/api/v6/users/@me/library", headers={"Content-Type": "application/json", "authorization": token})
    if response.status_code == 403:
        printl("error", f"Generate Email Verify Locked Token {email}:{password}:{token}")
        if response.json()["message"] == "この操作を行うには、アカウントを認証する必要があります。" and response.json()["code"] == 40002:
            printl("error", f"Phone Verify Or Email Verify Requirement")
            with open("./output/locked_tokens.txt", mode='a') as f:
                f.write(token+"\n")
        else:
            printl("error", f"Reason {response.json()}")
            #return
        #return
    elif response.status_code == 200:
        printl("info", f"Generate Email Verify UnLocked Token {email}:{password}:{token}")
        with open("./output/valid_tokens.txt", mode='a') as f:
            f.write(token+"\n")
    return email,password,token
        
#Phone Verify
def verify_phone(phone_headers, password, proxie, proxy_host, proxy_port, proxy_username, proxy_password):
    
    session = get_session()
    
    if config["phone_verify"]["provider"] == "fivesim":
        NUMBER, TZID = fivesim.ordernumber()
    NUMBER = f"+{NUMBER}"
    
    data1 = {"captcha_key": None, "change_phone_reason": "user_settings_update", "phone": NUMBER}
    resp2 = session.post(
        url="https://discord.com/api/v9/users/@me/phone",
        json=data1,
        headers=phone_headers,
        proxy={"http":{"http":f"http://{proxie}"}}
    )

    if "captcha_key" in resp2.json():
        if resp2.json()["captcha_key"] == ["You need to update your app to verify your phone number."]:
            printl("info", "Captcha Solving...")
            
            captcha_sitekey = resp2.json()["captcha_sitekey"]
            data1["captcha_key"] = solve_captcha(captcha_sitekey, "https://discord.com/api/v9/users/@me/phone", proxy_host, proxy_port, proxy_username, proxy_password)


            resp2 = session.post(
                url="https://discord.com/api/v9/users/@me/phone",
                json=data1,
                headers=phone_headers,
                proxy={"http":{"http":f"http://{proxie}"}}
            )
    else:
        printl("info", "No Captcha Solving required... Skipping!")

    if resp2.status_code == 204:
        printl("info", "Successfully requested verification code!")
        
    def waitsms(NUMBER, TZID, phone_headers):
        waitcount = 0
        retries = 0
        if config["phone_verify"]["provider"] == "fivesim":
            waitcount, verifycode = fivesim.getcode(NUMBER, TZID)

        if waitcount == "TIMEOUT":
            retries += 1
            if retries >= 5:
                printl("error", "Failed to get SMS code after 5 retries, switching token!")
                #removetoken()

                if config["phone_verify"]["provider"] == "fivesim":
                    waitcount, verifycode = fivesim.deletenumber(TZID, phone_headers)
                    
                verify_phone(phone_headers, password, proxie, proxy_host, proxy_port, proxy_username, proxy_password)

            else:
                printl("error", f"Discord refused to send a SMS to {NUMBER}! Rerunning with another Number...")
                
                if config["phone_verify"]["provider"] == "fivesim":
                    waitcount, verifycode = fivesim.deletenumber(TZID, phone_headers)
                    
                verify_phone(phone_headers, password, proxie, proxy_host, proxy_port, proxy_username, proxy_password)

        return verifycode
    VERIFYCODE = waitsms(NUMBER, TZID, phone_headers)

    if VERIFYCODE is not None:
        printl("info", "Found Verificationcode: {VERIFYCODE}, sending it to Discord...")
        data2 = {"phone": NUMBER, "code": VERIFYCODE}

        resp4 = session.post(
            url="https://discord.com/api/v9/phone-verifications/verify",
            json=data2,
            headers=phone_headers,
            proxy={"http":{"http":f"http://{proxie}"}}
        ).json()
        try: phone_token = resp4["token"]
        except KeyError: phone_token = None



        data3 = {"change_phone_reason": "user_settings_update", "password": password, "phone_token": phone_token}
        session.post(
            url="https://discord.com/api/v9/users/@me/phone",
            json=data3,
            headers=phone_headers,
            proxy={"http":{"http":f"http://{proxie}"}}
        )

        printl("info", f'Successfully verified {phone_headers["authorization"]} with {NUMBER}!')
        return phone_headers["authorization"]

    elif VERIFYCODE is None:
        printl("error", "Failed to get verification code! Rerunning...")
        #removetoken()
        verify_phone(phone_headers, password, proxie, proxy_host, proxy_port, proxy_username, proxy_password)