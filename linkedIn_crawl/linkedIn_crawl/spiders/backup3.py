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
#     page_number= 2
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
#         # Remplacez ces informations par vos identifiants LinkedIn
#         username = ""
#         password = ""
#
#         # Remplissez le formulaire de connexion
#         driver.find_element(By.ID, 'session_key').send_keys(username)
#         driver.find_element(By.ID, 'session_password').send_keys(password)
#         driver.find_element(By.XPATH, "//button[@type='submit']").click()
#
#         # Après la connexion, accédez à la page de recherche
#         search_url = 'https://www.linkedin.com/search/results/people/?keywords=miage%20nice&origin=SWITCH_SEARCH_VERTICAL&sid=Xhf'
#         driver.get(search_url)
#         driver.implicitly_wait(3)
#
#         # Laissez la page se charger complètement (ajustez le temps d'attente si nécessaire)
#         driver.implicitly_wait(10)
#
#         # Une fois la page chargée, passez le contenu à Scrapy
#         yield scrapy.Request(driver.current_url, callback=self.parse, meta={'driver': driver})
#
#     def parse(self, response):
#         driver = response.meta['driver']
#         sel = Selector(text=driver.page_source)
#
#         # Extrayez les données comme vous le faisiez précédemment
#         items = LinkedinCrawlItem()
#
#         # name = sel.css('.entity-result__title-text .app-aware-link::text').extract()
#         # title = sel.css('div.entity-result__primary-subtitle::text').extract()
#         # test = sel.css('title::text').extract()
#         links = sel.css(
#             'div.entity-result__item span.entity-result__title-text.t-16 a.app-aware-link::attr(href)').getall()
#
#         # items['name'] = name
#         # items['title'] = title
#         # items['gettest'] = test
#         items['links'] = links
#
#         yield items
#
#         next_page = "https://www.linkedin.com/search/results/people/?keywords=miage%20nice&origin=SWITCH_SEARCH_VERTICAL&page="+str(LinkedinSpider.page_number) +"&sid=k)e"
#         if LinkedinSpider.page_number <=3:
#             yield response.follow(next_page, callback=self.parse)
#
#
# def closed(self, reason):
#     driver = self.driver
#     driver.quit()
