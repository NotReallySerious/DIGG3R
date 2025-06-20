import pandas as pd
from bs4 import BeautifulSoup
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
    import time
    url = input("Insert URL: ").strip().replace("http://", "").replace("https://", "").strip("/")
    # Use RAW GitHub link for the actual wordlist
    wordlist_url = 'https://github.com/NotReallySerious/DIGG3R/blob/main/wordlist.txt'
    output = f"{url.replace('.', '_')}_subdomains.txt"

    try:
        print("[+] Downloading wordlist...")
        response = rq.get(wordlist_url, timeout=10)
        subdomains = response.text.splitlines()
    except Exception as e:
        print(Fore.RED + f"[!] Failed to download wordlist: {e}")
        return

    if not subdomains:
        print(Fore.RED + "[-] Wordlist is empty.")
        return

    # Wildcard detection
    try:
        wildcard_test = rq.get(f"http://xyz-notreal-subdomain.{url}", timeout=5)
        wildcard_hash = hash_content(wildcard_test.text)
    except:
        wildcard_hash = None

    found_count = 0

    with open(output, 'w') as out:
        print(Fore.YELLOW + "\n[+] Searching for Subdomains...\n" + Style.RESET_ALL)
        for subs in subdomains:
            for protocol in ['http://','https://']:
                full_url = f"{protocol}{subs}.{url}"
                try:
                    resp = rq.get(full_url, timeout=5)
                    current_hash = hash_content(resp.text)
                    if resp.status_code not in [200,400] and current_hash != wildcard_hash:
                        print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL} {full_url} (Status: {resp.status_code})")
                        out.write(full_url + '\n')
                        found_count += 1
                except rq.RequestException:
                    pass
            # Optional: rate limit to avoid blocking
            time.sleep(0.1)
            for protocol in ['http://','https://']:
                full_url = f"{protocol}{url}/{subs}"
                try:
                    resp = rq.get(full_url, timeout=5)
                    current_hash = hash_content(resp.text)
                    if resp.status_code < 400 and current_hash != wildcard_hash:
                        print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL} {full_url} (Status: {resp.status_code})")
                        out.write(full_url + '\n')
                        found_count += 1
                except rq.RequestException:
                    pass
            # Optional: rate limit to avoid blocking
            time.sleep(0.1)


    if found_count == 0:
        print(Fore.RED + "[-] No valid subdomains found. Try a larger or more accurate wordlist.")
    else:
        print(Fore.YELLOW + f"\n[+] Found {found_count} subdomain(s). Output file has been created.\n")


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
    print(Fore.YELLOW + "=" * 60)
    print(Fore.CYAN + "  Author     : MrHoodie")
    print(Fore.CYAN + "  Version    : 1.0")
    print(Fore.CYAN + "  GitHub     : https://github.com/NotReallySerious/Digg3r")
    print(Fore.CYAN + "  Searching has never been easier ")
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
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
