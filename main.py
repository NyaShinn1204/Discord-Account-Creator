import requests, os
from colorama import Fore

def get_filename():
  return os.path.basename(__file__)

def printl(num, data):
  if num == "error":
    print(f"[{Fore.LIGHTRED_EX}Error{Fore.RESET}] [{get_filename()}] " + data)
  if num == "debug":
    print(f"[{Fore.LIGHTCYAN_EX}Debug{Fore.RESET}] [{get_filename()}] " + data)
  if num == "info":
    print(f"[{Fore.LIGHTGREEN_EX}Info{Fore.RESET}] [{get_filename()}] " + data)

with open("version") as f:
    version = f.read()

def update_check():
  try:
    version_get = requests.get("https://raw.githubusercontent.com/NyaShinn1204/twocoin-assets/main/version").text
    if version_get.__contains__('\n'):
      version_get = version_get.replace('\n', '')
    if version == version_get:
      printl("info", "Latest Version")
    else:
      printl("error", "You are using an older version")
      printl("error", "Latest Version "+version_get)
  except:
    printl("error", "Failed to Get Version")
    
update_check()