FROM python:3.7-slim-stretch

COPY . /wv
WORKDIR /wv

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "wv.py"]
