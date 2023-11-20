# import scrapy
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.options import Options
# from scrapy.selector import Selector
# from ..items import LinkedinCrawlItem
#
# class LinkedinSpider(scrapy.Spider):
#     name = "linkedin"
#
#     def start_requests(self):
#         linkedin_home = 'https://www.linkedin.com/'
#         options = Options()
#         options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
#         driver = webdriver.Firefox(options=options)
#
#         driver.get(linkedin_home)
#         driver.implicitly_wait(3)
#
#         # Auth data
#         username = ""
#         password = ""
#
#         driver.implicitly_wait(3)
#
#         # Connection Form
#         driver.find_element(By.ID, 'session_key').send_keys(username)
#         driver.find_element(By.ID, 'session_password').send_keys(password)
#         driver.find_element(By.XPATH, "//button[@type='submit']").click()
#
#         # Process after auth
#         search_url = 'https://www.linkedin.com/search/results/people/?keywords=miage%20nice&origin=SWITCH_SEARCH_VERTICAL&sid=Xhf'
#         driver.get(search_url)
#         driver.implicitly_wait(3)
#
#         # Laissez la page se charger complètement (ajustez le temps d'attente si nécessaire)
#         driver.implicitly_wait(10)
#
#         profile_urls = [a.get_attribute('href') for a in driver.find_elements(By.XPATH, "//a[@class='app-aware-link']")]
#
#         # Visitez chaque profil
#         for profile_url in profile_urls:
#             yield scrapy.Request(profile_url, callback=self.parse_profile, meta={'driver': driver})
#
#     def parse_profile(self, response):
#         driver = response.meta['driver']
#         sel = Selector(text=driver.page_source)
#
#         # Extrayez le nom et le prénom du profil
#         items = LinkedinCrawlItem()
#         full_name = sel.css('h1.text-heading-xlarge::text').extract_first().strip()
#         items['full_name'] = full_name
#
#         yield items
#
#     def closed(self, reason):
#         driver = self.meta['driver']
#         driver.close()
