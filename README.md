# Description and Purpose
A lightweight TCP/UDP port scanner which scans common open ports and stores the information in a SQLite backend for triage

# Features
- TCP scanning (default + custom ports)
- Optional UDP scanning
- CLI-based operation
- Cloud-native config via environment variables
- Logs to file with optional `--log` flag

# Help
```python
python3 scanner.py -h

usage: scanner.py [-h] [-p ports] [-P range] [-pT file] [--udp] [--log] -t target

Scan open ports

options:
  -h, --help            Show this help message and exit
  -p ports, --ports     Comma-separated list of ports to scan e.g., 22,80,443
  -P range, --portrange Range of ports e.g., 1-1024
  -pT file, --portfile  Path to a file with one port per line
  --udp                 Include this flag to scan UDP ports
  --log                 Enable logging to scanner.log
  -t target, --target   Target IP or hostname to scan
```

# Requirements
- Python 3.10+
- Flask
- requests
- python-dotenv
- SQLite

# Installation & Quick Start
## Start API in background
```bash
make run
```

## In a new terminal, run scanner with CLI flags
```python
python3 scanner.py --target x.x.x.x --ports 22,80
```


# Local Setup
```bash
git clone https://github.com/Khurrum1/PortScanner.git
cd PortScanner
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # copy file and provide real values
make run
```
This will run the API in the background; which is followed by starting the scanner in a new terminal.

# Docker
```bash
docker build -t port-scanner-api -f Dockerfile .
docker run -p 5000:5000 --env-file .env port-scanner-api
```
This will expose the API on http://localhost:5000

# Docker Compose
```bash
docker-compose up --build -d
```

- This will run two scanner containers, each simulating different open ports
- One API container to receive results

Results can be viewed with `docker logs container_name`

# Alerting Function (Future work)
Although alerting capabilities are not currently implemented in this project there is scope to introduce this feature.

## Proposed Features
### Rule-based Alerting
- Define a list of critical ports that should not be open.
- Raise an alert if any disallowed port is found in a scan.

### Threshold Alerts
- Alert if the number of open ports exceeds a defined threshold (e.g., more than 20).

### Anomaly Detection
- Track historical scans per host.
- Alert if a new open port appears compared to the last scan.

### Destination Options
- Email notifications using SMTP (e.g., SendGrid, Mailgun).
- Slack / Teams webhook integration for team alerts.
- SIEM forwarding (e.g., Splunk, ELK) via syslog or HTTP.

### Logging-Based Alerts
- Integrate with Promtail + Loki to forward logs to Grafana.
- Use Grafana Alerts for conditions on scanner logs (e.g., repeated closed port attempts)

