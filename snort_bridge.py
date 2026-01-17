import time
import requests
import os
import sys
import signal
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ==============================================================================
# CONFIGURATION
# ==============================================================================
# YOUR NEW DEPLOYMENT URL
WEBHOOK_URL = 'https://script.google.com/macros/s/AKfycbxjE15Qhj698dsz_QJ7Ti2GX1dZHbqQ96PCwuIrlMzYlE84eOwb76CAdo4p-7R0qP09sQ/exec'

LOG_FILE = '/var/log/snort/alert.csv'
EMAIL_COOLDOWN = 60  # Seconds to wait before emailing about the same IP again


# ==============================================================================
# LOGGING & VISUALS
# ==============================================================================
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


# Configure system logging (Standard Output)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("SnortBridge")


def print_banner():
    os.system('clear')
    print(Colors.HEADER + "=" * 60 + Colors.ENDC)
    print(Colors.HEADER + "       SNORT BRIDGE PRO v5.3 (Smart)" + Colors.ENDC)
    print(Colors.HEADER + "=" * 60 + Colors.ENDC)
    print(Colors.BLUE + " Dev       : " + Colors.ENDC + "Sahil Thakur (aka geeksahil)")
    print(Colors.BLUE + " Mode      : " + Colors.ENDC + "Anti-Flood Active (60s Cooldown)")
    print(Colors.HEADER + "=" * 60 + Colors.ENDC + "\n")


# ==============================================================================
# MAIN APPLICATION CLASS
# ==============================================================================
class SnortBridge:
    def __init__(self, webhook_url, log_file):
        self.webhook_url = webhook_url
        self.log_file = log_file
        self.running = True

        # Tracking State for Anti-Flood
        self.last_email_time = {}
        self.attack_counter = {}

        # Setup High-Performance HTTP Session
        self.session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

        # Register Signal Handlers (Ctrl+C, System Kill)
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def shutdown(self, signum, frame):
        """Graceful shutdown handler."""
        print(f"\n{Colors.WARNING}>> Shutdown signal received. Closing bridge...{Colors.ENDC}")
        self.running = False

    def send_to_webhook(self, payload):
        """Sends data to Google with robust error handling."""
        try:
            response = self.session.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()  # Raise error for 4xx/5xx status codes
            return True
        except requests.exceptions.ConnectionError:
            print(f"{Colors.FAIL}[NET ERROR]{Colors.ENDC} Connection failed. Check internet.")
            logger.error("ConnectionError: Failed to reach Google Sheets.")
        except requests.exceptions.Timeout:
            print(f"{Colors.FAIL}[TIMEOUT]{Colors.ENDC} Google API timed out.")
            logger.error("TimeoutError: Request took too long.")
        except Exception as e:
            print(f"{Colors.FAIL}[ERROR]{Colors.ENDC} Upload failed: {e}")
            logger.error(f"UploadError: {str(e)}")
        return False

    def process_alert(self, raw_line):
        """Parses the CSV line and determines if email is needed."""
        # 1. Parse CSV safely
        try:
            parts = raw_line.split(',')
            # Index 1 is Message, Index 3 is Src IP (Based on Super Safe Mode)
            msg = parts[1].strip().replace('"', '')
            src_ip = parts[3].strip()
        except IndexError:
            logger.warning(f"Malformed log line skipped: {raw_line}")
            return
        except Exception:
            src_ip = "Unknown"
            msg = "Unknown Alert"

        # 2. Deduplication Logic (The "Smart" Part)
        attack_key = (src_ip, msg)
        self.attack_counter[attack_key] = self.attack_counter.get(attack_key, 0) + 1
        current_count = self.attack_counter[attack_key]

        # 3. Check Cooldown Timer
        current_time = time.time()
        last_sent = self.last_email_time.get(attack_key, 0)

        should_email = False
        status_msg = f"{Colors.WARNING}[LOG ONLY]{Colors.ENDC}"

        if (current_time - last_sent) > EMAIL_COOLDOWN:
            should_email = True
            self.last_email_time[attack_key] = current_time
            status_msg = f"{Colors.FAIL}[EMAIL SENT]{Colors.ENDC}"

        # 4. Console Output
        print(f"{Colors.GREEN}>> ALERT (x{current_count}):{Colors.ENDC} {src_ip} | {msg} | {status_msg}")

        # 5. Send Payload to Google
        payload = {
            'log_line': raw_line,
            'send_email': should_email
        }
        self.send_to_webhook(payload)

    def run(self):
        """Main Loop."""
        print_banner()

        # Wait for log file creation
        while not os.path.exists(self.log_file) and self.running:
            print(f"{Colors.WARNING}Waiting for {self.log_file} to be created...{Colors.ENDC}")
            time.sleep(5)

        print(f"{Colors.GREEN}[READY]{Colors.ENDC} Watching log file...")
        logger.info("SnortBridge Service Started.")

        try:
            with open(self.log_file, 'r') as f:
                f.seek(0, 2)  # Jump to end of file to ignore old alerts

                while self.running:
                    # Robust File Reading
                    try:
                        line = f.readline()

                        if not line:
                            # If file was rotated/deleted, check existence
                            if not os.path.exists(self.log_file):
                                raise FileNotFoundError("Log file disappeared")
                            time.sleep(0.5)
                            continue

                        self.process_alert(line.strip())
                        # Rate limit calls to Google to avoid 429 Errors (1 request per second)
                        time.sleep(1.0)

                    except FileNotFoundError:
                        print(f"{Colors.FAIL}Log file rotated or deleted. Reopening...{Colors.ENDC}")
                        time.sleep(2)
                        # Attempt to reopen
                        if os.path.exists(self.log_file):
                            f.close()
                            f = open(self.log_file, 'r')
                            f.seek(0, 2)  # Skip old logs in new file
                    except Exception as e:
                        logger.error(f"Unexpected error in loop: {e}")
                        time.sleep(1)

        except Exception as e:
            logger.critical(f"Fatal Error: {e}")
        finally:
            print(f"{Colors.BLUE}>> Bridge stopped. Clean exit.{Colors.ENDC}")


# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == '__main__':
    bridge = SnortBridge(WEBHOOK_URL, LOG_FILE)
    bridge.run()