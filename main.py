import os
import sendgrid
from sendgrid.helpers.mail import *
import functions_framework

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

sendgrid_key = os.getenv("SENDGRID_API_KEY")


@functions_framework.http
def receive_request(request):
    request_json = request.get_json(silent=True)
    username = request_json["body"]["username"]
    email_body = f"New user: {username}"

    send_mail_with_sendgrid(email_body)
    print("New user found and mail sent.")


def send_mail_with_sendgrid(body):
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_key)
    from_email = Email("support@sg.nukumori-gay.space")
    to_email = To("hirorocky@gmail.com")
    subject = "【ぬくもり】新規ユーザーが登録されました"
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    sg.client.mail.send.post(request_body=mail.get())


if __name__ == "__main__":
    receive_request(None)
