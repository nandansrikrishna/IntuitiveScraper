# IntuitiveScraper

Simple scraping script to check for new intern listings on Intuitive Surgicals career website.

How to Use:

The script is designed to work with google's cloud services, specifically the gmail API, to notify the user of a new job listing. Thus a google cloud account is required to use the full features. Initilize a google cloud project, enable the Gmail API, and download the credentials for the credentials.json file. 

Remove the "send_email()" function to simply run localy. It can be scheduled using linux cron.

Additionally the script can be run in a cloud service's (like the google cloud project) compute instance to run at all times.

For local use, create a python virtual environment and pip install the requirements.txt file. In a compute instance, it can simply be installed to the VM.
