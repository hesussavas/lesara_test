FROM python:3.6

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python-pip


COPY . /opt/lesara_test
WORKDIR /opt/lesara_test

RUN pip install -r requirements.txt

RUN chmod +x run.sh

CMD bash