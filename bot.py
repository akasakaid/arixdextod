import os
import sys
import time
import requests
from colorama import *
from datetime import datetime

init(autoreset=True)

merah = Fore.LIGHTRED_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
putih = Fore.LIGHTWHITE_EX
biru = Fore.LIGHTBLUE_EX
hitam = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL

class ArixDexTod:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Priority": "u=1, i",
            "Referer": "https://miner-webapp-pi.vercel.app/",
            "Sec-Ch-Ua": '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        }
        self.line = putih + "~" * 50

    def next_claim_is(self, last_claim):
        next_claim = last_claim + 3600
        now = datetime.now().timestamp()
        tetod = round(next_claim - now)
        return tetod

    def get_user(self, id):
        url = f"https://miner-webapp-pi.vercel.app/api/user?id={id}"
        url_claim = f"https://miner-webapp-pi.vercel.app/api/claim?id={id}"
        res = self.http(url, self.headers)
        first_name = res.json().get("first_name", "Unknown")
        balance = res.json().get("balance", "Unknown")
        last_claim = res.json().get("last_claim", 0)
        self.log(f"{hijau}login as {putih}{first_name}")
        self.log(f"{hijau}balance : {putih}{balance}")
        can_claim = self.next_claim_is(last_claim)
        if can_claim >= 0:
            self.log(f"{kuning}not time to claim !")
            return can_claim

        res = self.http(url_claim, self.headers, "")
        balance = res.json().get("balance", "Unknown")
        self.log(f"{hijau}balance after claim : {putih}{balance}")
        return 3600

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{hitam}[{now}]{reset} {msg}")

    def http(self, url, headers, data=None):
        while True:
            try:
                if data is None:
                    res = requests.get(url, headers=headers)
                elif data == "":
                    res = requests.post(url, headers=headers)
                else:
                    res = requests.post(url, headers=headers, data=data)

                open("http.log", "a", encoding="utf-8").write(f"{res.text}\n")
                return res

            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                self.log(f"{merah}connection error / connection time out !")
                time.sleep(2)  # Fixed typo here
                continue

    def main(self):
        banner = f"""
    {hijau}Auto claim {putih}Arix coin{hijau} on Telegram Bot
    
    {biru}By: {putih}t.me/AkasakaID
    {biru}Github: {putih}@AkasakaID
    
        """
        arg = sys.argv
        if "marinkitagawa" not in arg:
            os.system("cls" if os.name == "nt" else "clear")
        print(banner)
        while True:
            ids = open("id.txt", "r").read().splitlines()
            list_countdown = []
            self.log(f"{hijau}account detected : {putih}{len(ids)}")
            print(self.line)
            if len(ids) <= 0:
                self.log(f"{merah}add your userid telegram account in id.txt file")
                sys.exit()

            _start = int(time.time())
            for id in ids:
                cd = self.get_user(id)
                list_countdown.append(cd)
                print(self.line)
                self.countdown(5)
            _end = int(time.time())
            _tot = _end - _start
            _min = min(list_countdown) - _tot
            print(f"list_countdown: {list_countdown}")
            print(f"_start: {_start}, _end: {_end}, _tot: {_tot}, _min: {_min}")
            if _min <= 0:
                continue

            self.countdown(_min)

if name == "__main__":
    try:
        ArixDexTod().main()
    except KeyboardInterrupt:
        sys.exit()
