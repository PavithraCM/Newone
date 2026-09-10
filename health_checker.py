import sys
import urllib.request
import urllib.error

# ==================== CONFIGURATION ====================
# The URL of the application you want to monitor
APP_URL = "https://google.com"  # Replace with your app's address (e.g., http://localhost:4499)

# How many seconds to wait before giving up on a non-responding app
TIMEOUT_SECONDS = 5
# =======================================================

def check_application_health(url):
    print("=" * 60)
    print(f"Checking Application Status for: {url}")
    print("=" * 60)
    
    try:
        # Attempt to connect to the target web address
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            status_code = response.getcode()
            
            # 200 OK means the site is up and healthy
            if status_code == 200:
                print(f"STATUS: UP (HTTP Status Code: {status_code})")
                print("The application is healthy and functioning correctly.")
            else:
                # Catches unusual non-200 successful statuses
                print(f"STATUS: UP/REDIRECT (HTTP Status Code: {status_code})")
                print("The application is responding but returned a redirection status.")
                
    except urllib.error.HTTPError as e:
        # The server responded, but returned an error page (e.g., 404 Not Found, 500 Internal Error)
        print(f"STATUS: DOWN (HTTP Status Code: {e.code})")
        print("The application server is alive but returning error codes.")
        
    except urllib.error.URLError as e:
        # The application is completely unreachable (DNS failed, port closed, or server offline)
        print("STATUS: DOWN")
        print(f"The application is completely unreachable. Reason: {e.reason}")
        
    except Exception as e:
        # Fallback for any other unexpected issues
        print("STATUS: DOWN")
        print(f"An unexpected tracking error occurred: {e}")
        
    print("=" * 60)

if __name__ == "__main__":
    check_application_health(APP_URL)
