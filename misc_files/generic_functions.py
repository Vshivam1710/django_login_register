import smtplib, string, random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket


def generate_string(length=10):
    string_data = string.ascii_letters
    gen_string = "".join(random.choice(string_data) for _ in range(length))
    return gen_string


def verification_link(to_address, username, link):
    msg = MIMEMultipart()
    msg['From'] = 'Django Project'
    msg['To'] = to_address
    msg['Subject'] = 'Verification Link'

    body = f'Hey {username},\nyour verification link is {link}'
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
    except socket.gaierror as error:
        return error.strerror
    else:
        server.starttls()
        try:
            server.login('schoolmanagementdjp@gmail.com', '@&&schoolmanagement')
        except smtplib.SMTPAuthenticationError as error:
            return error.smtp_code
        else:
            server.sendmail('schoolmanagementdjp@gmail.com', to_address, text)
            return True
        finally:
            server.quit()
