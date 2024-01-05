import random, yaml, time, threading
from modules.utilities import check_version, format_proxy
from modules.captcha_utilities import get_balance
from modules.console import printl, clear_screen

def test(proxie):
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
        printl("info", f"Running Proxie on {host[:7] + '*' * (len(host) - 7)}:{port} | {username[:3] + '*' * (len(username) - 3)}:{password[:3] + '*' * (len(password) - 3)}")

def main():
    check_version()
    printl("info", "Checking config...")
    try:
        config = yaml.safe_load((open("config.yml")))
    except:
        printl("error", "WHY DO YOU DELETE CONFIG FILE????? WTF")
        input("Press Enter to exit")
        exit(0)
    if not config["captcha_solver"]["provider"] in ["anti-captcha.com"]:
        printl("error", f"Invalid captcha provider detected ({config['captcha_solver']['provider']})")
        input("Press Enter to exit")
        exit(0)
    if config["captcha_solver"]["apikey"] == '':
        printl("error", "No captcha key detected")
        input("Press Enter to exit")
        exit(0)
    printl("info", "Checking captcha apikey...")
    balance = get_balance(config["captcha_solver"]["provider"], config["captcha_solver"]["apikey"])
    if not float(balance) >= .1:
        printl("error", "Your captcha account has less then 0.1$, Please charge your funds then try again.")
        answer = input("(#) Continue anyway? (Y/N) >> ")
        if answer.lower() == "n":
            exit(0)
    else:
        printl("info", f"Solver Balance ${balance}")
    proxies = open("proxies.txt").read().splitlines()
    if len(proxies) == 0 or proxies.__contains__("username:password@ip:port"):
        printl("error", "No proxies detected in proxies.txt")
        input("Press ENTER to exit")
        exit(0)
    time.sleep(3)
    clear_screen()
    proxie = random.choice(proxies)
    threading.Thread(target=test, args=(proxie,)).start()
    #console.information("Checking captcha key...")
    #if not float(get_balance()) >= .1:
    #    console.error("Your captcha account has less then 0.1$, Please charge your funds then try again.")
    #    answer = input("(#) Continue anyway? (Y/N) >> ")
    #    if answer.lower() == "n":
    #        exit(0)
    #console.clear()
    #threads = console.input("Threads")
    #try: 
    #    if int(threads) > 0: threads = int(threads)
    #except:
    #    console.error("Invalid input.")
    #    time.sleep(2)
    #    main()
    #console.clear()
    #proxies = itertools.cycle(open("proxies.txt").read().splitlines())
    #for _ in range(threads):
    #    threading.Thread(target=thread,args=(proxies,)).start()
if __name__ == "__main__":
    main()