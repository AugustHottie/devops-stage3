# Messaging System with RabbitMQ, Celery, and Flask

## Overview

This project sets up a messaging system using Flask, RabbitMQ, and Celery to handle asynchronous tasks such as sending emails and logging timestamps. It includes a simple web application that can send emails and log time based on URL parameters, exposed through ngrok for external access.

### Tutorial Video

Check out the tutorial video to see the setup process in action:

[Watch the tutorial](https://youtu.be/TVK24gbf0q4)

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Endpoints](#endpoints)
- [Logging](#logging)
- [Using ngrok](#using-ngrok)

## Features

- Send emails using SMTP with the `?sendmail` parameter.
- Log the current time to a log file with the `?talktome` parameter.
- View application logs through the `/logs` endpoint.
- Asynchronous task handling with RabbitMQ and Celery.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework.
- **Celery**: An asynchronous task queue/job queue based on distributed message passing.
- **RabbitMQ**: A robust messaging broker that serves as the message queue.
- **SMTP**: For sending emails.
- **ngrok**: To expose the local server to the internet.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- RabbitMQ server installed and running

### Step 1: Clone the Repository

```bash
git clone https://github.com/AugustHottie/task3.git
cd task3
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

1. **Set up your environment variables** in a `.env` file or directly in your shell:

   ```plaintext
      MAIL_ADDRESS=your-email@gmail.com
      APP_PASSWORD=your-google-app-password
      LOG_FILE_PATH=/var/log/messaging_system.log
   ```

2. **Ensure RabbitMQ is running**:
   ```bash
   sudo systemctl start rabbitmq-server
   ```

## Running the Application

### Step 1: Start the Celery Worker

Open a new terminal and activate your virtual environment, then run:

```bash
celery -A app.celery worker --loglevel=info
```

### Step 2: Start the Flask Application

In another terminal window, run:

```bash
python app.py
```

## Endpoints

| Endpoint            | Description                                 | Example Usage                     |
|---------------------|---------------------------------------------|------------------------------------|
| `/`                 | Main route to send emails or log time       | `http://localhost:8000/?sendmail=your_email@example.com` |
| `/logs`             | View the application logs                    | `http://localhost:8000/logs`     |

## Logging

All logs will be written to `/var/log/messaging_system.log`. Ensure your application has permission to write to this path.

## Using ngrok

To expose your application to the internet, follow these steps:

1. **Start ngrok**:
   ```bash
   ngrok http 8000
   ```

2. **Use the provided ngrok URL** to access your application externally.
