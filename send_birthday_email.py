import os
import smtplib
import ssl
import csv
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Read email credentials from environment variables
username = os.getenv('EMAIL_USERNAME')
password = os.getenv('EMAIL_PASSWORD')

# Email content
subject = "Happy Birthday!"
body_template = """
Hi {name},

Wishing you a very Happy Birthday! May your day be filled with lots of love, joy, and happiness.

Best regards,
EICE Infotech
"""

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg['From'] = username
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(username, password)
        server.sendmail(username, to_email, msg.as_string())

def check_and_send_birthday_emails():
    today = datetime.today().strftime('%m-%d')

    with open('Employee.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name']
            email = row['Email']
            birthday = datetime.strptime(row['DOB'], '%d-%m-%Y').strftime('%m-%d')

            if birthday == today:
                body = body_template.format(name=name)
                send_email(email, subject, body)
                print(f"Sent birthday email to {name} at {email}")

if __name__ == "__main__":
    check_and_send_birthday_emails()
