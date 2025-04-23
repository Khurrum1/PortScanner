# Description and Purpose
A TCP/UDP port scanner which scans open ports and stores the information in a SQLite backend.

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
- Sqlite

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
git clone https://github.com/yourname/port-scanner.git
cd port-scanner
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
make run

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

Results can be viewed with ```bash docker logs container_name```

# Alerting Plans (Future work)
