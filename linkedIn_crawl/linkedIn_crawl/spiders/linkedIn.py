import scrapy
import re
import time
import json
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkedInSpider(scrapy.Spider):
    name = 'linkedin_spider'
    start_urls = ['https://www.linkedin.com/']

    def start_requests(self):
        linkedin_home = 'https://www.linkedin.com/'
        options = FirefoxOptions()
        options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
        driver = webdriver.Firefox(options=options)

        driver.get(linkedin_home)
        driver.implicitly_wait(3)

        yield scrapy.Request(driver.current_url, callback=self.parse, meta={'driver': driver})

    def parse(self, response):
        driver = response.meta.get('driver')

        # add credentials
        username = ""
        driver.implicitly_wait(5)
        password = ""

        driver.find_element(By.ID, 'session_key').send_keys(username)
        driver.find_element(By.ID, 'session_password').send_keys(password)
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        driver.implicitly_wait(3)

        search_url = 'https://www.linkedin.com/search/results/people/?keywords=miage%20nice&origin=SWITCH_SEARCH_VERTICAL&sid=Xhf'
        driver.get(search_url)
        driver.implicitly_wait(3)

        driver.implicitly_wait(10)

        all_profile_URL = []

        def get_url():
            sel = Selector(text=driver.page_source)
            profiles = sel.css('a.app-aware-link')

            for profile in profiles:
                href = profile.attrib.get('href')
                if href:
                    profile_URL = re.findall(r"https://www.linkedin.com/in/([^\'\" >?$]+)", href)
                    if profile_URL:
                        user_profile_name = profile_URL[0]
                        if len(user_profile_name) > 0 and not user_profile_name.startswith("ACoAA"):
                            profile_link = f"https://www.linkedin.com/in/{user_profile_name}"
                            if profile_link not in all_profile_URL:
                                all_profile_URL.append(profile_link)

        input_page = 5
        URLs_all_page = []

        for page in range(1, input_page + 1):
            get_url()
            time.sleep(2)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(5)

            try:
                next_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                "//button[@aria-label='Next' and contains(@class, 'artdeco-pagination__button--next')]"))
                )
                print(next_button)
                next_button.click()
            except TimeoutException:
                print("Le bouton 'Suivant' n'a pas été trouvé ou n'est pas cliquable après un délai d'attente prolongé.")
            except NoSuchElementException:
                print("L'élément 'Suivant' n'a pas été trouvé sur la page.")
                break

            URLs_all_page = URLs_all_page + all_profile_URL
            time.sleep(3)

        # Remove duplicates from URLs_all_page
        URLs_all_page = list(set(URLs_all_page))

        # Write to the JSON file only once, after all URLs have been collected
        with open('output.json', 'w') as f:
            for url in URLs_all_page:
                # Generate a Scrapy item containing the URL
                yield {'url': url}
                # Write to the JSON file
                f.write(f'"{url}"\n')

        # Close the driver after finishing scraping
        # driver.quit()