FROM python:3.5-jessie
ENV TEAM_ID=CC_167_169_179

RUN apt-get update -y

WORKDIR /root
RUN mkdir flask-mongodb-example
COPY ./ ./flask-mongodb-example/
COPY ./python/* ./flask-mongodb-example/
RUN pip install -qr ./flask-mongodb-example/requirements.txt

ENTRYPOINT ["python", "./flask-mongodb-example/acts.py"]
EXPOSE 5000