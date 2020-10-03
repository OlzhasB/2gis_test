FROM python:3.7
MAINTAINER olzhas
ENV PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY *.py *.txt xml_files ./