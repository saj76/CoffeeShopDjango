from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=data['customer_email'])
        email.send()
