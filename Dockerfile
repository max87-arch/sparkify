FROM ubuntu:20.04

RUN DEBIAN_FRONTEND="noninteractive"  apt-get update -y && apt-get -y install tzdata

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev default-jre

WORKDIR /app

RUN pip3 install Flask pypmml numpy

COPY . /app

EXPOSE 3001

WORKDIR /app/app

ENTRYPOINT [ "python3" ]
CMD ["run.py"]
