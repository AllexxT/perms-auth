from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework.exceptions import ValidationError


class EmailService:
    @classmethod
    def send_email(cls, data):
        # is_debug = getattr(settings, "DEBUG", False)
        # if is_debug:
        #     print(
        #         "--- Email not sent because DEBUG is TRUE. Email data below. ---"  # noqa
        #     )
        #     print(data)
        #     return None

        to_email = data.get("to_email")
        subject = data.get("subject")
        template_data = data.get("meta") or {}
        template_data["subject"] = subject
        if not data.get("templates"):
            raise ValidationError("templates is required")
        html = render_to_string(data.get("templates"), template_data)

        message = EmailMultiAlternatives(
            subject,
            html,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
        )
        try:
            message.attach_alternative(html, "text/html")
            message.send()
        except Exception as e:
            print(f"Email exception: {e}")

        return None

    @classmethod
    def send_verification_email(cls, email, first_name, token):
        data = {
            "to_name": first_name,
            "to_email": email,
            "subject": "Test",
            "templates": "email/reset_password.html",
            "text": "Your code {}",
            "meta": {
                "first_name": first_name or "No First Name",
                "token": token.key,
            },
        }
        from pprint import pprint
        pprint(data)
        return cls.send_email(data)
