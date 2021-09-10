# krypto-price-tracker


## Running Servers
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
### Install celery
pip install celery
### Install RabbitMQ (Ubuntu Linux 20.04LTS)
sudo apt-get install rabbitmq-server


### Start Celery
```
    celery -A KryptoAPI worker --loglevel=info
```

### Start Schdeuler
```
celery -A KryptoAPI beat --loglevel=info
```

## Tasks

* CRUD of Alerts
    - ~~POSTGRE~~
    - DB Design
    - ~~Django Rest Frame Work~~
* User Auth JWT
    - MiddleWare
    - ~~Setup Login~~
* PriceMoinitor 
    - Notifiaction System
    - BackGround Tasks (Celery)
* EMail System
    - Redis

## Rountes
    - Create
    - List 
        - Paginate ()
        - Filter
            - Triggered
            - Sleep
            - Active (Listen)
    - Delete
    - Listen/Sleep



Things to do for the assignment
* Create a rest API endpoint for the user’s to create an alert `alerts/create/`
* Create a rest API endpoint for the user’s to delete an alert `alerts/delete/`
* Create a rest API endpoint to fetch all the alerts that the user has created.
* The response should also include the status of the alerts
(created/deleted/triggered/.. or any other status you feel needs to be included)
* Paginate the response.
* Include filter options based on the status of the alerts. Eg: if the user wanted only
the alerts that were triggered, then the endpoint should provide just that)

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
