FROM python:3.12

RUN pip install confluent-kafka mysql-connector-python

COPY setup.py .

CMD ["python", "setup.py"]
