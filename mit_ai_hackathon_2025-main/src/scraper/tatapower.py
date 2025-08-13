"""
This script contains functions for the scraping of data from TATA-POWER:
    https://www.tatapower.com/renewables/solar-energy#tabs-9975c704ed-item-2a3f25ad7e-tab
"""




# #############################################################################
# IMPORTS
# #############################################################################

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




# #############################################################################
# CONSTANTS
# #############################################################################

START_PAGE = "https://www.tatapower.com/renewables/solar-energy#tabs-9975c704ed-item-2a3f25ad7e-tab"
TARGET_FILE = "../../data/raw_data/company_tata_projects.csv"

# #############################################################################
# MAIN CODE
# #############################################################################



# DOWNLOAD 

PAGE_SOLAR = ""

driver = webdriver.Chrome()
driver.get(START_PAGE)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
except Exception as e:
    print("Page did not load in time:", e)

PAGE = driver.page_source

driver.quit()



# ########## PARSE CONTENT

company_data = []
parts = PAGE.split("leadership-card")[2:14]
for part in parts:
    title = part.split("leadership-person-name\">")[1].split("</p>")[0]
    img = "https://www.tatapower.com/"+part.split("src=\"")[1].split("\"")[0]
    url = "https://www.tatapower.com/"+part.split("href=\"")[1].split("\"")[0]
    company_data.append([title, img, url])

company_data = pd.DataFrame(company_data, columns=["title", "img", "url"])
company_data.to_csv(TARGET_FILE, index=False)