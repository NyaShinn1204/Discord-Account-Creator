import requests, re
from modules.console import printl

def check_version():
  try:
    printl("info", "Checking version...")
    # githubからデータを取得
    get_version = requests.get("https://raw.githubusercontent.com/NyaShinn1204/Discord-Account-Creator/dev-v0.0.1/version").text.split("\n")[0]
    now_version = open("version","r").read().splitlines()[0]
    # デバイスとオンライン上と照合
    if now_version == get_version:
      printl("info", f"Using Latest Version: {now_version}")
    else:
      printl("error", f"You are using an older version, now version: {now_version}")
      printl("error", f"Latest Version: {get_version}")
  except:
    printl("error", "Failed to Check Version")
      
def format_proxy(data):
  # match_typeの初期設定
  match_type = None
  # ip:portのパターン
  ip_port_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+):(\d+)')
  # username:password@ip:portのパターン
  user_pass_ip_port_pattern = re.compile(r'(\w+):(\w+)@(\d+\.\d+\.\d+\.\d+):(\w+)')
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
  print("データの形式が不明です。")
