import socket
import requests as rq
import urllib.parse
import colorama
import os
import hashlib
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

def hash_content(text):
    return hashlib.md5(text.encode()).hexdigest()

def subdomain_finder():
    url = input("Insert URL (e.g., wikipedia.org):").strip()
    wordlist_path = '../DIGG3R/wordlist.txt'
    output = f"{url.replace('.', '_')}_subdomains_with_ips.txt"

    try:
        with open(wordlist_path, 'r') as file:
            subdomains = file.read().splitlines()
    except FileNotFoundError:
        print("File not found.")
        return

    with open(output, 'w') as out:
        print("\n[+] Slowly searching for subdomains (stealth mode)...\n")
        for subs in subdomains:
            full_subdomain = f"{subs}.{url}"
            for protocol in ["http://", "https://"]:
                full_url = f"{protocol}{full_subdomain}"
                try:
                    resp = rq.get(full_url, timeout=5)
                    if resp.status_code < 400:
                        try:
                            ip = socket.gethostbyname(full_subdomain)
                        except socket.gaierror:
                            ip = "IP not found"
                        print(f"[FOUND] {full_url} -> {ip} (Status: {resp.status_code})")
                        out.write(f"{full_url} -> {ip} (Status: {resp.status_code})\n")
                except rq.exceptions.RequestException:
                    pass  # silently skip unreachable subdomains
        for subs in subdomains:
            full_subdomain = f"{url}/{subs}"
            for protocol in ["http://", "https://"]:
                full_url = f"{protocol}{full_subdomain}"
                try:
                    resp = rq.get(full_url, timeout=5)
                    if resp.status_code < 400:
                        try:
                            ip = socket.gethostbyname(full_subdomain)
                        except socket.gaierror:
                            ip = "IP not found"
                        print(f"[FOUND] {full_url} -> {ip} (Status: {resp.status_code})")
                        out.write(f"{full_url} -> {ip} (Status: {resp.status_code})\n")
                except rq.exceptions.RequestException:
                    pass  # silently skip unreachable subdomains
            

    print(f"\n[✓] Scan complete. Results saved to: {output}")


def username_search():
    
    name = input("Enter the Username: ")
    encoded_name = urllib.parse.quote(name)
    output = f"{name}_report.txt"
    link_db_path = '../DIGG3R/link_lists.txt'

    # Generate a fake username to detect wildcard pages
    fake_username = 'nonexistentuser1234567890'
    fake_hashes = set()

    # Load sites
    with open(link_db_path, 'r') as file:
        links = file.read().splitlines()

    print("Detecting wildcard responses...")
    for link in links:
        fake_url = link.format(urllib.parse.quote(fake_username))
        try:
            resp = rq.get(fake_url, timeout=5)
            fake_hashes.add(hash_content(resp.text))
        except:
            continue

    print("Searching Usernames Online. Please wait...\n")
    found_count = 0

    with open(output, 'w') as out:
        for link in links:
            real_url = link.format(encoded_name)
            try:
                resp = rq.get(real_url, timeout=5)
                body_hash = hash_content(resp.text)
                if resp.status_code == 200 and body_hash not in fake_hashes:
                    print(f"{Fore.GREEN}[+] Username Found in {real_url}{Style.RESET_ALL}")
                    out.write(real_url + '\n')
                    found_count += 1
            except rq.RequestException:
                continue

    if found_count == 0:
        print(Fore.RED + "[-] No real accounts found. All hits matched wildcard patterns.")
    else:
        print(Fore.YELLOW + f"[+] Found {found_count} username(s). Output file created.")
        
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = pyfiglet.figlet_format("DIGG3R", font="smslant")
    print(Fore.CYAN + banner)
    print(Fore.YELLOW + "=" * 80)
    print(Fore.CYAN + "  Author     : MrHoodie")
    print(Fore.CYAN + "  Version    : 1.0")
    print(Fore.CYAN + "  GitHub     : https://github.com/NotReallySerious/Digg3r")
    print(Fore.CYAN + "  Searching has never been easier ")
    print(Fore.RED + "  WARNING     : DONT USE THIS TOOL FOR ILLEGAL PURPOSES")
    print(Fore.RED + "           THIS TOOL IS FOR ETHICAL AND EDUCATIONAL USE ONLY")
    print(Fore.YELLOW + "=" * 80 + Style.RESET_ALL)
    print('\n')
    print('SERVICES: ')
    print("1. Subdomain Finder")
    print("2. Online Username Finder")
    print("3. Exit")

    while True:
        try:
            choice = int(input("Enter Your choice: "))
            if choice == 1:
                subdomain_finder()
            elif choice == 2:
                username_search()
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
