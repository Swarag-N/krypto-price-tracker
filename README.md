# Krypto Price Tracker

Price alert application that triggers an email when the user’s target price is achieved.

## Table of Contents
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Features](#features)
- [Get Started](#get-started)
  - [Docker Compose](#docker-compose)
  - [Local Development](#local-development)
  - [Install celery](#install-celery)
  - [Install RabbitMQ (Ubuntu Linux 20.04LTS)](#install-rabbitmq-ubuntu-linux-2004lts)
- [Life Cycle](#life-cycle)
- [Reproducibility Tips](#reproducibility-tips)
- [Folder Structure](#folder-structure)
- [Routes](#routes)
  - [Features](#features-1)
- [Setting Up Postgre DB](#setting-up-postgre-db)
- [Checking Routes](#checking-routes)
  - [Login](#login)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Features
- CRUD Alerts
- JWT Auth
- Email Notifications
- Celery Scheduler
- Multiple Coins

## Get Started
### Docker Compose
1. Clone the repo 
2. Update the `.docker.env` file.
    - Create a env using `.docker.env.example`
3. Start Server
    - Docker Compose
    ```shell
    docker-compose up
    ```

### Local Development
1. Clone the repo 
2. Create a virtual env
    ```
    python3 -m venv venv
    source ./venv/bin/activate 
    ```
4. Update the `.env` file.
    - Create a env using `env.example`
5. Have Postgre and RebitMQ running 
    - postgre
    ```
    pgrep -u postgres -fa -- -D
    ```
    - rabitmq
    ```
    sudo systemctl enable rabbitmq-server
    sudo systemctl status  rabbitmq-server
    sudo systemctl start rabbitmq-server
    ```
6. Install Dependeince
    - pip
    ```
    pip install -r requirements.txt
    ```
7. Make Migrations
    - shell
    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```
8. Start Server
    - Django Server
    ```
    python manage.py runserver
    ```
    - start Celery
    ```
    celery -A KryptoAPI worker --loglevel=info
    ```
    - start Scheduler
    ```
    celery -A KryptoAPI beat --loglevel=info
    ```

### Install celery

pip install celery

### Install RabbitMQ (Ubuntu Linux 20.04LTS)

sudo apt-get install rabbitmq-server

## Life Cycle
1. Admin Starts the server instance and add few coins to the database
2. User Creates an account and start creating alerts for registred coins
3. Service Actively fetches, the latest prices of Coins (30 Sec)(Can be modified)
4. Once the latest prices are fetched, start querying the alerts such that
    - alert is active
    - the alert target is crossed, both reaching an upper limit and lower limit
5. Found Alerts are turned to sleep, 
    - since once an email is sent, the notification is reached. Not to spam user
    - if the user, want to have the notification still running, he/she needs to activate the alert.

## Reproducibility Tips
1. Use Pro list view to add alerts for users, without much Hassel (added for testing) 
    - `http://localhost:8000/api/alert/pro-listview/`
2. Auth Header is set to JWT, not Bearer 
3. Once Scheduler  is called,  alerts are set to sleep, so activate the alert again in Django Admin Panel 
4. Access and Refresh Token 
    1. `http://localhost:8000/auth/jwt/create/`
    2. `http://localhost:8000/auth/jwt/refresh/`
5. End Points
    1. KryptoAPI.http
    2. POSTMAN collection `https://www.getpostman.com/collections/46a548c84c21fc0c2f78`
## Folder Structure
```
.dockerignore
.gitignore
|____launch.json
Dockerfile
KryptoAPI.http
|____.docker.env
|____.env
| |______init__.py
| |____admin.py
| |____apps.py
| | |______init__.py
| | |____requests_manager.py
| | |____routine_manager.py
| | |____task_manager.py
| |____mail.py
| | |______init__.py
| |____models.py
| |____serializers.py
| |____tasks.py
| |____tests.py
| |____urls.py
| |____views.py
| |______init__.py
| |____admin.py
| |____apps.py
| | |______init__.py
| |____models.py
| |____tests.py
| |____views.py
| |______init__.py
| |____asgi.py
| |____celery.py
| |____settings.py
| |____urls.py
| |____wsgi.py
|____manage.py
README.md
docker-compose.yml
requirements.txt
```
## Routes
    - Create
    - List  
        ```localhost:8000/api/alert/pro-listview/```
        - Paginate ()
        - Filter
            - Triggered
            - Sleep
            - Active (Listen)
    - Delete
    - Activate/Deactivate


### Features
* Create a rest API endpoint for the user’s to create an alert `alerts/create/`
* Create a rest API endpoint for the user’s to delete an alert `alerts/delete/`
* Create a rest API endpoint to fetch all the alerts that the user has created.
* The response should also include the status of the alerts
(created/deleted/triggered/.. or any other status you feel needs to be included)
- Paginate the response.
- Include filter options based on the status of the alerts. Eg: if the user wanted only
the alerts that were triggered, then the endpoint should provide just that)
* Add user authentication to the endpoints. Use JWT tokens.
* Write a script that monitors the price of the cryptocurrency
* You can use this endpoint to fetch the latest price of the cryptocurrency:
`'https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies={curr}'`
* When the price of the coin reaches the price specified by the users, send an email to all
the users that set the alert at that price. (send mail using Gmail SMTP, SendGrid, etc)
* You should set up a background worker(eg: celery/python-script/go-script) to send the
email. Use Rabbit MQ/Redis as a message broker.)

## Setting Up Postgre DB
```sql
CREATE DATABASE krypto2;
CREATE USER krypto2  WITH PASSWORD 'Swarag';
GRANT ALL PRIVILEGES ON DATABASE krypto TO krypto;
```

## Checking Routes
1. Headers are configured as
**Authorization: JWT <access_token> header:**



### Login
```shell
curl --location --request POST 'http://localhost:8000/auth/jwt/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "apple@a.cm",
    "password": "qwe"
}'
```

```
POST /auth/jwt/create

HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMTM3NTMwOCwianRpIjoiMmNmYzg5MjdiZWMxNDEyYWE2Y2Q5OTc4ZTg5N2ZkMzciLCJ1c2VyX2lkIjoyfQ.DK_sTu-Qd-ZI-utAysylokIV2H0HJ3abTlSW8I4ojNc",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMxMjg5MjA4LCJqdGkiOiI1NDA5OGI0ZTdkNmM0ODgyOTM2MDc1OGNjNDc5YmFiOSIsInVzZXJfaWQiOjJ9.FvBp001LT1ChJlZllZ6u4jkhcc3FXeicr03NmsCY_9E"
}

```
