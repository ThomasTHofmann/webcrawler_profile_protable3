# https://selenium-python.readthedocs.io/getting-started.html
# https://beautiful-soup-4.readthedocs.io/en/latest/
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
import csv
from random import randint
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.common.by import By

import sys
import os
import warnings

error_count = 0

warnings.filterwarnings("ignore")
#disables warnings from selenium
LOGGER.setLevel("ERROR")

#path = '' so that the chrome driver is saved in the project folder and not locally in C:\Users\Admin\.wdm\drivers\chromedriver\win32\113.0.5672.63 for example
#driver = webdriver.Chrome(ChromeDriverManager(path = '').install())


service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
#maximize windowl, as there were some issues if the window was smaller.
driver.maximize_window()

with open("credentials.txt", "r") as file:
    credentials = file.read().strip().split(":")

linkedin_username = credentials[0]
linkedin_password = credentials[1]

#print(linkedin_password)
#print(linkedin_username)

#open linkedin login page
driver.get('https://www.linkedin.com/login')
time.sleep(randint(10,30))
#Enter login info:
username = driver.find_element(By.ID, 'username')
username.send_keys(linkedin_username)

password = driver.find_element(By.ID,'password')
password.send_keys(linkedin_password)

password.send_keys(Keys.RETURN)
time.sleep(randint(20,30))

