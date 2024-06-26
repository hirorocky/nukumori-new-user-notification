# %%
from zoneinfo import ZoneInfo
import requests
import json
import os
import datetime
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import *
import pytz

load_dotenv()
misskey_key = os.getenv("MISSKEY_BOT_API_KEY")
sendgrid_key = os.getenv("SENDGRID_API_KEY")
# %%
data = {"i": misskey_key, "sort": "+createdAt"}
data_encode = json.dumps(data)
url = "https://mi.nukumori-gay.space/api/users"
headers = {"Content-Type": "application/json"}
response = requests.post(url, data=data_encode, headers=headers, timeout=20)
# %%
# today = datetime.date.today
today = datetime.date(2024, 3, 21)
users_created_at_today = [
    user for user in response.json() if user.get("createdAt").startswith(str(today))
]

# %%
if users_created_at_today:
    # Construct email body
    email_body = "\n".join(
        [
            f"User: {user['name']}, Created At: {user['createdAt']}"
            for user in users_created_at_today
        ]
    )
    sg = sendgrid.SendGridAPIClient(api_key=sendgrid_key)
    from_email = Email("support@sg.nukumori-gay.space")
    to_email = To("hirorocky@gmail.com")
    subject = "【ぬくもり】新規ユーザーが登録されました"
    content = Content("text/plain", email_body)
    mail = Mail(from_email, to_email, subject, content)
    sg.client.mail.send.post(request_body=mail.get())
else:
    print("No users created today.")

# %%
if []:
    print("true")
else:
    print("false")

# %%
yesterday = datetime.date.today() - datetime.timedelta(days=1)

# %%
dt_now = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
yesterday = dt_now.date() - datetime.timedelta(days=1)

created_at = "2024-03-23T08:24:48.742Z"
created_at_in_utc = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))

# UTCからJSTに変換
jst_timezone = pytz.timezone("Asia/Tokyo")
created_at_in_jst = created_at_in_utc.astimezone(jst_timezone)
# %%
