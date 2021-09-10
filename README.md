# Krypto Price Tracker

Price alert application that triggers an email when the user’s target price is achieved.

## Features
- CRUD Alerts
- JWT Auth
- EMail Notifications
- Celery Scheduler

## Get Started
1. Clone the repo 
2. Create a virtual env
4. Update the `.env` file. 
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
    - Djnago Server
    ```
    python manage.py runserver
    ```
    - start Celery
    ```
    celery -A KryptoAPI worker --loglevel=info
    ```
    - start Schdeuler
    ```
    celery -A KryptoAPI beat --loglevel=info
    ```

### Install celery

pip install celery

### Install RabbitMQ (Ubuntu Linux 20.04LTS)

sudo apt-get install rabbitmq-server

## If I had more time, I would have
- Included more coins to set alerts, with other table, (one to many)
- Formated Routes to use Django Rest FramwWork ViewSets
- Set the Alerts to read state once the alert is called, if the user persists to have the alert continue, he would reactivate the alert.
- formated and add more comments

## Routes
    - Create
    - List 
        - Paginate ()
        - Filter
            - Triggered
            - Sleep
            - Active (Listen)
    - Delete
    - Activate/Deactivate

## PostMan 
Alerts: https://www.getpostman.com/collections/46a548c84c21fc0c2f78

### Tasks Done
* Create a rest API endpoint for the user’s to create an alert `alerts/create/`
* Create a rest API endpoint for the user’s to delete an alert `alerts/delete/`
* Create a rest API endpoint to fetch all the alerts that the user has created.
* The response should also include the status of the alerts
(created/deleted/triggered/.. or any other status you feel needs to be included)
* Add user authentication to the endpoints. Use JWT tokens.
* There is no need to add tests.
* Write a script that monitors the price of the cryptocurrency
* You can use this endpoint to fetch the latest price of the cryptocurrency:
https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_d
esc&per_page=100&page=1&sparkline=false
* When the price of the coin reaches the price specified by the users, send an email to all
the users that set the alert at that price. (send mail using Gmail SMTP, SendGrid, etc)
* You should set up a background worker(eg: celery/python-script/go-script) to send the
email. Use Rabbit MQ/Redis as a message broker.)

### TODO
* Paginate the response.
* Include filter options based on the status of the alerts. Eg: if the user wanted only
the alerts that were triggered, then the endpoint should provide just that)

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
