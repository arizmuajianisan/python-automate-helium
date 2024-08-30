from helium import *
import time

# Configurations
url = "http://192.168.147.74/ConMasManager/"
login_page = url + "Login"
data_output_page = url + "DataOutput"
username = "user30"
password = "user30"


# Initialize browser
def initialize_browser():
    browser = start_chrome(login_page)
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
