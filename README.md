# Network Intrusion Log Analyser

A Python + MySQL tool that parses real network traffic logs, stores them in a relational database, and runs SQL-based anomaly detection to flag potential intrusions.

## Features
- Parses 50,000+ records from the KDD Cup 99 dataset
- Stores structured connection data in MariaDB
- Detects 3 attack patterns via SQL queries:
  - Port scans (zero-duration, low-byte bursts)
  - Brute force attempts (failed login spikes by service)
  - Data exfiltration suspects (high outbound byte transfers)
- Logs all findings to an `anomaly_log` table with timestamps
- Prints a formatted terminal report

## Tech Stack
- Python 3.13
- MariaDB / MySQL
- mysql-connector-python

## Dataset
KDD Cup 1999 — [Download here](https://www.kaggle.com/datasets/galaxyh/kdd-cup-1999-data)  
Place `kddcup.data_10_percent` in the `data/` folder.

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/TyrantAkuma/network-log-analyser.git
cd network-log-analyser

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install mysql-connector-python

# 3. Set up MariaDB
sudo mysql
```

```sql
CREATE DATABASE intrusion_logs;
CREATE USER 'loguser'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON intrusion_logs.* TO 'loguser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# 4. Update config.py with your DB credentials

# 5. Run
python3 main.py
```

## Sample Output

[1] Traffic breakdown by type:
normal                73978  ████████████████████████████████████████
smurf                 14198  ████████████████████
[2] Potential port scans:
udp/domain_u          1878 connections
tcp/http               869 connections
[3] Brute force attempts:
http             64860 failed attempts
smtp              5145 failed attempts
[4] Possible data exfiltration:
[normal] telnet — 2,661,605 bytes out

## Resume Bullet
> Built a network intrusion log analyser in Python + MariaDB, parsing 50,000+ records from the KDD Cup 99 dataset and detecting port scans, brute-force attempts, and exfiltration suspects using SQL anomaly queries.
