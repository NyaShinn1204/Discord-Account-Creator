import yaml, random, base64, json, string, requests, time, re
from modules.utilities import get_session, get_cookies, get_fingerprint, get_buildnum, get_username, get_globalname, get_email, get_password, format_proxy
from modules.captcha_utilities import solve_captcha
from modules.console import printl
from modules.random_agent import random_agent
from bs4 import BeautifulSoup

def creator(proxie):
    config = yaml.safe_load((open("config.yml", encoding="utf-8")))
    formated_proxy = format_proxy(proxie)
    if formated_proxy[0] == 1:
        proxy_host = formated_proxy[1]
        proxy_port = formated_proxy[2]
        printl("info", f"Running on {proxy_host[:7] + '*' * (len(proxy_host) - 7)}:{proxy_port}")
    if formated_proxy[0] == 2:
        proxy_username = formated_proxy[1]
        proxy_password = formated_proxy[2]
        proxy_host = formated_proxy[3]
        proxy_port = formated_proxy[4]
        printl("info", f"Running Proxie of {proxy_host[:7] + '*' * (len(proxy_host) - 7)}:{proxy_port} | {proxy_username[:3] + '*' * (len(proxy_username) - 3)}:{proxy_password[:3] + '*' * (len(proxy_password) - 3)}")
    session = get_session()
    cookies = get_cookies(session)
    fingerprint = get_fingerprint(session)
    username = get_username()
    if not config["register"]["global_username"] == '':
        global_name = config["register"]["global_username"]
        printl("info", f"Got Global Username {global_name}")
    else:
        global_name = get_globalname()
    if config["email_verify"]["enable"] == True:
        email = get_email(config["email_verify"]["m.kuku.lu_token"], config["email_verify"]["m.kuku.lu_sessionhash"])
        if email == "":
            printl("error", "Failed to Generate Email")
            printl("error", "Please review your settings.")
        else:
            printl("info", f"Geneated Email {email}")
    else:
        email = f"{''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(15)))}@gmail.com" 
    password = get_password()

    # Headers
    ##ここから
    agent_string = random_agent()
    buildnum = get_buildnum(session)
    browser_data = agent_string.split(" ")[-1].split("/")
    possible_os_list = ["Windows", "Macintosh"]
    for possible_os in possible_os_list:
        if possible_os in agent_string:
            agent_os = possible_os
    if agent_os == "Macintosh":
        os_version = f'Intel Mac OS X 10_15_{str(random.randint(5, 7))}'
    else:
        os_version = "10"
    device_info = {
        "os": agent_os,
        "browser": browser_data[0],
        "device": "",
        "system_locale": "ja-JP",
        "browser_user_agent": agent_string,
        "browser_version": browser_data[1],
        "os_version": os_version,
        "referrer": "",
        "referring_domain": "",
        "referrer_current": "",
        "referring_domain_current": "",
        "release_channel": "stable",
        "client_build_number": buildnum,
        "client_event_source": None
    }
    headers = {
        "Accept":"*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "discord.com",
        "Origin": "https://discord.com",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "sec-ch-ua-platform": "Windows",
        "sec-ch-ua-mobile": "?0",
        "TE": "Trailers",
        "User-Agent": agent_string,
        "x-fingerprint": fingerprint,
        "X-Super-Properties": base64.b64encode(json.dumps(device_info).encode('utf-8')).decode("utf-8"),
        "X-Debug-Options": "bugReporterEnabled"
    }
    ##ここまで
    
    # Payload
    ##ここから
    payload = {
        "consent": True,
        "data_of_birth": f"{random.randint(1950, 2004)}-{str(random.randint(1, 12)).zfill(2)}-{str(random.randint(1, 28)).zfill(2)}",
        "email": email,
        "fingerprint": fingerprint,
        "gift_code_sku_id": None,
        "global_name": global_name,
        "invite": None,
        "password": password,
        "promotional_email_opt_in": False,
        "username": username,
    }
    ##ここまで
    
    response = session.post('https://discord.com/api/v9/auth/register', headers=headers, proxy=f"http://{proxie}", json=payload, cookies=cookies)
    if response.status_code == 429:
        printl("error", "WTF??? RATELIMITED :skull:")
    print(response.status_code, response.json())
    if response.status_code == 201:
        token = response.json()['token']
        printl("info", f"Success Create Account {email}:{password}:{token}")
    elif response.status_code == 400:
        printl("info", "Captcha Solving...")
        captcha_sitekey = response.json()["captcha_sitekey"]
        captcha_result = solve_captcha(captcha_sitekey, "https://discord.com/register", proxy_host, proxy_port, proxy_username, proxy_password)
        if captcha_result:
            headers['X-Captcha-Key'] = captcha_result
            response = session.post('https://discord.com/api/v9/auth/register', headers=headers, proxy=f"http://{proxie}", json=payload, cookies=cookies)
            #print(response.status_code, response.text)
            if response.status_code == 200 or response.status_code == 201:
                token = response.json()['token']
                response = requests.get("https://discordapp.com/api/v6/users/@me/library", headers={"Content-Type": "application/json", "authorization": token})
                if response.status_code == 403:
                    printl("error", f"Lol Generate Locked Token {email}:{password}:{token}")
                    return
                elif response.status_code == 200:
                    printl("info", f"Success Create Account {email}:{password}:{token}")
                    headers['Authorization'] = token
                    headers.pop('X-Captcha-Key')
            else:
                return
        else:
            return
        
        
    if config["email_verify"]["enable"] == True:
        poipoi_session = requests.session()
        poipoi_session.cookies.set('cookie_csrf_token', config["email_verify"]["m.kuku.lu_token"])
        poipoi_session.cookies.set('cookie_sessionhash', config["email_verify"]["m.kuku.lu_sessionhash"])
        while True:
            response = poipoi_session.get(f'https://m.kuku.lu/recv._ajax.php?&q={email} Verify Email Address for Discord&csrf_token_check={config["email_verify"]["m.kuku.lu_token"]}')
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
        response = requests.get(verify_redirect_url, headers=headers, proxies=f"http://{proxie}")
        soup = BeautifulSoup(response.text, 'html.parser')
        script_element = soup.find('script')
        verify_url = script_element.contents[0].replace('\n', '').replace('\t', '').replace('setTimeout(function(){location.href = "', '').replace('";}, 1);', '')
        response = requests.get(verify_url, headers=headers, proxies=f"http://{proxie}")
        verify_token = response.request.url.replace('https://discord.com/verify#token=', '')
        request_data = {"token": verify_token}
        response = requests.post('https://discord.com/api/v9/auth/verify', headers=headers, proxies=f"http://{proxie}", json=request_data)
        print(response.status_code, response.text)
        if response.status_code == 200:
            token = response.json()['token']
            print(f'[Email Verified] {email}:{password}:{token}')
            headers['Authorization'] = token
        elif response.status_code == 400:
            if 'captcha_sitekey' in response.json().keys():
                captcha_sitekey = response.json()['captcha_sitekey']
                captcha_result = solve_captcha(captcha_sitekey, "https://discord.com/verify", proxy_host, proxy_port, proxy_username, proxy_password)
                if captcha_result:
                    headers['X-Captcha-Key'] = captcha_result
                    response = requests.post('https://discord.com/api/v9/auth/verify', headers=headers, json=request_data, proxies=f"http://{proxie}")
                    print(response.status_code, response.text)
                    if response.status_code == 200 or response.status_code == 201:
                        print(f'[Email Verified] {email}:{password}:{token}')
                        token = response.json()['token']
                        headers['Authorization'] = token
                        headers.pop('X-Captcha-Key')
                    else:
                        return
                else:
                    return
            else:
                return