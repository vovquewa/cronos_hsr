#running from home: docker build -f infra/Dockerfile -t cronos .
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y cron && \
    apt-get install -y nano

WORKDIR /opt

COPY requirements.txt /opt

COPY .env /opt

RUN pip3 install -r requirements.txt --no-cache-dir

COPY /scripts /opt/scripts

# RUN chmod a+x /opt/scripts/qlik_hypercube_outbound.py

RUN mkdir /opt/logs
RUN mkdir /opt/certificates

COPY crontab.txt /opt

RUN crontab /opt/crontab.txt

CMD ["cron", "-f"]