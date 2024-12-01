FROM python:3.12

RUN pip install confluent-kafka

COPY produce.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "produce.py"]
