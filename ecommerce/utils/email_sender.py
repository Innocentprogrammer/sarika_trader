import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from django.conf import settings

def send_brevo_email(subject, html_content, recipient_list):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender = {"name": "Ecommerce Site", "email": settings.DEFAULT_FROM_EMAIL}

    to_list = [{"email": email} for email in recipient_list]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to_list,
        html_content=html_content,
        subject=subject,
        sender=sender
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email)
        print("Email sent:", response)
        return response
    except ApiException as e:
        print("Error sending email: %s\n" % e)
        return None
