# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json

URL = "https://careers.intuitive.com/en/jobs/?search=&type=Intern&pagesize=20#results"

def get_job_listings(url):
    driver = webdriver.Chrome()
    driver.get(URL)

    # Wait for JavaScript to load (adjust the selector as needed)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "stretched-link"))
    )

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    job_listings = soup.find_all("a", class_="stretched-link js-view-job")

    return job_listings

def load_previous_listings(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            # Return an empty dictionary if the file is empty
            return json.loads(data) if data else {}
    except FileNotFoundError:
        return {}

def save_listings(filename, listings):
    with open(filename, "w") as file:
        json.dump(listings, file)

previous_listings = load_previous_listings("listings.txt")

current_listings = get_job_listings(URL)

for job in current_listings:
    if job.text not in previous_listings:
        previous_listings[job.text] = "https://careers.intuitive.com" + job['href']
        print("New Job Found:", job.text)

save_listings("listings.txt", previous_listings)