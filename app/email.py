from flask_mail import Message
from app import mail

def send_email(subject, sender, recipients, test_body, html_body):
    """Send email with named properties."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = test_body
    msg.html = html_body
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
            '[Microblog] Reset Your Password',
            sender=app.config['ADMINS'][0],
            recipients=[user.email],
            test_body=render_template('email/reset_password.txt', 
                user=user, token=token),
            html_body=render_template('email/reset_password.html',
                user=user, token=token))

