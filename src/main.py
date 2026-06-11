import argparse

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
    else:
        print("[!] Error: Please provide a username using -u or --username")

if __name__ == "__main__":
    main()        