import argparse
import requests

def check_username(username):
    print(f"\n[*] Scanning across multiple platforms for: {username}...\n")

    #Creating a dictionary of platforms and their URL structures
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Snapchat": f"https://story.snapchat.com/@{username}",
        "Linktree": f"https://linktr.ee/{username}"
    }

#looping through each platform
    for platforms, url in platforms.items():
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

def main():
    #setting up argument parser
    parser = argparse.ArgumentParser(description="A Simple OSINT Recon Tool")

    #argument for target username
    parser.add_argument("-u", "--username", help="The username to investigate")

    #parse the inputs
    args = parser.parse_args()

    #check if user actually provide a username
    if args.username:
        print(f"[*] Target Username Locked: {args.username}")
        check_username(args.username)
    else:
        print("[!] Error: Please provide a username using -u or --username")

if __name__ == "__main__":
    main()        