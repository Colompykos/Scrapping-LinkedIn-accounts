# import scrapy
# from scrapy.http import FormRequest
# from scrapy.utils.response import open_in_browser
#
# from ..items import LinkedinCrawlItem
#
#
# class LinkedinSpider(scrapy.Spider):
#     name = "linkedIn"
#
#     start_urls = ['https://www.linkedin.com/']
#
#     def parse(self, response):
#         open_in_browser(response)
#         token = response.css('form input[name="loginCsrfParam"]::attr(value)').extract_first()
#         print(token)
#
#         return FormRequest.from_response(response, formdata={
#             'loginCsrfParam': token,
#             'userName': '',
#             'password': ''
#
#         }, callback=self.start_scraping)
#
#     def start_scraping(self, response):
#         items = LinkedinCrawlItem()
#
# #        name = response.css('.entity-result__title-text .app-aware-link::text').extract()
# #        title = response.css('div.entity-result__primary-subtitle::text').extract()
#         test = response.css('title::text').extract()
#
#         #        items['name']=name
#         #       items['title']=title
#         items['gettest'] = test
#
#         yield items
