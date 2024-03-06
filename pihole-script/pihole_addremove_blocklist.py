import re
import logging
import argparse
import os
from dotenv import load_dotenv
from APiHole import PiHole


# Load environment variables from .env file
load_dotenv()


# Set the logging level for the package you want to change
piholelogger = logging.getLogger('PiHole')
piholelogger.setLevel(logging.WARNING)

PiHoleAPI = os.getenv('PIHOLE_API_KEY')


def generate_subdomain_regex(domain):
    # Escape special characters in the domain
    escaped_domain = re.escape(domain)
    # Create the regex pattern to match all subdomains
    regex_pattern = r"(\.|^)" + escaped_domain + r"$"
    return regex_pattern

def read_blocklist(filename):
    try:
        with open(filename, 'r') as file:
            items = file.readlines()
            items = [item.strip() for item in items]  # remove whitespace and newline characters
        return items
    except Exception as e:
        print(str(e))
        exit(0)


if __name__ == '__main__':
# Instantiate the ArgumentParser
    parser = argparse.ArgumentParser(description='Process command line arguments')
# Add the arguments
    parser.add_argument('--host', type=str, default='pi.hole', help='Host/IP of pi-hole')
    parser.add_argument('--blocklist', type=str, default='blocklist.txt', help='Name of the blocklist file')
    parser.add_argument('--add', action='store_true', help='Add blocklist')
    parser.add_argument('--remove', action='store_true', help='Remove blocklist')

# Parse the arguments and store them in the 'args' variable
    args = parser.parse_args()
    pihole_host = args.host

# Check if --add or --remove argument is provided and set the 'add_blocklist' variable accordingly
    if args.add:
        action = "ADD"
    elif args.remove:
        action = "REMOVE"
    else:
        action = "ADD"

    status = PiHole.GetStatus(pihole_host, PiHoleAPI)

    if status is None:
        print("ERROR CONNECTING TO PIHOLE")
        exit(0)

    blocklist = read_blocklist(args.blocklist)

    regex_blocklist = [generate_subdomain_regex(b) for b in blocklist]

    for rb in regex_blocklist:
        if action == "ADD":
            result = PiHole.AddRegexBlock(pihole_host,PiHoleAPI, rb)
        if action == "REMOVE":
            result = PiHole.RemoveRegexBlock(pihole_host,PiHoleAPI, rb)
        print(f'{action}\t--\t{rb}\t\t\t\t{"SUCCESS" if result else "FAIL"}')





