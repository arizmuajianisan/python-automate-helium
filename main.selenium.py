from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
import time
import os
import sys

# Configurations
url = "http://192.168.147.74/ConMasManager/"
login_page = url + "Login"
data_output_page = url + "DataOutput"
username = "user30"
password = "user30"
project_dir = os.path.dirname(os.path.abspath(__file__))  # Root directory of the code
download_dir = project_dir  # Set download directory to the code directory
print(download_dir)


# Initialize browser
def initialize_browser():
    chrome_options = Options()
    chrome_options.add_argument(
        "--unsafely-treat-insecure-origin-as-secure=http://192.168.147.74/"
    )
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": download_dir,  # Set download directory to the code directory
            "download.prompt_for_download": False,  # Disable the prompt for download
            "safebrowsing.enabled": False,  # Allow potentially dangerous downloads
            "safebrowsing.disable_download_protection": True,  # Disable download protection
            "credentials_enable_service": False, # Disable credentials service
            "password_manager_enabled": False,  # Disable password manager
            "password_manager_leak_detection": False,  # Disable password
        },
    )

    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    return browser


# Login function
def login(browser):
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "UserName"))
    ).send_keys(username)
    browser.find_element(By.NAME, "Password").send_keys(password)
    browser.find_element(By.XPATH, "//input[@value='Log-in']").click()
    time.sleep(2)  # Wait for login to complete


# Navigate and perform tasks
def navigate_and_perform_tasks(browser):
    """
    Step 1: Navigate to the Data Output page and perform tasks.
    """
    try:
        browser.get(data_output_page)
        print("Step 1: Success to navigate to %s" % data_output_page)
        time.sleep(2)  # Wait for page to load
    except Exception as e:
        print(f"Step 1 An error occurred while navigating to the Data Output page: {e}")
        sys.exit()

    """
    Step 2: Search the element "img_search" and click the "Search" button
    """
    try:
        browser.find_element(By.CLASS_NAME, "img_search").click()
        print("Step 2: Success to click the search button")
    except Exception as e:
        print(f"Step 2 An error occurred while finding the search button: {e}")
        sys.exit()

    """
    Step 3: Search for the form "SearchInfo_ReportName" and input the keyword "pcb molding"
    """
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id='SearchInfo_ReportName']")
            )
        ).send_keys("pcb molding")
        print("Step 3: Success to search for the form")
        time.sleep(2)
    except Exception as e:
        print(f"Step 3 An error occurred while searching for the form: {e}")
        sys.exit()

    """
    Step 4. Click the "Search" button
    """
    try:
        browser.find_element(By.ID, "conmasSearchButton").click()
        print("Step 4: Success to click the search button")
        time.sleep(2)
    except Exception as e:
        print(f"Step 4 An error occurred while clicking the search button: {e}")
        sys.exit()

    """
    Step 5: Select the checkboxes that used

    The Molding Department use 5 first rows and use the ID as identifier
    """
    try:
        id_form_values = ["17872", "15850", "15851", "15852", "15853"]
        for value in id_form_values:
            browser.find_element(By.XPATH, f"//*[@id='Cbx'][@value={value}]").click()
        wait_until_page_loads(browser)
        time.sleep(5)
        print("Step 5: Success to select the checkboxes")
    except Exception as e:
        print(f"Step 5 An error occurred while selecting the checkboxes: {e}")
        sys.exit()

    """
    Step 6: Click the NEXT button to move to the Export page
    """
    try:
        # browser.find_element(
        #     By.XPATH, "//*[@id='FiltersTable']/tbody/tr[1]/td[2]/a[2]"
        # ).click()
        browser.find_element(By.CLASS_NAME, "img_next").click()
        wait_until_page_loads(browser)
        print("Step 6: Success to click the Export button")
    except Exception as e:
        print(f"Step 6 An error occurred while clicking the Next button: {e}")
        sys.exit()

    """
    Step 7: Select the only 'Completed' form then click NEXT button
    """
    try:
        select_element = browser.find_element(By.ID, "EditReferStatus")
        # print("Select option: %s\n", select_element.text) # Debug list optons
        select = Select(select_element)
        select.select_by_visible_text("Completed")
        print("Step 7: Success to select the status of form to 'Completed'")
    except Exception as e:
        print(
            f"Step 7 An error occurred while waiting for the status and checkbox: {e}"
        )
        sys.exit()

    """
    Step 8: Click the all checkbox
    """
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "HeadCbx"))
        ).click()
        print("Step 8 Success to select the checkbox 'ID'")
    except Exception as e:
        print(f"Step 8 An error occurred while selecting the checkbox: {e}")
        sys.exit()

    """
    Step 9: After select the form that want to exported
    Then click the Next button to proceed the request
    """
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "img_next"))
        ).click()
        print("Step 9 Success to select the form that want to")
    except Exception as e:
        print(f"Step 9 An error occurred while clicking the Next button: {e}")
        sys.exit()

    """
    Step 10: Click the Export button to download the report
    """
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "img_next"))
        ).click()
        print("Step 10: Success to click the Next button at the Details page")
    except Exception as e:
        print(
            f"Step 10 An error occurred while clicking the Next button at Details Page: {e}"
        )
        sys.exit()

    """
    Step 11: After download the report, check if the file exists
    """
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "img_output_csv"))
        ).click()
        print("Step 11: Success to find the OUTPUT button")
    except Exception as e:
        print(f"Step 11 An error occurred while finding the OUTPUT button: {e}")
        sys.exit()


# Wait until the page is fully loaded
def wait_until_page_loads(browser, timeout=15):
    WebDriverWait(browser, timeout).until(
        EC.invisibility_of_element((By.XPATH, "//*[text()='Loading...']"))
    )


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
        navigate_and_perform_tasks(browser)
        monitor_download()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        browser.quit()


if __name__ == "__main__":
    main()
