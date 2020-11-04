FROM python:3.8.5-slim-buster
WORKDIR /casper
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . /casper
CMD tail -f /var/null
#ENTRYPOINT [ "python3" ]
#CMD [ "main.py" ]
