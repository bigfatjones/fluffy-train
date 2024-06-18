from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import time

app = Flask(__name__)

def scrape_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()

def send_email(sender_email, receiver_email, password, subject, message):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    # Ensure password is a string and encode it to UTF-8
    server.login(sender_email, password.encode('utf-8'))  
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        sender_email = request.form.get('sender_email')
        receiver_email = request.form.get('receiver_email')
        password = "hkaw cyeh vazh glul"  # Replace with your actual password

        content = scrape_webpage(url)

        # Send an email to notify that monitoring has started
        start_subject = "Webpage Monitoring Started"
        start_message = f"The monitoring of the webpage at {url} has started."
        send_email(sender_email, receiver_email, password, start_subject, start_message)

        def check_for_updates():
            nonlocal content
            while True:
                new_content = scrape_webpage(url)
                if new_content != content:
                    subject = "Webpage Update Notification"
                    message = "The webpage content has been updated. Check it out."
                    send_email(sender_email, receiver_email, password, subject, message)
                    content = new_content
                time.sleep(600)

        thread = threading.Thread(target=check_for_updates)
        thread.start()

        return 'Monitoring started!'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
