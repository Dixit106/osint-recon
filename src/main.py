import argparse
import requests
import socket

def check_username(username):
    print(f"\n[*] Scanning across multiple platforms for: {username}...\n")

    #Creating a dictionary of platforms and their URL structures
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Snapchat": f"https://story.snapchat.com/@{username}",
        "Linktree": f"https://linktr.ee/{username}"
    }

#looping through each platform
    for platform, url in platforms.items():
        try:
        # We need user-Agent so website don't immediately block out bot
            headers = {"User-Agent": "Mozilla/5.0"}
        #HTTP GET request to the profile
            response = requests.get(url, headers=headers, timeout=5)

        # 200 OK would mean the page exists
            if response.status_code == 200:
                print(f"[+] FOUND on {platforms}: {url}")
        #404 Not Found means the username available/doesn't exist
            elif response.status_code == 404:
                print(f"[-] NOT FOUND on {platforms}")
            else:
                print(f"[?] UNKNOWN: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[!] Connection Error: {e}")

def check_domain(domain):
    print(f"\n[*] Investigating Domain: {domain}...\n")
    try:
        #Resolve domain to an IP address
        ip_address = socket.gethostbyname(domain)
        print(f"[+] Target IP Address: {ip_address}")

        #free api to locate the IP address
        geo_url = f"http://ip-api.com/json/{ip_address}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response= requests.get(geo_url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            print(f"[+] ISP/Hosting: {data.get('org', 'Unknown')}")
            print(f"[+] Location: {data.get('city', 'Unknown')}, {data.get('region', "Unknown")}, {data.get('country_name','Unknown')}")                        

        else:
            print("[-] Could not retrieve geolocation details.")

    except socket.gaierror:
        print("[!] Error: Invalid domain name or connection failure.")
    except Exception as e:
        print(f"[!] Error gathering intel: {e}")

def main():
    #setting up argument parser
    parser = argparse.ArgumentParser(description="A Simple OSINT Recon Tool")

    #argument for target username
    parser.add_argument("-u", "--username", help="The username to investigate")

    #argument for targetting domain
    parser.add_argument("-d", "--domain", help="The domain name to investigate")

    #parse the inputs
    args = parser.parse_args()

    #check if user actually provide a username
    if args.username:
        print(f"[*] Target Username Locked: {args.username}")
        check_username(args.username)
    elif args.domain:
        print(f"[*] Target Domain Locked: {args.domain}")
        check_domain(args.domain)    
    else:
        print("[!] Error: Please provide an argument. Use -h or --help for instructions.")

if __name__ == "__main__":
    main()        