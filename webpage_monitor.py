import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def scrape_webpage(url):
    print("Scraping webpage...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.get_text()
    print("Webpage scraped successfully!")
    return content

def send_email(sender_email, receiver_email, password, subject, message):
    print("Sending email notification...")
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email notification sent successfully!")
        server.quit()
    except Exception as e:
        print("Error occurred while sending email:", str(e))

def send_initial_notification(sender_email, receiver_email, password):
    subject = "Webpage Monitoring Started"
    message = "The webpage monitoring process has started. You will receive email notifications for any updates."
    send_email(sender_email, receiver_email, password, subject, message)

# Prompt the user for the necessary values
url = input("Enter the URL to monitor: ")
sender_email = input("Enter your email address: ")
receiver_email = input("Enter the receiver's email address: ")
password = input("Enter your email password: ")

send_initial_notification(sender_email, receiver_email, password)

content = scrape_webpage(url)
while True:
    time.sleep(600)
    print("Checking for updates...")
    new_content = scrape_webpage(url)
    if new_content != content:
        subject = "Webpage Update Notification"
        message = "The webpage content has been updated. Check it out."
        send_email(sender_email, receiver_email, password, subject, message)
        print("Email notification sent to", receiver_email)
        content = new_content
    else:
        print("No updates found.")
