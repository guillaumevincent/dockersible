FROM python:3.5-alpine

RUN mkdir /backups
WORKDIR /dockersible
ADD requirements.txt /dockersible/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /dockersible/

COPY entrypoint.sh /
RUN chmod 755 /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

