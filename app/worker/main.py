import boto3
import json
import time
import openai
from datetime import datetime

AWS_REGION = "us-east-1"
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/your-queue"
BUCKET_NAME = "your-audio-bucket"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
s3 = boto3.client("s3")
sqs = boto3.client("sqs")
transcribe = boto3.client("transcribe", region_name=AWS_REGION)

def generate_diary(transcript: str):
    prompt = (
        "Convert the following transcription into a structured personal diary journaling note. "
        "Include clear sections such as Date, Mood, Key Events, and Reflections.\n\n"
        f"Transcription:\n{transcript}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that helps convert plain text into a structured personal diary entry."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500,
    )
    return response.choices[0].message["content"].strip()

def poll_sqs():
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        messages = response.get("Messages", [])
        for msg in messages:
            receipt = msg["ReceiptHandle"]
            body = eval(msg["Body"])  # Safe alternative: use JSON
            job_name = body["job_name"]

            # Wait until transcription is complete
            while True:
                job_status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
                status = job_status['TranscriptionJob']['TranscriptionJobStatus']
                if status == "COMPLETED":
                    uri = job_status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                    transcript_json = requests.get(uri).json()
                    transcript_text = transcript_json["results"]["transcripts"][0]["transcript"]
                    diary = generate_diary(transcript_text)
                    print(f"\nDiary Generated:\n{diary}\n")
                    break
                elif status == "FAILED":
                    print(f"Job {job_name} failed.")
                    break
                else:
                    time.sleep(5)

            sqs.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=receipt)

if __name__ == "__main__":
    poll_sqs()
