import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def random_delay(min_delay=1, max_delay=3):
    """Generate a random delay between min_delay and max_delay."""
    time.sleep(random.uniform(min_delay, max_delay))

def test_click_buttons_and_submit_input(url: str):
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Custom User-Agent

    driver = webdriver.Chrome(options=options)
    action = ActionChains(driver)  # For simulating mouse movements
    try:
        driver.get(url)
        random_delay(2, 3)  # Random delay before starting

        # Click all buttons on the page
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            try:
                # Move to the button before clicking
                action.move_to_element(button).perform()
                button.click()
                random_delay(1, 2)  # Random delay between clicks
            except Exception as e:
                print(f"Could not click the button: {e}")

        # Look for an input field
        input_fields = driver.find_elements(By.TAG_NAME, 'input')
        for input_field in input_fields:
            if input_field.is_displayed() and input_field.is_enabled():
                action.move_to_element(input_field).perform()  # Move to the input field
                input_field.send_keys("data:text/html;base64,PHN2Zy9vbmxvYWQ9YWxlcnQoMik+<script src='data:;base64,YWxlcnQoZG9jdW1lbnQuZG9tYWluKQ=='></script>")  # Enter text
                input_field.submit()  # Submit the form
                break  # Exit if an input field is found and processed

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.close()
        driver.quit()

if __name__ == "__main__":
    test_click_buttons_and_submit_input("http://localhost:3000/")
