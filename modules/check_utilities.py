import requests
from modules.console import printl

def check_version():
  try:
    printl("info", "Checking version...")
    get_version = requests.get("https://raw.githubusercontent.com/NyaShinn1204/Discord-Account-Creator/dev-v0.0.1/version").text.split("\n")[0]
    now_version = open("version","r").read().splitlines()[0]
    if now_version == get_version:
      printl("info", f"Using Latest Version: {now_version}")
    else:
      printl("error", f"You are using an older version, now version: {now_version}")
      printl("error", f"Latest Version: {get_version}")
  except:
    printl("error", "Failed to Check Version")