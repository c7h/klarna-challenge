FROM alpine:latest

MAINTAINER Christoph Gerneth <christoph@gerneth.info>

WORKDIR /code/
ADD ./klarnachallenge /code/
ADD ./gunicorn_config.py /code/

RUN apk --no-cache add --virtual build-deps build-base python3-dev curl netcat-openbsd \
 && apk --no-cache add --virtual runtime-deps python3 libpq ca-certificates\
 && apk --no-cache upgrade \
 && curl -O https://bootstrap.pypa.io/get-pip.py \
 && python3 get-pip.py \
 && apk del --purge build-deps \
 && pip3 install gunicorn

ADD ./requirements.txt /code/
RUN pip install -r ./requirements.txt

RUN mkdir /tmp/prom_data
ENV prometheus_multiproc_dir /tmp/prom_data

# expose port(s)
EXPOSE 8000

CMD ["/usr/bin/gunicorn", "--config", "gunicorn_config.py", "server:app"]
