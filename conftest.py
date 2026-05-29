import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from pathlib import Path


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)

@pytest.fixture()
def setup(request):
    browser = request.config.getoption("--browser").lower()

    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    elif browser == "edge":
        options = EdgeOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser}. Use --browser chrome, --browser firefox, or --browser edge")

    options.add_argument("--start-maximized")
    if request.config.getoption("--headless"):
        options.add_argument("--headless")

    if browser == "chrome":
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("setup")
        if driver:
            try:
                Path("screenshots").mkdir(exist_ok=True)
                driver.save_screenshot(f"screenshots/{item.name}.png")
            except Exception as e:
                print(f"Screenshot failed: {e}")
