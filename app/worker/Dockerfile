FROM python:3.10-slim

WORKDIR /worker

COPY worker.py .

RUN pip install boto3 openai requests

CMD ["python", "worker.py"]
