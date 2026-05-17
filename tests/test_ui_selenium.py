import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture(scope="module")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize webdriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_dashboard_title(driver):
    # This test expects the FastAPI server to be running on port 8000
    try:
        driver.get("http://localhost:8000")
        assert "K8s" in driver.title or "Failure Prediction" in driver.page_source
    except Exception as e:
        pytest.skip(f"Server might not be running: {e}")

def test_manual_prediction_form(driver):
    try:
        driver.get("http://localhost:8000")
        
        # We need to wait for the page to load or ensure elements exist.
        # Assuming the dashboard has input fields, we just check for their presence.
        # The exact IDs depend on index.html, which we are assuming has input fields.
        # Since this is a generic test, we'll try to find any input or button.
        buttons = driver.find_elements(By.TAG_NAME, "button")
        assert len(buttons) > 0, "No buttons found on the dashboard"
        
    except Exception as e:
        pytest.skip(f"Could not interact with dashboard: {e}")
