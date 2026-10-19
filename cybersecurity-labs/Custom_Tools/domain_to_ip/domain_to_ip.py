import socket
import pyfiglet
from termcolor import colored

print("***********************CONVERTOR*************************")

banner = colored(pyfiglet.figlet_format("Domain To Ip"), "green")
print(banner)

domain_name = input("Enter Your Target Domain: ")

try:
    ip = socket.gethostbyname(domain_name)
    print(colored(f"\n[+] IP Address: {ip}", "red"))
except socket.gaierror:
    print(colored("\n[!] Could not resolve domain. Check spelling & internet.", "yellow"))

print("\n***********************DONE*************************")
