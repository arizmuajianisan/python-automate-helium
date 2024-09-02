from helium import *
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Configurations
url = "http://192.168.147.74/ConMasManager/"
login_page = url + "Login"
data_output_page = url + "DataOutput"
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
project_dir = os.path.dirname(os.path.abspath(__file__))  # Root directory of the code
download_dir = project_dir  # Set download directory to the code directory


# Initialize browser
def initialize_browser():
    browser = start_chrome(url)
    return browser


# Login function
def login(browser):
    write(username, into="User name")
    write(password, into="Password")
    click("Log-in")
    time.sleep(2)  # Wait for login to complete


# Navigate and perform tasks
def navigate_and_perform_tasks():
    go_to(data_output_page)
    time.sleep(2)  # Wait for page to load
    click("Search")
    write("pcb molding", into="Form name")
    click("Search")

    # Click the checkboxes
    checkboxes = [
        "PCB MOLDING SHIFT 1 Rev. 14",
        "PCB MOLDING SHIFT 2 Rev. 14",
        "PCB MOLDING SHIFT 1 Jumat Rev. 14",
        "PCB MOLDING LONG SHIFT 2 Rev. 14",
        "PCB MOLDING LONG SHIFT 1 Rev. 14",
    ]

    for checkbox in checkboxes:
        click(CheckBox(checkbox))
        time.sleep(1)  # Small delay to ensure the action is registered

    click("Next")
    wait_until(
        lambda: not Text("Loading...").exists(), timeout_secs=15
    )  # Wait until page is fully loaded
    select("- Status -", "Completed")
    click(CheckBox("ID"))
    wait_until(
        lambda: not Text("Loading...").exists(), timeout_secs=15
    )  # Wait until page is fully loaded
    click("Next")
    wait_until(
        lambda: not Text("Loading...").exists(), timeout_secs=15
    )  # Wait until page is fully loaded
    click("Next")
    wait_until(
        lambda: not Text("Loading...").exists(), timeout_secs=15
    )  # Wait until page is fully loaded
    click("OUTPUT")
    wait_until(
        lambda: not Text("Loading...").exists(), timeout_secs=15
    )  # Wait until page is fully loaded


def monitor_download():
    print("Waiting for the download to complete...")

    # Wait until the file appears in the download directory
    while True:
        for file in os.listdir(download_dir):
            if file.endswith(".zip"):
                print(f"Download complete: {file}")
                return
        time.sleep(1)  # Check every second


# Main function to run the automation
def main():
    browser = initialize_browser()

    try:
        login(browser)
        navigate_and_perform_tasks()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        kill_browser()


if __name__ == "__main__":
    main()
