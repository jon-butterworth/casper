FROM ubuntu:latest
MAINTAINER Jon Butterworth
CMD tail -f /dev/null
RUN apt-get update -y && apt-get install -y python3-pip python3-dev
EXPOSE 4040
EXPOSE 5000
COPY ./requirements.txt /casper/requirements.txt
WORKDIR /casper
RUN pip3 install -r requirements
COPY . /casper
ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]