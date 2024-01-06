import yaml, random, base64, json, string
from modules.utilities import get_session, get_cookies, get_fingerprint, get_buildnum, get_username, get_globalname, get_email, get_password, format_proxy
from modules.console import printl
from modules.random_agent import random_agent

def creator(proxie):
    config = yaml.safe_load((open("config.yml", encoding="utf-8")))
    formated_proxy = format_proxy(proxie)
    if formated_proxy[0] == 1:
        printl("info", f"Running on {formated_proxy[1][:7] + '*' * (len(formated_proxy[1]) - 7)}:{formated_proxy[2]}")
    if formated_proxy[0] == 2:
        printl("info", f"Running Proxie of {formated_proxy[3][:7] + '*' * (len(formated_proxy[3]) - 7)}:{formated_proxy[4]} | {formated_proxy[1][:3] + '*' * (len(formated_proxy[1]) - 3)}:{formated_proxy[2][:3] + '*' * (len(formated_proxy[2]) - 3)}")
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