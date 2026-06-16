import argparse
import requests
import socket
import json
import os
from rich.console import Console 

#Initialize the Rich console for colors
console = Console()

def save_report(data, filename):
    #Create a reports folder if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    filepath = os.path.join("reports", filename)

    #Save data dictionary as a JSON file
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    console.print(f"\n[bold magenta][*] Report successfully saved to {filepath}[/bold magenta]")
    


def check_username(username):
    console.print(f"\n[bold cyan][*] Scanning across multiple platforms for: {username}...[/bold cyan]\n")
    #Creating a dictionary of platforms and their URL structures
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Snapchat": f"https://story.snapchat.com/@{username}",
        "Linktree": f"https://linktr.ee/{username}"
    }

    #Dictionary to hold data for our JSON report
    results = {"target": username, "type": "username", "found_on": [], "not_found_on": []}

#looping through each platform
    for platform, url in platforms.items():
        try:
        # We need user-Agent so website don't immediately block out bot
            headers = {"User-Agent": "Mozilla/5.0"}
        #HTTP GET request to the profile
            response = requests.get(url, headers=headers, timeout=5)

        # 200 OK would mean the page exists
            if response.status_code == 200:
                console.print(f"[bold green][+][/bold green] FOUND on {platforms}: {url}")
                results["found_on"].append(platform)
        #404 Not Found means the username available/doesn't exist
            elif response.status_code == 404:
                console.print(f"[bold red][-][/bold red] NOT FOUND on {platforms}")
                results["not_found_on"].append(platform)
            else:
                console.print(f"[bold yellow][?][/bold yellow] UNKNOWN: Received status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            console.print(f"[bold red][!][/bold red] Connection Error with {platform}: {e}")

    return results

def check_domain(domain):
    console.print(f"\n[bold cyan][*] Investigating Domain: {domain}...[/bold cyan]\n")
    results = {"target": domain, "type": "domain", "ip": None, "isp": None, "location": None}

    try:
        #Resolve domain to an IP address
        ip_address = socket.gethostbyname(domain)
        console.print(f"[bold green][+][/bold green] Target IP Address: {ip_address}")
        results["ip"] = ip_address

        #free api to locate the IP address
        geo_url = f"http://ip-api.com/json/{ip_address}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response= requests.get(geo_url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                isp = data.get('isp', 'Unknown')
                loc = f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}"

            console.print(f"[bold green][+][/bold green] ISP/Hosting: {isp}")
            console.print(f"[bold green][+][/bold green] Location: {loc}")                        

            results["isp"] = isp
            results["location"] = loc 
        else:
            console.print(f"[bold red][-][/bold red] Could not retrieve geolocation details.")
       
    except socket.gaierror:
        console.print("[bold red][!][/bold red] Error: Invalid domain name or connection failure.")
    except Exception as e:
        console.print(f"[bold red][!][/bold red] Error gathering intel: {e}")
    return results

def main():
    #setting up argument parser
    parser = argparse.ArgumentParser(description="A Simple OSINT Recon Tool")

    #argument for target username
    parser.add_argument("-u", "--username", help="The username to investigate")

    #argument for targetting domain
    parser.add_argument("-d", "--domain", help="The domain name to investigate")

    #Adding new output flag
    parser.add_argument("-o", "--output", help="Save results to a JSON file (e.g., target_report.json)")
    #parse the inputs
    args = parser.parse_args()

    report_data = None

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