import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def test_crud(base_url):
    wait = WebDriverWait(driver, 10)
    driver.get(f"{base_url}/records")

    driver.find_element(By.id,"Add")
    # wait.until(EC.element_to_be_clickable)

