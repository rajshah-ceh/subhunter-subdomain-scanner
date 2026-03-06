#!/usr/bin/env python3

import requests
import sys
import concurrent.futures

# Wordlist of common subdomains
subdomains = [
"www","mail","ftp","webmail","test","dev","api","blog","stage",
"beta","admin","portal","vpn","m","mobile","support","shop",
"dashboard","secure","server","cloud","app"
]

TIMEOUT = 3
THREADS = 20

def check_subdomain(sub, domain):
    url = f"http://{sub}.{domain}"

    try:
        r = requests.get(url, timeout=TIMEOUT)

        if r.status_code < 400:
            print(f"[+] Found: {url}")

            with open("found_subdomains.txt","a") as f:
                f.write(url + "\n")

    except:
        pass


def main():

    if len(sys.argv) != 2:
        print("Usage: python3 subhunter.py domain.com")
        sys.exit()

    domain = sys.argv[1]

    print(f"\nScanning subdomains for {domain}\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        for sub in subdomains:
            executor.submit(check_subdomain, sub, domain)


if __name__ == "__main__":
    main()
