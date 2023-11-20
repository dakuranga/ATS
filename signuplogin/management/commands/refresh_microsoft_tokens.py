import time
from django.core.management.base import BaseCommand
import schedule

from settingsapp.models import UserEmail  # Replace with your actual model import
from AA.settings import MS_CLIENT_ID, MS_CLIENT_SECRET, MS_REDIRECT_URI  # Replace with your actual settings import
from datetime import datetime, timedelta
import requests

def refresh_microsoft_token(user_email):
    token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
    data = {
        'client_id': MS_CLIENT_ID,
        'client_secret': MS_CLIENT_SECRET,
        'redirect_uri': MS_REDIRECT_URI,
        'refresh_token': user_email.refresh_token,
        'grant_type': 'refresh_token'
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    user_email.access_token = token_data['access_token']
    user_email.refresh_token = token_data['refresh_token']
    user_email.token_expiration = datetime.now() + timedelta(seconds=token_data['expires_in'])
    user_email.save()

class Command(BaseCommand):
    help = 'Refresh Microsoft tokens every 50 minutes'

    def handle(self, *args, **options):
        def job():
            # Fetch and refresh tokens for all user emails
            user_emails = UserEmail.objects.all()  # Replace with your actual model
            for user_email in user_emails:
                refresh_microsoft_token(user_email)

        # Schedule the job to run every 50 minutes
        schedule.every(1).minutes.do(job)

        while True:
            schedule.run_pending()
            time.sleep(1)
