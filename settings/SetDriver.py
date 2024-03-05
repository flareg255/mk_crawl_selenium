from selenium import webdriver


from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


class SetDriver:
    options = None
    driver = None

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=self.options)

    def getDriver(self):
        return self.driver