import yaml, random, base64, json, string, requests, time, re
from modules.utilities import get_session, get_cookies, get_fingerprint, get_buildnum, get_username, get_globalname, get_email, get_password, format_proxy
from modules.captcha_utilities import solve_captcha
from modules.verify_utilities import verify_email, verify_phone
from modules.console import printl
from modules.random_agent import random_agent

def creator(proxie):
    config = yaml.safe_load((open("config.yml", encoding="utf-8")))
    formated_proxy = format_proxy(proxie)
    if formated_proxy[0] == 1:
        proxy_host = formated_proxy[1]
        proxy_port = formated_proxy[2]
        convert_proxie = f"{proxy_host[:7] + '*' * (len(proxy_host) - 7)}:{proxy_port}"
    if formated_proxy[0] == 2:
        proxy_username = formated_proxy[1]
        proxy_password = formated_proxy[2]
        proxy_host = formated_proxy[3]
        proxy_port = formated_proxy[4]
        convert_proxie = f"{proxy_host[:7] + '*' * (len(proxy_host) - 7)}:{proxy_port} | {proxy_username[:3] + '*' * (len(proxy_username) - 3)}:{proxy_password[:3] + '*' * (len(proxy_password) - 3)}"
    printl("info", f"Running Proxie of {convert_proxie}")
    try:
        start = time.time()
        response = requests.get("http://example.com", proxies={"http" : f"http://{proxie}"})
        end = time.time()
        time_elapsed = end - start
        time_elapsed = time_elapsed * 1000
        printl("info", f"{convert_proxie} - Working {round(time_elapsed)}ms")
    except IOError:
        printl("error", f"Connection error of {convert_proxie}")
        return
    except:
        printl("error", f"Failed Check Proxies of {convert_proxie}")
        return
    session = get_session()
    cookies = get_cookies(session, proxie)
    fingerprint = get_fingerprint(session)
    username = get_username(session, proxie)
    if not config["register"]["global_username"] == '':
        global_name = config["register"]["global_username"]
        printl("info", f"Got Global Username {global_name}")
    else:
        global_name = get_globalname(session)
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
    token = None


    # 初期設定Headers
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
    
    # Normal Headers
    ##ここから
    headers = {
        "Accept":"*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja;q=0.7",
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
        "sec-ch-ua": "'Not_A Brand';v='8', 'Chromium';v='120', 'Brave';v='120'",
        "TE": "Trailers",
        "User-Agent": agent_string,
        "X-Discord-Locale": "ja",
        "X-Discord-Timezone": "Asia/Tokyo",
        "x-fingerprint": fingerprint,
        "X-Super-Properties": base64.b64encode(json.dumps(device_info).encode('utf-8')).decode("utf-8"),
        "X-Debug-Options": "bugReporterEnabled"
    }
    ##ここまで
    
    # Phone Verify Headers
    ##ここから
    phone_headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "authorization": token,
        "content-type": "application/json",
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": agent_string,
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
    
    response = session.post('https://discord.com/api/v9/auth/register', headers=headers, proxy={"http":f"http://{proxie}"}, json=payload, cookies=cookies)
    if response.status_code == 429:
        printl("error", "WTF??? RATELIMITED :skull:")
        return
    else:
        print(response.status_code, response.json())
    if response.status_code == 201:
        token = response.json()['token']
        phone_headers["authorization"] = token
        printl("info", f"Success Create Account {email}:{password}:{token}")
    elif response.status_code == 400:
        printl("info", "Captcha Solving...")
        captcha_sitekey = response.json()["captcha_sitekey"]
        captcha_result = solve_captcha(captcha_sitekey, "https://discord.com/register", proxy_host, proxy_port, proxy_username, proxy_password)
        if captcha_result:
            headers['X-Captcha-Key'] = captcha_result
            response = session.post('https://discord.com/api/v9/auth/register', headers=headers, proxy={"http":f"http://{proxie}"}, json=payload, cookies=cookies)
            if response.status_code == 200 or response.status_code == 201:
                token = response.json()['token']
                phone_headers["authorization"] = token
                response = requests.get("https://discordapp.com/api/v6/users/@me/library", headers={"Content-Type": "application/json", "authorization": token})
                if response.status_code == 403:
                    printl("error", f"Generate Locked Token {email}:{password}:{token}")
                    if response.json()["message"] == "この操作を行うには、アカウントを認証する必要があります。" and response.json()["code"] == 40002:
                        printl("error", f"Phone Verify Or Email Verify Requirement")
                    else:
                        printl("error", f"Reason {response.json()}")
                        #return
                    #return
                elif response.status_code == 200:
                    printl("info", f"Generate UnLocked Token {email}:{password}:{token}")
                    headers['Authorization'] = token
                    headers.pop('X-Captcha-Key')
                else:
                    printl("error", "LOL FAILED TO GENERATE ACCOUNT")
                    return
            else:
                return
        else:
            return 
    else:
        printl("error", f"Failed to Response Register {response.json()}")
    
    #Email Verify
    if config["email_verify"]["enable"] == True:
        verify_email(headers, email, password, proxie, proxy_host, proxy_port, proxy_username, proxy_password)
        
    #Phone Verify
    if config["phone_verify"]["enable"] == True:
        verify_phone(phone_headers, password, proxie, proxy_host, proxy_port, proxy_username, proxy_password)