#!/usr/bin/env python3

import subprocess
import sys
import os

def run(cmd):
    print(f"\n[+] Running: {cmd}\n")
    subprocess.run(cmd, shell=True)


def check_tool(tool):
    return subprocess.call(f"which {tool}",
                           shell=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0


def check_dependencies():

    tools = ["subfinder", "amass", "httpx"]

    for tool in tools:
        if not check_tool(tool):
            print(f"[!] {tool} not installed")
            sys.exit()

    print("[+] All tools installed")


def main():

    if len(sys.argv) != 2:
        print("Usage: python3 subrecon.py domain.com")
        sys.exit()

    domain = sys.argv[1]

    os.makedirs("output", exist_ok=True)

    check_dependencies()

    print(f"\n[+] Starting Subdomain Recon for {domain}")

    # Subfinder
    run(f"subfinder -d {domain} -silent -o output/subfinder.txt")

    # Amass
    run(f"amass enum -passive -d {domain} -o output/amass.txt")

    # Merge results
    run("cat output/*.txt | sort -u > output/all_subdomains.txt")

    # Check live domains
    run("httpx -l output/all_subdomains.txt -silent -o output/live_subdomains.txt")

    print("\n[+] Recon Completed")
    print("[+] Results saved in output/ folder")


if __name__ == "__main__":
    main()
