FROM ubuntu:20.04

RUN DEBIAN_FRONTEND="noninteractive"  apt-get update -y && apt-get -y install tzdata

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get -y install default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

RUN pip3 install Flask pypmml numpy

COPY . /app

EXPOSE 3001

WORKDIR /app/app

ENTRYPOINT [ "python3" ]
CMD ["run.py"]
