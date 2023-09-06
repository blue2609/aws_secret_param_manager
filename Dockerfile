FROM python:3.11-alpine

WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN apk update
RUN apk upgrade

RUN apk add ncurses
RUN apk add aws-cli --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community/
RUN pip install awscliv2 --upgrade 
CMD ["ping", "www.google.com"]