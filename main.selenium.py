from helium import *
import os
import time
import shutil

# Configurations
url = "http://192.168.147.74/ConMasManager/"
login_page = url + "Login"
data_output_page = url + "DataOutput"
username = "user30"
password = "user30"
project_dir = os.path.dirname(os.path.abspath(__file__))  # Root directory of the code
download_dir = os.path.join(
    project_dir, "downloads"
)  # Set download directory to the code directory


# Initialize browser with download preferences
def initialize_browser():
    chrome_options = Options()
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    start_chrome(login_page, options=chrome_options)


# Login function
def login():
    write(username, into="User name")
    write(password, into="Password")
    click("Log-in")
    wait_until(
        Text("Dashboard").exists, timeout_secs=10
    )  # Wait until login is successful


# Navigate and perform tasks
def navigate_and_perform_tasks():
    go_to(data_output_page)
    wait_until(Text("Search").exists, timeout_secs=10)  # Wait for the page to load

    # Search for the form and select checkboxes
    click("Search")
    write("pcb molding", into="Form name")
    click("Search")

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

    # Additional tasks after checkbox selection
    click("Next")
    select("- Status -", "Completed")
    wait_until(
        lambda: not Text("Loading...").exists(), timeout_secs=15
    )  # Wait until page is fully loaded

    click(CheckBox("ID"))
    click("Next")
    click("Next")
    click("OUTPUT")

    # Wait for the download to complete
    handle_download()


# Function to monitor the download directory
def handle_download():
    print("Waiting for the download to complete...")

    # Ensure download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Track existing files in the directory
    existing_files = set(os.listdir(download_dir))

    # Monitor the directory for new files
    while True:
        current_files = set(os.listdir(download_dir))
        new_files = current_files - existing_files

        if new_files:
            for file in new_files:
                if file.endswith(".zip"):
                    print(f"Download complete: {file}")
                    return
        time.sleep(1)  # Check every second


def main():
    initialize_browser()

    try:
        login()
        navigate_and_perform_tasks()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        kill_browser()  # Properly close the browser


if __name__ == "__main__":
    main()
