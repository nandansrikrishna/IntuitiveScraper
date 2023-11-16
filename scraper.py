# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
from twilio.rest import Client
import os

# Twilio setup
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
twilio_number = os.environ.get('TWILIO_NUMBER')
your_phone_number = os.environ.get('YOUR_PHONE_NUMBER')

client = Client(account_sid, auth_token)

def load_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)

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

def send_sms(message):
    try:
        message = client.messages.create(
            to=your_phone_number,
            from_=twilio_number,
            body=message
        )
        print(f"Message sent: {message.sid}")
    except Exception as e:
        print(f"Error: {e}")

def save_listings(filename, listings):
    with open(filename, "w") as file:
        json.dump(listings, file, indent=4)

config = load_config('config.json')
URL = config['url']

previous_listings = load_previous_listings("listings.txt")

current_listings = get_job_listings(URL)

for job in current_listings:
    if job.text not in previous_listings:
        full_url = "https://careers.intuitive.com" + job['href']
        previous_listings[job.text] = full_url
        message = f"New Job Found: {job.text}, Link: {full_url}"
        print("New Job Found:", job.text)
        send_sms(message)

save_listings("listings.txt", previous_listings)