from flask import Flask, request, Response
from celery import Celery
from datetime import datetime
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve the value of MAIL environment variable
mail = os.getenv('MAIL_ADDRESS')

# Retrieve the value of APP_PASSWORD environment variable
app_password = os.getenv('APP_PASSWORD')

log_file_path = os.getenv('LOG_FILE_PATH')

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write('')

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')
    
    if sendmail:
        send_email_task.delay(sendmail)
        return 'Email task has been queued.'
    
    if talktome is not None:
        log_time()
        return 'Time has been logged.'
    
    return 'Welcome to the messaging system.'

@app.route('/logs')
def logs():
    try:
        with open(log_file_path, 'r') as log_file:
            logs = log_file.readlines()  # Read lines from the log file

        formatted_logs = ''.join(f'<div>{log.strip()}</div>' for log in logs)  # Wrap each log in a <div>
        return Response(f"<h2>Logs:</h2>{formatted_logs}", mimetype='text/html')  # Return as HTML
    except Exception as e:
        return f'Failed to read logs: {e}', 500

@celery.task
def send_email_task(email):
    try:
        msg = MIMEText('HNG Task 3\n I want my full marks 👁️👁️')
        msg['Subject'] = 'Sending email from Flask app'
        msg['From'] = mail
        msg['To'] = email

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_user = mail
        smtp_password = app_password

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        log_action(f'Sent email to: {email}')
    except Exception as e:
        log_action(f'Failed to send email to: {email} - Error: {e}')
        print(f'Failed to send email: {e}')

def log_action(action):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'{current_time} - {action}\n')

def log_time():
    log_action('Time has been logged')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)
