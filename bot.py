
from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout,
    BasicAuth
)
from aiohttp_socks import ProxyConnector
from fake_useragent import FakeUserAgent
from eth_account import Account
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from datetime import datetime
from colorama import *
import asyncio, json, re, os, pytz

# Initialization of Colorama
init(autoreset=True)

wib = pytz.timezone('Asia/Jakarta')

class X1:
    def __init__(self) -> None:
        self.BASE_API = "https://tapi.kod.af"
        self.HEADERS = {}
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        time_str = datetime.now().astimezone(wib).strftime('%H:%M:%S')
        print(
            f"{Fore.BLACK + Style.BRIGHT}[{time_str}]{Style.RESET_ALL} "
            f"{Fore.CYAN}➤{Style.RESET_ALL} {message}",
            flush=True
        )

    def welcome(self):
        banner = f"""
{Fore.CYAN + Style.BRIGHT}    ╔══════════════════════════════════════════════════════╗
    ║  {Fore.YELLOW}██╗  ██╗ ██╗{Fore.CYAN}      {Fore.WHITE}███████╗ ██████╗ ██████╗ {Fore.CYAN}     ║
    ║  {Fore.YELLOW}╚██╗██╔╝███║{Fore.CYAN}      {Fore.WHITE}██╔════╝██╔════╝██╔═══██╗{Fore.CYAN}     ║
    ║  {Fore.YELLOW} ╚███╔╝ ╚██║{Fore.CYAN}      {Fore.WHITE}█████╗  ██║     ██║   ██║{Fore.CYAN}     ║
    ║  {Fore.YELLOW} ██╔██╗  ██║{Fore.CYAN}      {Fore.WHITE}██╔══╝  ██║     ██║   ██║{Fore.CYAN}     ║
    ║  {Fore.YELLOW}██╔╝ ██╗ ██║{Fore.CYAN}      {Fore.WHITE}███████╗╚██████╗╚██████╔╝{Fore.CYAN}     ║
    ║  {Fore.YELLOW}╚═╝  ╚═╝ ╚═╝{Fore.CYAN}      {Fore.WHITE}╚══════╝ ╚═════╝ ╚═════╝ {Fore.CYAN}     ║
    ║                                                      ║
    ║  {Fore.GREEN + Style.BRIGHT}» X1 EcoChain Auto Bot - Premium v2.0 {Fore.CYAN}              ║
    ║  {Fore.MAGENTA + Style.BRIGHT}» Created with ❤️ by {Fore.WHITE}A K H I I {Fore.CYAN}                      ║
    ╚══════════════════════════════════════════════════════╝
        """
        print(banner)

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    
    async def load_proxies(self):
        filename = "proxy.txt"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}✘ File {filename} not found.")
                return
            with open(filename, 'r') as f:
                self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED}✘ No proxies in file.")
                return

            self.log(f"{Fore.BLUE}ℹ Total Proxies: {Fore.WHITE}{len(self.proxies)}")
        
        except Exception as e:
            self.log(f"{Fore.RED}✘ Proxy Load Error: {e}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, account):
        if account not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[account] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[account]

    def rotate_proxy_for_account(self, account):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxy_index)
        self.account_proxies[account] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def build_proxy_config(self, proxy=None):
        if not proxy: return None, None, None
        if proxy.startswith("socks"):
            return ProxyConnector.from_url(proxy), None, None
        elif proxy.startswith("http"):
            match = re.match(r"http://(.*?):(.*?)@(.*)", proxy)
            if match:
                u, p, hp = match.groups()
                return None, f"http://{hp}", BasicAuth(u, p)
            return None, proxy, None
        raise Exception("Unsupported Proxy.")
        
    def generate_address(self, account: str):
        try:
            return Account.from_key(account).address
        except: return None
    
    def generate_signature(self, account: str):
        try:
            encoded = encode_defunct(text="X1 Testnet Auth")
            return to_hex(Account.sign_message(encoded, private_key=account).signature)
        except Exception as e: raise Exception(f"Sign Error: {str(e)}")
        
    def mask_account(self, account):
        return f"{account[:6]}...{account[-4:]}"

    def print_question(self):
        self.clear_terminal()
        self.welcome()
        print(f"{Fore.WHITE}┌───────────────────────────────────┐")
        print(f"{Fore.WHITE}│ {Fore.YELLOW}1. {Fore.WHITE}Run With Proxy                 │")
        print(f"{Fore.WHITE}│ {Fore.YELLOW}2. {Fore.WHITE}Run Without Proxy              │")
        print(f"{Fore.WHITE}└───────────────────────────────────┘")
        
        while True:
            try:
                choice = int(input(f"{Fore.CYAN}Choice [1/2]: {Style.RESET_ALL}"))
                if choice in [1, 2]: break
            except: pass

        rotate = False
        if choice == 1:
            r = input(f"{Fore.CYAN}Rotate proxy on error? (y/n): {Style.RESET_ALL}").lower()
            rotate = r == 'y'
        return choice, rotate
    
    async def check_connection(self, proxy_url=None):
        connector, proxy, auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=15)) as session:
                async with session.get("https://api.ipify.org?format=json", proxy=proxy, proxy_auth=auth) as r:
                    return r.status == 200
        except: return False
    
    async def auth_signin(self, address: str, signature: str, proxy_url=None):
        url = f"{self.BASE_API}/signin"
        headers = {**self.HEADERS[address], "Content-Type": "application/json"}
        data = json.dumps({"signature": signature})
        connector, proxy, auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                async with session.post(url, headers=headers, data=data, proxy=proxy, proxy_auth=auth) as r:
                    return await r.json() if r.status == 201 or r.status == 200 else None
        except: return None
    
    async def user_data(self, address: str, proxy_url=None):
        url = f"{self.BASE_API}/me"
        headers = {**self.HEADERS[address], "Authorization": self.access_tokens[address]}
        connector, proxy, auth = self.build_proxy_config(proxy_url)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                async with session.get(url, headers=headers, proxy=proxy, proxy_auth=auth) as r:
                    return await r.json()
        except: return None

    async def quest_action(self, address, proxy, action="list", q_id=None):
        url = f"{self.BASE_API}/quests"
        headers = {**self.HEADERS[address], "Authorization": self.access_tokens[address]}
        connector, p, a = self.build_proxy_config(proxy)
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=30)) as session:
                if action == "list":
                    async with session.get(url, headers=headers, proxy=p, proxy_auth=a) as r:
                        return await r.json()
                else:
                    async with session.post(url, headers=headers, params={"quest_id": q_id}, proxy=p, proxy_auth=a) as r:
                        return await r.json() if r.status == 200 else None
        except: return None

    async def process_accounts(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        proxy = self.get_next_proxy_for_account(address) if use_proxy else None
        
        if use_proxy and not await self.check_connection(proxy):
            if rotate_proxy: proxy = self.rotate_proxy_for_account(address)
            else: 
                self.log(f"{Fore.RED}✘ Proxy Connection Failed.")
                return

        sig = self.generate_signature(account)
        login = await self.auth_signin(address, sig, proxy)
        
        if not login:
            self.log(f"{Fore.RED}✘ Authentication Failed.")
            return

        self.access_tokens[address] = login["token"]
        self.log(f"{Fore.GREEN}✔ Login Successful")

        user = await self.user_data(address, proxy)
        if user:
            self.log(f"{Fore.CYAN}💰 Balance: {Fore.WHITE}{user.get('points')} Points")

        quests = await self.quest_action(address, proxy)
        if quests:
            for q in quests:
                title = q.get('title')
                if q.get('is_completed') or q.get('is_completed_today'):
                    self.log(f"{Fore.BLACK + Style.BRIGHT}● {title[:30]}... {Fore.BLUE}(Completed)")
                    continue
                
                if await self.quest_action(address, proxy, "claim", q.get('id')):
                    self.log(f"{Fore.GREEN}● {title[:30]}... {Fore.WHITE}+ {q.get('reward')} pts")

    async def main(self):
        try:
            with open('accounts.txt', 'r') as f:
                accounts = [l.strip() for l in f if l.strip()]

            p_choice, r_proxy = self.print_question()

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(f"{Fore.BLUE}Loaded Accounts: {Fore.WHITE}{len(accounts)}")
                if p_choice == 1: await self.load_proxies()

                for acc in accounts:
                    addr = self.generate_address(acc)
                    if not addr: continue
                    
                    print(f"\n{Fore.YELLOW}┌── {Fore.WHITE}Account: {Fore.CYAN}{self.mask_account(addr)}")
                    self.HEADERS[addr] = {"User-Agent": FakeUserAgent().random, "Origin": "https://testnet.x1ecochain.com"}
                    await self.process_accounts(acc, addr, p_choice == 1, r_proxy)
                    print(f"{Fore.YELLOW}└───────────────────────────────────")

                delay = 24 * 3600
                while delay > 0:
                    print(f"{Fore.MAGENTA}⏳ Next cycle in: {Fore.WHITE}{self.format_seconds(delay)} ", end="\r")
                    await asyncio.sleep(1)
                    delay -= 1

        except Exception as e: self.log(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(X1().main())
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Shutdown Requested...")
