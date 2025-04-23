import socket
import logging
import sys
import platform
import datetime
import argparse
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

# Logging: DEBUG to file, WARNING and above to console
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Console handler (WARNING and above only)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
logger.addHandler(console_handler)

# File handler (DEBUG and above)
file_handler = logging.FileHandler("scanner.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logger.addHandler(file_handler)

SCAN_TIMEOUT = int(os.environ.get("SCAN_TIMEOUT", "10"))

# Common TCP ports to scan if no custom ports are provided
COMMON_TCP_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443,
    445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443, 1025,
    1720, 3128, 49152, 49153, 49154, 49155, 49156, 49157,
    20, 554, 8888, 5000, 1110, 113, 6001, 4444, 888, 514,
    67, 68, 137, 138, 161, 162, 32768, 49158, 5357, 8000,
    8008, 49159, 49160, 49161, 49162, 49163, 49164, 49165,
    79, 7, 9, 13, 19, 49, 69, 70, 79, 81, 88, 109, 119, 1433,
    1521, 3000, 6667, 8009, 8081, 8181, 9090, 10000, 32764,
    49166, 49167, 49168, 49169, 49170, 49171, 49172, 49173,
    49174, 49175, 49176, 49177, 49178, 49179
]

# Argument parser
parser = argparse.ArgumentParser(description='Scan open ports')

parser.add_argument('-p', '--ports', metavar='ports',
                    default=os.environ.get("PORTS"),
                    help='Comma-separated list of ports to scan e.g., 22,80,443')

parser.add_argument('-P', '--portrange', metavar='range',
                    help='Range of ports: e.g. 1-1024')

parser.add_argument('-pT', '--portfile', metavar='file',
                    help='Path to file with one port per line')

parser.add_argument('-udp','--udpscan', action='store_true',
                    help='Include this flag to scan UDP ports')

parser.add_argument('-t', '--target', metavar='target',
                    default=os.environ.get("TARGET"),
                    help='Target IP or hostname or scan')

parser.add_argument('--log', action='store_true',
                    help='Enable logging to file')

args = parser.parse_args()

# Logging config (based on --log flag)
if args.log:
    logging.basicConfig(
        filename='scanner.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )
else:
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )


# Build port list according to priority
if args.portfile:
    with open(args.portfile) as f:
        ports = [int(line.strip()) for line in f if line.strip().isdigit()]
elif args.portrange:
    start, end = map(int, args.portrange.split('-'))
    ports = list(range(start, end + 1))
elif args.ports:
    ports = [int(p.strip()) for p in args.ports.split(',')]
else:
    ports = COMMON_TCP_PORTS

# Gather host info
hostname = socket.gethostname()
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.connect(('8.8.8.8', 12345))
ip_info = client.getsockname()
os = platform.system()

# Port Scanning TCP,UDP
open_tcp_ports = []
open_udp_ports = []
target_host = args.target

# TCP Scan
def openTCPPorts():
    print("PORT   STATE")
    logging.info("Starting TCP scan...")

    for port in ports:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(SCAN_TIMEOUT)
        result = client.connect_ex((target_host, port))

        status = 'open' if result == 0 else 'closed' # 0 = connected to port, success
        if status == 'open':
            open_tcp_ports.append(port)

        print(f"{port}/tcp {status}")
        logging.info(f"{port}/tcp {status}")
    print(f"Open TCP ports: {open_tcp_ports}")


    if not open_tcp_ports:
        return "No ports are open"
    return open_tcp_ports

# UDP Scan
def openUDPPorts():
    print("PORT    STATE")
    logging.info("Starting UDP port scan...")

    for port in ports:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(SCAN_TIMEOUT)
        try:
            result = client.sendto(b"AAABBBCCC", (target_host, port))
            data, addr = client.recvfrom(1024)
            open_udp_ports.append(port)
            logging.info(f"{port}/udp open")
        except Exception:
             logging.warning(f"{port}/udp is closed or no response")
             continue

    if not open_udp_ports:
        return "No ports are open"
    return open_udp_ports

# Run scanner and send payload to API
if __name__ == "__main__":
    try:
        open_tcp_ports = openTCPPorts()

        if args.udpscan:
            open_udp_ports = openUDPPorts() # If the --udp flag is supplied, then call the function
        else:
            open_udp_ports = [] # otherwise provide an empty payload, honouring payload structure

        host_info = {"hostname": hostname,
                        "ip": ip_info[0],
                        "os_name": os,
                        "tcp_ports": open_tcp_ports,
                        "udp_ports": open_udp_ports,
                        "timestamp": datetime.datetime.now().isoformat()
        }

        # Send payload to endpoint
        r = requests.post('http://localhost:5000/submit-scan', json=host_info)
        logging.info(f"Status Code: {r.status_code}")
        logging.debug(f"API Response: {r.json()}")

    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user. Bye for now! :)")
        sys.exit(0)

    except requests.exceptions.JSONDecodeError:
        logging.error("Response is not valid JSON.")
        logging.error(f"Raw response: {r.text}")

    except Exception as e:
        logging.exception(f"Something else went wrong: {e}")