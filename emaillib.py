import email
from smtplib import SMTP
# creates SMTP session
s = SMTP('smtp.gmail.com', 587)
# start TLS for security
# s.starttls()
# # Authentication
# s.login("kiddow12345@gmail.com", "lqeu eefi ytxt kkcg")
# # message to be sent
# message = "This is a test message"
# # sending the mail
# s.sendmail("kiddow12345@gmail.com", "pophuismeester100@gmail.com", message)
# # terminating the session
# s.quit()

EMAIL = "kiddow12345@gmail.com"
PASSWORD = "lqeu eefi ytxt kkcg"


def send_message(subject, message, recipients: list[str]):
    s.starttls()
    # Authentication
    s.login(EMAIL, PASSWORD)

    # sending the mail
    s.sendmail("kiddow12345@gmail.com", "pophuismeester100@gmail.com", message)

    s.quit()

