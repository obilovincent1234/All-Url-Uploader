import os
import logging
import requests
from dotenv import load_dotenv

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

load_dotenv()

class Config(object):
    # Get a token from @BotFather
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    # The Telegram API things
    API_ID = os.environ.get("API_ID")
    API_HASH = os.environ.get("API_HASH")
    # Get these values from my.telegram.org
    # Array to store users who are authorized to use the bot

    # File /video download location
    DOWNLOAD_LOCATION = "./DOWNLOADS"

    # Telegram maximum file upload size
    TG_MAX_FILE_SIZE = 4194304000

    # Chunk size that should be used with requests : default is 128KB
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))

    # Proxy for accessing youtube-dl in GeoRestricted Areas
    # Get your own proxy from https://github.com/rg3/youtube-dl/issues/1091#issuecomment-230163061
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    
    # Set timeout for subprocess
    PROCESS_MAX_TIMEOUT = 7200  # Increased timeout to 2 hours (7200 seconds)
    
    OWNER_ID = os.environ.get("OWNER_ID")
    ADL_BOT_RQ = {}
    AUTH_USERS = list({int(x) for x in os.environ.get("AUTH_USERS", "0").split()})
    AUTH_USERS.append(OWNER_ID)

# Function to make requests with a timeout
def make_request(url, retries=3):
    try:
        response = requests.get(url, proxies={"http": Config.HTTP_PROXY, "https": Config.HTTP_PROXY}, timeout=30)  # 30 seconds timeout
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        logging.error(f"Request to {url} timed out.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
    return None

# Example usage for downloading a file
def download_file(url, destination_path):
    logging.info(f"Starting download from {url}...")
    
    try:
        with make_request(url) as response:
            if response:
                with open(destination_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=Config.CHUNK_SIZE):
                        f.write(chunk)
                logging.info(f"Download completed successfully: {destination_path}")
            else:
                logging.error(f"Download failed for {url}")
    except Exception as e:
        logging.error(f"An error occurred while downloading {url}: {e}")

# Example function to handle process timeout
def run_long_process():
    import time
    logging.info("Starting long process...")

    try:
        # Simulate long-running task
        time.sleep(Config.PROCESS_MAX_TIMEOUT)  # Simulate task running for the process max timeout duration
        logging.info("Long process completed successfully.")
    except TimeoutError:
        logging.error(f"Process exceeded maximum timeout of {Config.PROCESS_MAX_TIMEOUT} seconds.")
    except Exception as e:
        logging.error(f"An error occurred during the process: {e}")

# Sample function to demonstrate error handling and timeouts
def example_task():
    url = "https://example.com/largefile"
    destination = "largefile.mp4"
    
    # Download file with timeout handling
    download_file(url, destination)
    
    # Run a long process with timeout handling
    run_long_process()

# Execute the example task
if __name__ == "__main__":
    example_task()
    
