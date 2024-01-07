import requests, time, yaml, re, random
from modules.utilities import get_session
from modules.captcha_utilities import solve_captcha
from modules.console import printl
from bs4 import BeautifulSoup


config = yaml.safe_load((open("config.yml", encoding="utf-8")))

#Email Verify
## 注意: メールを既読してしまうと取得ができてもurlが取得できません
def verify_email(headers, email, password, proxie, proxy_host, proxy_port, proxy_username, proxy_password):
    poipoi_session = requests.session()
    # poipoi_sessionの初期設定
    poipoi_session.cookies.set('cookie_csrf_token', config["email_verify"]["m.kuku.lu_token"])
    poipoi_session.cookies.set('cookie_sessionhash', config["email_verify"]["m.kuku.lu_sessionhash"])
    # 未読の指定したメールが来るまで2秒間隔で検索を繰り返す
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
    # verify_urlの取得
    verify_url = script_element.contents[0].replace('\n', '').replace('\t', '').replace('setTimeout(function(){location.href = "', '').replace('";}, 1);', '')
    response = requests.get(verify_url, headers=headers, proxies=f"http://{proxie}")
    verify_token = response.request.url.replace('https://discord.com/verify#token=', '')
    request_data = {"token": verify_token}
    # Emailの認証
    response = requests.post('https://discord.com/api/v9/auth/verify', headers=headers, proxies=f"http://{proxie}", json=request_data)
    if response.status_code == 200:
        token = response.json()['token']
        printl("info", f"Email Verifed {email}:{password}:{token}")
        headers['Authorization'] = token
    elif response.status_code == 400:
        if 'captcha_sitekey' in response.json().keys():
            captcha_sitekey = response.json()['captcha_sitekey']
            captcha_result = solve_captcha(captcha_sitekey, "https://discord.com/verify", proxy_host, proxy_port, proxy_username, proxy_password)
            if captcha_result:
                headers['X-Captcha-Key'] = captcha_result
                response = requests.post('https://discord.com/api/v9/auth/verify', headers=headers, json=request_data, proxies=f"http://{proxie}")
                if response.status_code == 200 or response.status_code == 201:
                    printl("info", f"Email Verifed {email}:{password}:{token}")
                    token = response.json()['token']
                    headers['Authorization'] = token
                    headers.pop('X-Captcha-Key')
                else:
                    return
            else:
                return
        else:
            return
        
#Phone Verify
def verify_phone(phone_headers, proxie, proxy_host, proxy_port, proxy_username, proxy_password):
    session = get_session()
    NUMBER = f"81090{random.randint(10000000, 99999999)}"
    payload = {"captcha_key": None, "change_phone_reason": "user_settings_update", "phone": NUMBER}
    response = session.post(
        url="https://discord.com/api/v9/users/@me/phone",
        json=payload,
        headers=phone_headers,
        proxy={"http":f"http://{proxie}"}
    )
    if "captcha_key" in response.json():
        if response.json()["captcha_key"] == ["You need to update your app to verify your phone number."]:
            
            printl("info", "Captcha Solving...")
            
            captcha_sitekey = response.json()["captcha_sitekey"]
            captcha_result = solve_captcha(captcha_sitekey, "https://discord.com/register", proxy_host, proxy_port, proxy_username, proxy_password)

            phone_headers['X-Captcha-Key'] = captcha_result

            response = session.post(
                url="https://discord.com/api/v9/users/@me/phone",
                json=payload,
                headers=phone_headers,
                proxy={"http":f"http://{proxie}"}
            )