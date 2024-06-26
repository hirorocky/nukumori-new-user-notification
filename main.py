from zoneinfo import ZoneInfo
import requests
import json
import os
import datetime
import sendgrid
from sendgrid.helpers.mail import *
import pytz

if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

misskey_key = os.getenv("MISSKEY_BOT_API_KEY")
sendgrid_key = os.getenv("SENDGRID_API_KEY")


def send_mail_if_needed(_event, _context):
    new_users = fetch_new_users()
    if new_users:
        email_body = "\n".join(
            [
                f"User: {user['name']}, Created At: {user['createdAt']}"
                for user in new_users
            ]
        )
        send_mail_with_sendgrid(email_body)
        print("New users found and mail sent.")
    else:
        print("No users created today.")


def fetch_new_users():
    data = {"i": misskey_key, "sort": "+createdAt"}
    data_encode = json.dumps(data)
    url = "https://mi.nukumori-gay.space/api/users"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=data_encode, headers=headers, timeout=20)

    dt_now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    yesterday = dt_now.date() - datetime.timedelta(days=1)
    return [
        user
        for user in response.json()
        if is_in_yesterday(user.get("createdAt"), yesterday)
    ]


def is_in_yesterday(created_at, yesterday):
    created_at_in_utc = datetime.datetime.fromisoformat(
        created_at.replace("Z", "+00:00")
    )
    jst_timezone = pytz.timezone("Asia/Tokyo")
    created_at_in_jst = created_at_in_utc.astimezone(jst_timezone)
    return created_at_in_jst.date() == yesterday


def send_mail_with_sendgrid(body):
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_key)
    from_email = Email("support@sg.nukumori-gay.space")
    to_email = To("hirorocky@gmail.com")
    subject = "【ぬくもり】新規ユーザーが登録されました"
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    sg.client.mail.send.post(request_body=mail.get())


if __name__ == "__main__":
    send_mail_if_needed(None, None)
