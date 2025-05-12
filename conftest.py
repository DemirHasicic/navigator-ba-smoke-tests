# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.navigator.ba/"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture(scope="function", autouse=True)
def open_home(driver):
    driver.get(BASE_URL)
    yield

@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, 10)

def pytest_runtest_logreport(report):
    if report.when == "call":
        if report.passed:
            status = "PASSED"
        elif report.skipped:
            status = "SKIPPED"
        else:
            status = "FAILED"
        name = report.nodeid.split("::")[-1]
        print(f"{name}: {status}")
