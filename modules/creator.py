from modules.utilities import get_session, get_cookies, get_fingerprint, format_proxy
from modules.console import printl

def creator(proxie):
    formated_proxy = format_proxy(proxie)
    if formated_proxy[0] == 1:
        host = formated_proxy[1]
        port = formated_proxy[2]
        printl("info", f"Running on {host[:7] + '*' * (len(host) - 7)}:{port}")
    if formated_proxy[0] == 2:
        username = formated_proxy[1]
        password = formated_proxy[2]
        host = formated_proxy[3]
        port = formated_proxy[4]
        printl("info", f"Running Proxie of {host[:7] + '*' * (len(host) - 7)}:{port} | {username[:3] + '*' * (len(username) - 3)}:{password[:3] + '*' * (len(password) - 3)}")
    session = get_session()
    cookies = get_cookies(session)
    fingerprint = get_fingerprint(session)