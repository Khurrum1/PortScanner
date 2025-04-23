from dotenv import load_dotenv
load_dotenv()

import sqlite3
import json
import os


# Mock data
# scan_data = {
#         "hostname": "my-host",
#         "ip": "x.x.x.x",
#         "os": "linux",
#         "timestamp": "2025-04-18T10:00:00Z",
#         "tcp_ports": [22, 80],
#         "udp_ports": [53]
#         }

# Load environment variables from .env file
load_dotenv()

def insert_scan_results(scan_data): # scan_data = payload
    """
    Inserts scan results into the SQLite database.

    Parameters:
        scan_data (dict): A dictionary containing scan details with keys:
            - hostname (str)
            - ip (str)
            - os_name (str)
            - timestamp (str)
            - tcp_ports (list)
            - udp_ports (list)
    """
    # Extract and serialise scan data
    hostname = scan_data.get("hostname")
    ip = scan_data.get("ip")
    tcp_ports = json.dumps(scan_data.get("tcp_ports", []))
    udp_ports = json.dumps(scan_data.get("udp_ports", []))
    timestamp = scan_data.get("timestamp")
    os_name = scan_data.get("os_name")

    # holds real data from the endpoint(s)
    values = (hostname, ip, tcp_ports, udp_ports, timestamp, os_name)

    # Define database path with a fallback
    db_path = os.environ.get("DB_PATH", "open_ports.db")
    conn_obj = sqlite3.connect(db_path)
    cursor_obj = conn_obj.cursor()


    # Create table to store scan results and execute it; OS and udp left nullable for flexibility
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostname TEXT NOT NULL,
        ip TEXT NOT NULL,
        os_name TEXT,
        timestamp TEXT NOT NULL,
        tcp_ports TEXT NOT NULL,
        udp_ports TEXT
    );""")

    # Queries to INSERT records into columns
    cursor_obj.execute("""INSERT INTO scans (hostname, ip, tcp_ports, udp_ports, timestamp, os_name)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """, values)


    # Optional: Display all rows (debug only)
    print("Full scan table: ")
    for row in cursor_obj.execute("SELECT * FROM scans"):
        print(row)

    conn_obj.commit()
    conn_obj.close()

# insert_scan_results(scan_data) <- use for testing mock data