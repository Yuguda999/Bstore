import os
import smtplib

own_email = os.getenv('EMAIL_ADD')
own_password = os.getenv('EMAIL_PASS')


def send_email(name, email, phone, message):
    email_message = f"Subject:Bstor User!\n\nName: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:{message}"
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        # connection.starttls()
        connection.login(own_email, own_password)
        connection.sendmail(from_addr='Bstore', to_addrs=own_email, msg=email_message)


def email_new_user(username: str = 'user', email: str = own_email):
    with open("base/message_body.txt") as file:
        message = file.read()
        message = f"Subject:{message.replace('[User Name]', username)}"
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        # connection.starttls()
        connection.login(own_email, own_password)
        connection.sendmail(from_addr='Bstore', to_addrs=email, msg=message.encode('utf-8'))
