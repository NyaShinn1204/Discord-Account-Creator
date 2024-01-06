import os
from colorama import Fore

def printl(num, data):
  if num == "error":
    print(f"[{Fore.LIGHTRED_EX}Error{Fore.RESET}] " + data)
  if num == "info":
    print(f"[{Fore.LIGHTGREEN_EX}Info{Fore.RESET}] " + data)
    
def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')