names = []
company = None
profile_links = []
with open("data.txt", "r") as file:
    lines = file.readlines()
    line_index = 0
    while line_index < len(lines):
        line = lines[line_index].strip()
   
        if line.isdigit():
            company = line
            profile_links = []
            line_index += 1
            while line_index < len(lines) and not lines[line_index].strip().isdigit():
                profile_links.append(lines[line_index].strip())
                line_index += 1

            

            print(company)
            print(profile_links)
            #headings for the csv file:
            headings = ["Profile URL", "Name", "Company Index", "Title", "About", "Experience", "Education", "Skills"]
            #open csv file: this just writes the headings. New rows get edited further down
            with open("LinkedIn_Data/" + company + '.csv', 'w') as f:
                #create csv writer
                writer = csv.writer(f)
                writer.writerow(headings)
                f.close()

            for profile in profile_links:

                driver.get(profile)
                time.sleep(randint(25,45))

                #to move forward and backward use driver.forward() driver.back()

                #experience, education, skills
                experience_title = []
                #experience_company = []
                education_school = []
                #education_subject = []
                skills = []

                section_lists = driver.find_elements(By.CSS_SELECTOR,'.artdeco-card.pv-profile-card.break-words.mt2')
                #EXPERIENCE
                for section in section_lists:
                    #if this section contains the id 'experience' continue
                    if section.find_elements(By.ID,'experience'):
                        #if a show more button exists continue and click on the link, then scrape the new page that opened and then go back to the previous page.
                        #if section.find_elements_by_css_selector('.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid'):
                        if section.find_elements(By.CSS_SELECTOR,'.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--standard.artdeco-button--2.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid'):
                            #section.find_element_by_css_selector('.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid').click()
                            section.find_element(By.CSS_SELECTOR,'.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--standard.artdeco-button--2.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid').click()
                            time.sleep(randint(30,60))
                            #Scroll all the way down
                            last_height = driver.execute_script("return document.body.scrollHeight")
                            while True:
                                #Scroll to bottom
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                # Wait to load page
                                time.sleep(3)
                                # Calculate new scroll height and compare with last scroll height
                                new_height = driver.execute_script("return document.body.scrollHeight")
                                if new_height == last_height:
                                    break
                                last_height = new_height
                            #get new driver page for the new page that opened after the click
                            lists = driver.find_element(By.CSS_SELECTOR,'.pvs-list__container ')
                            #parts = lists.find_elements_by_tag_name('li')
                            #parts = lists.find_elements_by_css_selector('.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated ')
                            parts = lists.find_elements(By.CSS_SELECTOR,'.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column')
                            for part in parts:
                                #first part is the experience title
                                if part.find_elements(By.CSS_SELECTOR,'.visually-hidden'):
                                    p = part.find_elements(By.CSS_SELECTOR,'.visually-hidden')
                                    for part0 in p:
                                        experience_title.append(part0.get_attribute('innerText'))
                            
                                else:
                                    experience_title.append('NULL')

                            print("scrape experiences from site")
                            driver.execute_script("window.history.go(-1)")
                            time.sleep(randint(30,60))
                            #leave the loop early since the data is already scraped
                            break
                        else:
                            #no show more button so just scrape what is already there
                            print("scrape experiences from profile")
                            #check if there is a list is empty in this section
                            #if section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap'):
                                #section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap')
                            if section.find_elements(By.CSS_SELECTOR,'.display-flex.flex-column.align-self-center.flex-grow-1'):
                                section.find_elements(By.CSS_SELECTOR,'.display-flex.flex-column.align-self-center.flex-grow-1')
                                #items = section.find_elements_by_tag_name('li')
                                items = section.find_elements(By.CSS_SELECTOR,'.display-flex.flex-column.align-self-center.flex-grow-1')
                                for item in items:
                                    if item.find_elements(By.CSS_SELECTOR,'.visually-hidden'):
                                        i = item.find_elements(By.CSS_SELECTOR,'.visually-hidden')                            
                                        for item0 in i:
                                            experience_title.append(item0.get_attribute('innerText'))       
                                            #print("***************************************************")
                                            #print(item0.get_attribute('innerText'))
                                    else:
                                        experience_title.append('NULL')
                
                            break
                print(experience_title)
                #create a new section_lists since there is a possibility that the page was reloaded from the previous code
                section_lists = driver.find_elements(By.CSS_SELECTOR,'.artdeco-card.pv-profile-card.break-words.mt2')
                #EDUCATION
                for section in section_lists:
                    if section.find_elements(By.ID,'education'):
                        if section.find_elements(By.CSS_SELECTOR,'.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--standard.artdeco-button--2.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid'):
                            section.find_elements(By.CSS_SELECTOR,'.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--standard.artdeco-button--2.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid').click()
                            time.sleep(randint(30,60))
                            #Scroll all the way down
                            last_height = driver.execute_script("return document.body.scrollHeight")
                            while True:
                                #Scroll to bottom
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                # Wait to load page
                                time.sleep(3)
                                # Calculate new scroll height and compare with last scroll height
                                new_height = driver.execute_script("return document.body.scrollHeight")
                                if new_height == last_height:
                                    break
                                last_height = new_height
                            lists = driver.find_element(By.CSS_SELECTOR,'.pvs-list__container')
                            #parts = lists.find_elements_by_tag_name('li')
                            parts = lists.find_elements(By.CSS_SELECTOR,'.pvs-list__paged-list-item.artdeco-list__item.pvs-list__item--line-separated.pvs-list__item--one-column')
                            for part in parts:
                                if part.find_elements(By.CSS_SELECTOR,'.visually-hidden'):
                                    p = part.find_elements(By.CSS_SELECTOR,'.visually-hidden')
                                    for part0 in p:
                                        education_school.append(part0.get_attribute('innerText'))
                                else:
                                    education_school.append('NULL')

                            print("scrape educations from site")
                            driver.execute_script("window.history.go(-1)")
                            time.sleep(randint(30,60))
                            break
                        else:
                            #no show more button so just scrape what is already there
                            print("scrape educations from profile")
                            #check if there is a list is empty in this section
                            if section.find_elements(By.CSS_SELECTOR,'.display-flex.flex-column.align-self-center.flex-grow-1'):
                                section.find_elements(By.CSS_SELECTOR,'.display-flex.flex-column.align-self-center.flex-grow-1')
                                #items = section.find_elements_by_tag_name('li')
                                items = section.find_elements(By.CSS_SELECTOR,'.display-flex.flex-column.align-self-center.flex-grow-1')
                                for item in items:
                                    if item.find_elements(By.CSS_SELECTOR,'.visually-hidden'):
                                        i = item.find_elements(By.CSS_SELECTOR,'.visually-hidden')
                                        for item0 in i:
                                            education_school.append(item0.get_attribute('innerText'))
                                    else:
                                        education_school.append('NULL')

                            break
                print(education_school)
                section_lists = driver.find_elements(By.CSS_SELECTOR,'.artdeco-card.pv-profile-card.break-words.mt2')
                #SKILLS
                for section in section_lists:
                    if section.find_elements(By.ID,'skills'):
                        try:
                            if section.find_element(By.CSS_SELECTOR,'.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--standard.artdeco-button--2.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid'):
                                #Extremely rare case where it cant click on skills for profiles like "https://www.linkedin.com/in/fvdmaele/" temporary fix is use try and continue. this skips the skills section
                                try:
                                    section.find_element(By.CSS_SELECTOR,'.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--standard.artdeco-button--2.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid').click()
                                except:
                                    error_count += 1
                                    continue
                                time.sleep(randint(30,60))
                                #Scroll all the way down
                                last_height = driver.execute_script("return document.body.scrollHeight")
                                while True:
                                    #Scroll to bottom
                                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                    # Wait to load page
                                    time.sleep(3)
                                    # Calculate new scroll height and compare with last scroll height
                                    new_height = driver.execute_script("return document.body.scrollHeight")
                                    if new_height == last_height:
                                        break
                                    last_height = new_height
                                lists = driver.find_element(By.CSS_SELECTOR,'.pvs-list__container')
                                #this part is different than the previous code because the tag name 'li' is not only used for the name of the skill but also the endorsement. So used locate by css_selector instead.
                                parts = lists.find_elements(By.CSS_SELECTOR,'.display-flex.align-items-center.mr1.hoverable-link-text.t-bold')
                                for part in parts:
                                    if part.find_elements(By.CSS_SELECTOR,'.visually-hidden'):
                                        part0 = part.find_element(By.CSS_SELECTOR,'.visually-hidden')
                                        skills.append(part0.get_attribute('innerText'))
                                    else:
                                        skills.append('NULL')

                                print("scrape skills from site")
                                driver.execute_script("window.history.go(-1)")
                                time.sleep(randint(30,60))
                                break
                        except:
                        #else:
                            #no show more button so just scrape what is already there
                            print("scrape skills from profile")
                            #check if the list is empty in this section
                            #if section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap'):
                                #section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap')
                            if section.find_elements(By.CSS_SELECTOR,'.display-flex.flex-column.align-self-center.flex-grow-1'):
                                section.find_elements(By.CSS_SELECTOR,'.display-flex.flex-column.align-self-center.flex-grow-1')
                                items = section.find_elements(By.CSS_SELECTOR,'.display-flex.align-items-center.mr1.hoverable-link-text.t-bold')
                                for item in items:
                                    #check if the item exists
                                    if item.find_element(By.CSS_SELECTOR,'.visually-hidden'):
                                        #title of the experience
                                        item0 = item.find_element(By.CSS_SELECTOR,'.visually-hidden')
                                        skills.append(item0.get_attribute('innerText'))
                                        #print(item0)
                                    else:
                                        skills.append('NULL')
                            break
                print(skills)
                #BeautifulSoup part:
                src = driver.page_source
                soup = BeautifulSoup(src, 'lxml')

                #first profile part (the box with the name,title, location and number of connections)
                name_path = soup.find('div', {'class': 'mt2 relative'})

                #name
                try:
                    name = name_path.find('h1', {'class': 'XtnqdVTIVNWsbnBJDQhVakQTbSAaOKCkEMdbrk inline t-24 v-align-middle break-words'}).get_text().strip()
                except:
                    name = 'NULL'

                #title
                try:
                    title = name_path.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
                except:
                    title = 'NULL'

                #about
                about_path = soup.find('div', {'class': 'display-flex ph5 pv3'})
                try:
                    about = about_path.find('span', {'class': "visually-hidden"}).get_text().strip()
                except:
                    about = 'NULL'

                #join experience_title array into a single string
                a = ', '.join(str(x) for x in experience_title)
                #join education_school array into a single string
                b = ', '.join(str(x) for x in education_school)
                #join skills array into a single string
                c = ', '.join(str(x) for x in skills)
                save_csv_row = [profile, name, company, title, about, a, b, c]

                with open('LinkedIn_Data/' + company + '.csv', 'a', encoding='utf-8', newline='') as f:
                    #create csv writer
                    writer = csv.writer(f)
                    writer.writerow(save_csv_row)
                    f.close()
        else:
            line_index += 1
driver.close()
print(error_count)
print('Finished, console window can be closed')
