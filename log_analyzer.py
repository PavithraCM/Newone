import os
import re
from collections import Counter

# File paths
LOG_FILE = "server_access.log"

# Standard Combined Log Format regex pattern
# Example: 127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /index.html HTTP/1.0" 200 2326
LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+\[.*?\]\s+"(?P<method>\S+)\s+(?P<request>\S+)\s+.*?#?"\s+(?P<status>\d{3})\s+(?P<size>\S+)'
)


def create_sample_log_if_missing():
    """Generates a mock web server log file for testing purposes if none exists."""
    if not os.path.exists(LOG_FILE):
        sample_logs = [
            '192.168.1.10 - - [09/Sep/2026:14:32:10 +0530] "GET /home HTTP/1.1" 200 4523\n',
            '192.168.1.15 - - [09/Sep/2026:14:33:12 +0530] "GET /about HTTP/1.1" 200 3122\n',
            '192.168.1.10 - - [09/Sep/2026:14:34:01 +0530] "GET /contact HTTP/1.1" 404 1204\n',
            '10.0.0.5 - - [09/Sep/2026:14:35:55 +0530] "GET /home HTTP/1.1" 200 4523\n',
            '192.168.1.10 - - [09/Sep/2026:14:36:20 +0530] "GET /home HTTP/1.1" 200 4523\n',
            '172.16.0.42 - - [09/Sep/2026:14:37:11 +0530] "GET /login HTTP/1.1" 404 1204\n',
            '10.0.0.5 - - [09/Sep/2026:14:38:00 +0530] "GET /gallery HTTP/1.1" 200 8943\n',
        ]
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.writelines(sample_logs)
        print(f"[INFO] Generated a sample web server log file: '{LOG_FILE}'")


def analyze_log():
    create_sample_log_if_missing()

    total_requests = 0
    error_404_count = 0
    ip_counter = Counter()
    request_counter = Counter()

    try:
        with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = LOG_PATTERN.match(line)
                if not match:
                    continue

                total_requests += 1
                data = match.groupdict()

                # Aggregate metrics
                ip_counter[data["ip"]] += 1
                request_counter[data["request"]] += 1

                if data["status"] == "404":
                    error_404_count += 1

    except FileNotFoundError:
        print(f"[ERROR] The file '{LOG_FILE}' was not found.")
        return

    # Generate Summary Report
    print("=" * 50)
    print("               WEB SERVER LOG REPORT            ")
    print("=" * 50)
    print(f"Total Logged Requests: {total_requests}")
    print(f"Total 404 Errors:      {error_404_count}")
    print("-" * 50)

    print("\nTop Most Requested Pages:")
    for page, count in request_counter.most_common(3):
        print(f"  - {page}: {count} times")

    print("\nTop Most Active IP Addresses:")
    for ip, count in ip_counter.most_common(3):
        print(f"  - {ip}: {count} requests")
    print("=" * 50)


if __name__ == "__main__":
    analyze_log()
