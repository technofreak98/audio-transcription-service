from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import boto3
import uuid
import os
from datetime import datetime

app = FastAPI()
security = HTTPBearer()

AWS_REGION = "us-east-1"
SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/your-queue"

# Simple token-based auth
API_KEY = "supersecretkey"

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

s3 = boto3.client("s3")
sqs = boto3.client("sqs")
transcribe = boto3.client("transcribe", region_name=AWS_REGION)

BUCKET_NAME = "your-audio-bucket"

@app.post("/upload")
async def upload_audio(file: UploadFile = File(...), token: str = Depends(validate_token)):
    extension = file.filename.split(".")[-1]
    temp_filename = f"/tmp/{uuid.uuid4()}.{extension}"

    with open(temp_filename, "wb") as f:
        f.write(await file.read())

    s3_key = f"uploads/{uuid.uuid4()}.{extension}"
    s3.upload_file(temp_filename, BUCKET_NAME, s3_key)
    os.remove(temp_filename)

    job_name = f"transcription_{uuid.uuid4()}"
    media_uri = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
    
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': media_uri},
        MediaFormat=extension,
        LanguageCode='en-US',
        OutputBucketName=BUCKET_NAME
    )

    message = {
        "job_name": job_name,
        "s3_key": s3_key,
        "uploaded_at": str(datetime.utcnow())
    }

    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=str(message)
    )

    return {"message": "File uploaded and transcription started", "job_name": job_name}
