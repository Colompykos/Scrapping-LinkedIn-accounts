import scrapy
import re
import time
import json
import random
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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
        time.sleep(2)
        password = ""

        driver.find_element(By.ID, 'session_key').send_keys(username)
        time.sleep(random.uniform(4, 10))

        driver.find_element(By.ID, 'session_password').send_keys(password)
        time.sleep(random.uniform(4, 10))

        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(random.uniform(4, 10))

        time.sleep(random.uniform(4, 10))

        # search_url = ('https://www.linkedin.com/search/results/people/?keywords=miage%20nice&origin'
        #               '=SWITCH_SEARCH_VERTICAL&sid=Xhf')
        # driver.get(search_url)
        # driver.implicitly_wait(3)
        #
        # driver.implicitly_wait(10)
        #
        # all_profile_URL = []
        #
        # def get_url():
        #     sel = Selector(text=driver.page_source)
        #     profiles = sel.css('a.app-aware-link')
        #
        #     for profile in profiles:
        #         href = profile.attrib.get('href')
        #         if href:
        #             profile_URL = re.findall(r"https://www.linkedin.com/in/([^\'\" >?$]+)", href)
        #             if profile_URL:
        #                 user_profile_name = profile_URL[0]
        #                 if len(user_profile_name) > 0 and not user_profile_name.startswith("ACoAA"):
        #                     profile_link = f"https://www.linkedin.com/in/{user_profile_name}"
        #                     if profile_link not in all_profile_URL:
        #                         all_profile_URL.append(profile_link)
        #
        # input_page = 100
        # URLs_all_page = []
        #
        # for page in range(1, input_page + 1):
        #     get_url()
        #     time.sleep(3)
        #     scroll_pause_time = random.uniform(0.5, 1.5)
        #     driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #     time.sleep(scroll_pause_time)
        #     time.sleep(7)
        #
        #     try:
        #         next_button = WebDriverWait(driver, 20).until(
        #             EC.element_to_be_clickable((By.XPATH,
        #                                         "//button[@aria-label='Next' and contains(@class, "
        #                                         "'artdeco-pagination__button--next')]"))
        #         )
        #         print(next_button)
        #         next_button.click()
        #     except TimeoutException:
        #         print(
        #             "Le bouton 'Suivant' n'a pas été trouvé ou n'est pas cliquable après un délai d'attente prolongé.")
        #     except NoSuchElementException:
        #         print("L'élément 'Suivant' n'a pas été trouvé sur la page.")
        #         break
        #
        #     URLs_all_page = URLs_all_page + all_profile_URL
        #     time.sleep(3)
        #
        # # Remove duplicates from URLs_all_page
        # URLs_all_page = list(set(URLs_all_page))
        #
        # # Write to the JSON file only once, after all URLs have been collected
        # with open('links.json', 'w') as f:
        #     json.dump([{'url': url} for url in URLs_all_page], f)

        time.sleep(random.uniform(4, 12))

        driver.implicitly_wait(7)
        # Visit the collected URLs
        self.visit_links(driver)

        # Close the driver after finishing scraping
        # driver.quit()

    def visit_links(self, driver):
        # Load URLs from the JSON file
        with open('links.json', 'r') as f:
            urls = json.load(f)

        # Prepare a list to store the profiles
        profiles = []

        # Visit each URL
        for url in urls:
            time.sleep(random.uniform(4, 11))

            driver.get(url['url'])
            time.sleep(random.uniform(4, 10))

            # Wait for the name element to be present
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.text-heading-xlarge')))
            name_element = driver.find_element(By.CSS_SELECTOR, 'h1.text-heading-xlarge')
            name = name_element.text

            # Wait for the description element to be present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.text-body-medium.break-words')))
            description_element = driver.find_element(By.CSS_SELECTOR, 'div.text-body-medium.break-words')
            description = description_element.text

            time.sleep(random.uniform(4, 13))

            details_exp_url = url['url'] + '/details/experience/'
            driver.get(details_exp_url)

            time.sleep(random.uniform(4, 12))

            exp_list = []
            sel = Selector(text=driver.page_source)

            exps_section = sel.css('div.KSbylxhLdMCJJvdLQgdLPKsaCDCmuNqXsGs')

            for section in exps_section:
                if section.css('.scaffold-finite-scroll__content'):
                    company_name = section.css('div.display-flex div div div span::text').get().strip()
                    job_role_elements = section.css('.pvs-list__paged-list-item')

                    for job_role in job_role_elements:
                        role_element = job_role.css('.mr1.hoverable-link-text.t-bold')
                        if role_element:

                            role = role_element.css('span::text').get().strip()
                            date_element_list = job_role.css('.pvs-entity__caption-wrapper::text').getall()
                            date = date_element_list[0].strip() if date_element_list else None

                            if date and ' - ' in date:
                                date_components = date.split(' - ')
                                date_start = date_components[0]
                                end_and_duration = date_components[1].split(' · ')
                                date_end = end_and_duration[0]  # Second part before '·' is the end date
                                duration = end_and_duration[1]
                            elif date:
                                date_parts = date.split(' · ')
                                date_start = date_parts[0]
                                duration = date_parts[1]
                                date_end = None
                            else:
                                date_start = None
                                date_end = None
                                duration = None
                            # contract_type = job_role.css('span.t-14.t-normal span::text')

                            # location = job_role.css('span.t-14.t-normal.t-black--light:nth-child(4) span::text')

                            exp_list.append({
                                'Company': company_name,
                                'Position': role,
                                'Date_début': date_start,
                                'Date_fin': date_end,
                                'Duration': duration,
                                # 'Contract Type': contract_type,
                                # 'Location': location,
                            })

                elif section.css('.pvs-entity--padded'):
                    name_company_element = section.css('span.t-14.t-normal span[aria-hidden="true"]::text').get()
                    if name_company_element:
                        name_company_parts = name_company_element.split(
                            '·')
                        company_name = name_company_parts[0].strip() if name_company_parts else None
                    else:
                        company_name = None

                    title_job_element = section.css('span.visually-hidden::text').get()
                    role = title_job_element.strip() if title_job_element else None

                    date_element_list = section.css('span.pvs-entity__caption-wrapper::text').getall()
                    date = date_element_list[0].strip() if date_element_list else None

                    if date and ' - ' in date:
                        date_components = date.split(' - ')
                        date_start = date_components[0]
                        end_and_duration = date_components[1].split(' · ')
                        date_end = end_and_duration[0]  # Second part before '·' is the end date
                        duration = end_and_duration[1]
                    elif date:
                        date_parts = date.split(' · ')
                        date_start = date_parts[0]
                        duration = date_parts[1]
                        date_end = None
                    else:
                        date_start = None
                        date_end = None
                        duration = None

                    # url_company_element = exps_section.css('a::attr(href)').get()
                    # url_company = url_company_element if url_company_element else None

                    exp_list.append({
                        'Company': company_name,
                        'Position': role,
                        'Date_début': date_start,
                        'Date_fin': date_end,
                        'Duration': duration,
                    })

            time.sleep(random.uniform(4, 13))

            details_edu_url = url['url'] + '/details/education/'
            driver.get(details_edu_url)

            time.sleep(random.uniform(4, 12))

            sel = Selector(text=driver.page_source)
            educations = sel.css('li.pvs-list__paged-list-item')

            education_list = []

            for education in educations:
                school_element = education.css(
                    'div.display-flex.align-items-center.mr1.hoverable-link-text.t-bold span[aria-hidden="true"]::text').get()
                school_name = school_element.strip() if school_element else None

                degree_field_element = education.css('span.t-14.t-normal span[aria-hidden="true"]::text').get()
                if degree_field_element:
                    degree_field_parts = degree_field_element.split(',')
                    degree = degree_field_parts[0].strip() if degree_field_parts else None
                    field = degree_field_parts[1].strip() if len(degree_field_parts) > 1 else None
                else:
                    degree = None
                    field = None

                date_element = education.css(
                    'span.t-14.t-normal.t-black--light span.pvs-entity__caption-wrapper[aria-hidden="true"]::text').get()
                date = date_element.strip() if date_element else None

                education_list.append({
                    'school_title': school_name,
                    'degree_school': degree,
                    'field': field,
                    'date': date
                })

            time.sleep(random.uniform(4, 15))

            details_skills_url = url['url'] + '/details/skills/'
            driver.get(details_skills_url)

            time.sleep(random.uniform(4, 13))

            sel = Selector(text=driver.page_source)
            skills = sel.css('li.pvs-list__paged-list-item')

            skills_list = []

            for skill in skills:
                skill_element = skill.css(
                    'div.display-flex.align-items-center.mr1.hoverable-link-text.t-bold span[aria-hidden="true"]::text').get()
                skill = skill_element.strip() if skill_element else None

                skills_list.append({
                    'skill_title': skill,
                })

            # Add the profile to the list
            profiles.append({
                'Name': name,
                'Description': description,
                'Experience': exp_list,
                'Education': education_list,
                'Skills': skills_list,
            })

            # Write the profiles list to the JSON file after scraping each profile
            with open('../../Profils.json', 'w') as f:
                json.dump(profiles, f)

        # Write all the profiles to the JSON file
        with open('../../Profils.json', 'w') as f:
            json.dump(profiles, f)