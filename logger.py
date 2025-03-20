from datetime import datetime
from colorama import Fore, Back, Style, init
import logger as Logger

def get_time_formated() -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

def info(msg: str):
    print(f"{Fore.BLACK}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.BLACK}] {Fore.CYAN}INFO{Fore.BLACK}: {Fore.WHITE}{msg}")
    return
    
def warning(msg: str):
    print(f"{Fore.BLACK}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.BLACK}] {Fore.YELLOW}WARNING{Fore.BLACK}: {Fore.WHITE}{msg}")
    return
    
def error(msg: str):
    print(f"{Fore.BLACK}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.BLACK}] {Fore.RED}ERROR{Fore.BLACK}: {Fore.WHITE}{msg}")
    return
    
def success(msg: str):
    print(f"{Fore.BLACK}[{Fore.WHITE}{Logger.get_time_formated()}{Fore.BLACK}] {Fore.GREEN}SUCCESS{Fore.BLACK}: {Fore.WHITE}{msg}")
    return