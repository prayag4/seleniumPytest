# conftest.py
import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome or firefox")
    parser.addoption("--url", action="store", default="https://crud-mvp-frontend.onrender.com/", help="Base URL of the application")

@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("--browser").lower()
    
    if browser_name == "chrome":
        driver = webdriver.Chrome()
    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError(f"Browser '{browser_name}' is not supported")
    
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url")

def pytest_itemcollected(item):
    """Show test docstring as the test name in the HTML report."""
    if item.function.__doc__:
        item._nodeid = item.function.__doc__.strip()

def pytest_html_report_title(report):
    report.title = "CRUD Automation Test Report"
   