## Deploy
- sudo apt-get install docker
- sudo apt-get install docker-compose
- create .env file
- create crontab.txt
- create logs folder
- copy certificates
- copy docker-compose.yml
- run docker-compose up -d

## ENV

```env
QLIK_HOST=<ip>
QLIK_CERT_PATH=certificates
QLIK_USER_DIRECTORY=<ad>
QLIK_USER_ID=<usuer>
QLIK_DOC_ID_OUTBOUND=<app_id>
QLIK_DOC_OBJECT_OUTBOUND=<object_id>
```

## crontab.txt

```txt
* * * * * /usr/local/bin/python /opt/scripts/qlik_hypercube_outbound.py

```
