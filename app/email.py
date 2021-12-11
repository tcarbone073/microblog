from flask_mail import Message
from app import mail

def send_mail(subject, sender, recipients, test_body, html_body):
    """Send email with named properties."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = test_body
    msg.html = html_body
    mail.send(msg)
