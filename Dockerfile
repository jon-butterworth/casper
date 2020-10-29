FROM python:3.8.0-buster
WORKDIR /casper
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /casper
CMD [ "python" "main.py" ]