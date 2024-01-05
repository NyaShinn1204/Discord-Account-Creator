import requests, yaml
from colorama import Fore

def printl(num, data):
  if num == "error":
    print(f"[{Fore.LIGHTRED_EX}Error{Fore.RESET}] " + data)
  if num == "info":
    print(f"[{Fore.LIGHTGREEN_EX}Info{Fore.RESET}] " + data)

def check_version():
  try:
    printl("info", "Checking version...")
    get_version = requests.get("https://raw.githubusercontent.com/NyaShinn1204/Discord-Account-Creator/dev-v0.0.1/version").text.split("\n")[0]
    now_version = open("version","r").read().splitlines()[0]
    if now_version == get_version:
      printl("info", "Using Latest Version: "+now_version)
    else:
      printl("error", "You are using an older version, now version: "+now_version)
      printl("error", "Latest Version: "+get_version)
  except:
    printl("error", "Failed to Check Version")
    

def main():
    check_version()
    printl("info", "Checking config...")
    try:
        config = yaml.safe_load((open("config.yml")))
    except:
        printl("error", "WHY DO YOU DELETE CONFIG FILE????? WTF")
        input("Press Enter to exit")
        exit(0)
    print(config["email_verify"]["m.kuku.lu_token"])
    print(config["email_verify"]["m.kuku.lu_sessionhash"])
    if not config["captcha_solver"]["provider"] in ["anti-captcha.com"]:
        printl("error", f"Invalid captcha provider detected ({config['captcha_solver']['provider']})")
        input("Press Enter to exit")
        exit(0)
    if config["captcha_solver"]["apikey"] == '':
        printl("error", "No captcha key detected")
        input("Press Enter to exit")
        exit(0)
    #proxies = open("proxies.txt").read().splitlines()
    #if len(proxies) == 0:
    #    console.error("No proxies detected in proxies.txt")
    #    input("Press ENTER to exit.")
    #    exit(0)
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