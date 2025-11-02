import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


#poetry run pytest -m smoke
@pytest.mark.smoke
def test_google_homepage():
    driver.get("https://www.google.com")
    print("opening google")
    assert "Google" in driver.title

    '''to generate report pytest --html=report.html --self-contained-html  
    pip install pytest-html or poetry add pytest-html'''
