from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle
import base64

# Load configuration from a JSON file
def load_config(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Scrape job listings from a given URL
def get_job_listings(url):
    driver = webdriver.Chrome()
    driver.get(url)

    # Wait for the page's JavaScript to load and for a specific element to appear
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "stretched-link"))
    )

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Find all job listings based on their HTML class
    job_listings = soup.find_all("a", class_="stretched-link js-view-job")

    return job_listings

# Load previously scraped listings from a file
def load_previous_listings(filename):
    try:
        with open(filename, "r") as file:
            data = file.read()
            return json.loads(data) if data else {}
    except FileNotFoundError:
        return {}

# Authenticate and create a service for Gmail API
def service_gmail():
    creds = None
    # Load or refresh existing tokens, or create new ones if necessary
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', ['https://www.googleapis.com/auth/gmail.send'])
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

# Send an email using the Gmail API
def send_email(subject, message, receiver_email):
    service = service_gmail()
    message = (service.users().messages().send(userId="me", body={
        'raw': base64.urlsafe_b64encode(
            f"To: {receiver_email}\r\nSubject: {subject}\r\n\r\n{message}".encode()
        ).decode()
    }).execute())
    print(f"Message Id: {message['id']}")

# Save the current listings to a file
def save_listings(filename, listings):
    with open(filename, "w") as file:
        json.dump(listings, file, indent=4)

# Main script execution
config = load_config('config.json')
URL = config['url']

previous_listings = load_previous_listings("listings.txt")

current_listings = get_job_listings(URL)

# Check each job listing and send an email if it's new
for job in current_listings:
    if job.text not in previous_listings:
        full_url = "https://careers.intuitive.com" + job['href']
        previous_listings[job.text] = full_url
        subject = "New Job Listing Found"
        message = f"New Job Found: {job.text}, Link: {full_url}"
        print("New Job Found:", job.text)
        send_email(subject, message, "nsrikrishna06@gmail.com") 

# Save the updated listings
save_listings("listings.txt", previous_listings)
