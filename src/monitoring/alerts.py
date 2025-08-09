import os
from dotenv import load_dotenv
import smtplib
import json
from email.mime.text import MIMEText
from google.cloud import pubsub_v1

load_dotenv()

class EmailNotifier:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('ALERT_SENDER_EMAIL')
        self.sender_password = os.getenv('ALERT_SENDER_PASSWORD')
        self.recipient_email = os.getenv('ALERT_RECIPIENT')
    
    def send(self, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)

def callback(message):
    notifier = EmailNotifier()
    data = json.loads(message.data.decode('utf-8'))
    
    if data['severity'] == 'ERROR':
        subject = f"Dataflow Job Failure: {data.get('job_id', 'unknown')}"
        body = f"Error occurred at {data['timestamp']}:\n{data.get('message', 'No details')}"
    elif 'estimated_time' in data:
        subject = f"Dataflow Job Started: {data['job_id']}"
        body = f"Job started at {data['timestamp']}\nEstimated duration: {data['estimated_time']} minutes"
    else:
        subject = f"Dataflow Job Completed: {data['job_id']}"
        body = f"Job completed at {data['timestamp']}\nProcessed records: {data.get('processed_records', 0)}"
    
    notifier.send("data-engineering-team@yourcompany.com", subject, body)
    message.ack()

def listen_for_alerts(project_id, subscription_id):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    
    future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()

if __name__ == "__main__":
    listen_for_alerts("your-project", "dataflow-alerts")
