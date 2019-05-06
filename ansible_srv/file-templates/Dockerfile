FROM ubuntu:16.04
RUN mkdir -p /app
WORKDIR /app
COPY . /app
RUN apt-get -y update
RUN apt-get -y install nodejs
RUN apt-get -y install npm
RUN apt-get -y install git
ENV APP_PORT=3002
RUN git clone https://github.com/ppvasude/checkbox-microservice.git
RUN cd /app/checkbox-microservice/server-side/site && npm install

CMD cd /app/checkbox-microservice/server-side/site && nodejs server.js
