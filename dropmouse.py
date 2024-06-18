from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

app = Flask(_name_)

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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        url = request.form.get('url')
        sender_email = request.form.get('sender_email')
        receiver_email = request.form.get('receiver_email')
        password = request.form.get('password')

        content = scrape_webpage(url)

        def check_for_updates():
            nonlocal content
            while True:
                new_content = scrape_webpage(url)
                if new_content != content:
                    subject = "Webpage Update Notification"
                    message = "The webpage content has been updated. Check it out."
                    send_email(sender_email, receiver_email, password, subject, message)
                    print("Email notification sent to", receiver_email)
                    content = new_content
                time.sleep(600)

        thread = threading.Thread(target=check_for_updates)
        thread.start()

        return 'Monitoring started!'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
