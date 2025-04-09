# audio-transcription-service

# 🧠 Audio Diary Transcription System

A scalable, cloud-native architecture that transcribes audio into structured personal diary entries using **AWS Transcribe**, **OpenAI GPT**, and **FastAPI**, deployed on **EKS with Karpenter + KEDA** and managed through **Terraform IaC + GitHub Actions CI/CD**.

---

## 🔧 Tech Stack

- **FastAPI** – REST API for audio upload/authentication
- **AWS Transcribe** – For audio-to-text transcription
- **OpenAI GPT-3.5** – Converts transcription into diary format
- **Amazon S3** – For storing audio files
- **Amazon SQS** – Event queue for async processing
- **Amazon RDS** – Optional storage for diary entries
- **KEDA** – Autoscale worker pods from SQS queue
- **Karpenter** – Autoscale EKS nodes
- **Terraform** – Infrastructure as Code
- **GitHub Actions** – CI/CD pipeline for deployment

---

## 📦 System Architecture

![Mentalyc Architecture](Mentalyc.drawio.png)

---

## 📁 Directory Structure

```bash
infra/
├── main.tf                  # Root Terraform entry point
├── eks/                     # EKS cluster, Karpenter, KEDA setup
├── network/                 # VPC & subnets
├── services/                # S3, SQS, RDS, Transcribe resources
└── apps/
    ├── fastapi-deployment.yaml
    ├── worker-deployment.yaml
    └── ingress.yaml
.github/
└── workflows/
    └── deploy.yml           # CI/CD GitHub Action
app/
├── api/                     # FastAPI upload endpoint
│   ├── main.py
│   └── Dockerfile
└── worker/                  # EKS Worker app
    ├── worker.py
    └── Dockerfile
```

Here's a **complete `README.md`** for your GitHub repo, integrating **AWS EKS architecture**, **FastAPI & Worker apps**, **Terraform infrastructure**, and **GitHub Actions CI/CD** setup.

---

```markdown
# 🧠 Mentalyc Audio Diary Transcription System

A scalable, cloud-native architecture that transcribes audio into structured personal diary entries using **AWS Transcribe**, **OpenAI GPT**, and **FastAPI**, deployed on **EKS with Karpenter + KEDA** and managed through **Terraform IaC + GitHub Actions CI/CD**.

---

## 🔧 Tech Stack

- **FastAPI** – REST API for audio upload/authentication
- **AWS Transcribe** – For audio-to-text transcription
- **OpenAI GPT-3.5** – Converts transcription into diary format
- **Amazon S3** – For storing audio files
- **Amazon SQS** – Event queue for async processing
- **Amazon RDS** – Optional storage for diary entries
- **KEDA** – Autoscale worker pods from SQS queue
- **Karpenter** – Autoscale EKS nodes
- **Terraform** – Infrastructure as Code
- **GitHub Actions** – CI/CD pipeline for deployment

---

## 📦 System Architecture

![Mentalyc Architecture](Mentalyc.drawio.png)

---

## 📁 Directory Structure

```bash
infra/
├── main.tf                  # Root Terraform entry point
├── eks/                     # EKS cluster, Karpenter, KEDA setup
├── network/                 # VPC & subnets
├── services/                # S3, SQS, RDS, Transcribe resources
└── apps/
    ├── fastapi-deployment.yaml
    ├── worker-deployment.yaml
    └── ingress.yaml
.github/
└── workflows/
    └── deploy.yml           # CI/CD GitHub Action
app/
├── api/                     # FastAPI upload endpoint
│   ├── main.py
│   └── Dockerfile
└── worker/                  # EKS Worker app
    ├── worker.py
    └── Dockerfile
```

---

## 🚀 Deploy Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/mentalyc-audio-transcriber.git
cd mentalyc-audio-transcriber
```

---

### 2. 🌍 Provision Infrastructure (Terraform)

> You must have AWS CLI and Terraform installed with credentials configured.

```bash
cd infra
terraform init
terraform apply -auto-approve
```

---

### 3. ☸️ Deploy Applications to EKS

```bash
# Update kubeconfig for your EKS cluster
aws eks update-kubeconfig --name mentalyc-cluster --region us-east-1

# Deploy Kubernetes manifests
kubectl apply -f apps/fastapi-deployment.yaml
kubectl apply -f apps/worker-deployment.yaml
kubectl apply -f apps/ingress.yaml
```

---

## 🤖 GitHub Actions CI/CD

### 🎯 Trigger: Push to `main` branch

Workflow File: `.github/workflows/deploy.yml`

### ✅ What It Does

1. Build Docker images for:
   - `fastapi-api`
   - `worker`
2. Push to Docker Hub
3. Update image in EKS deployments using `kubectl set image`

### 🔐 Required GitHub Secrets

| Secret Name              | Description                                 |
|--------------------------|---------------------------------------------|
| `AWS_ACCESS_KEY_ID`      | AWS IAM Access Key                          |
| `AWS_SECRET_ACCESS_KEY`  | AWS IAM Secret Key                          |
| `AWS_REGION`             | AWS region (e.g., `us-east-1`)              |
| `EKS_CLUSTER_NAME`       | Your EKS cluster name                       |
| `DOCKER_USERNAME`        | Docker Hub username                         |
| `DOCKER_PASSWORD`        | Docker Hub password                         |
| `DOCKER_REPO`            | Docker repo (e.g., `yourdocker/fastapi`)   |

---

## 📦 API Endpoint (FastAPI)

**POST** `/upload`

**Headers:**
- `Authorization: Bearer <API_KEY>`

**Body:**
- Multipart `audio_file`

**Response:**
```json
{
  "message": "File uploaded and transcription started",
  "job_name": "transcription_abc123"
}
```

---

## 🧠 Worker Function

The worker running in EKS:
- Polls SQS using long polling
- Waits for AWS Transcribe job to complete
- Downloads transcript
- Sends to OpenAI API for diary formatting
- (Optional) Saves result to RDS or S3

---

## 📌 Scaling & Observability

- **Karpenter** – Automatically provisions EC2 instances based on pod demand
- **KEDA** – Scales worker pods based on SQS message count
- **CloudWatch** – Logs and metrics integrated via EKS

---

## 📜 License

MIT © [Your Name]

---

## ❤️ Contributions

PRs welcome! For major changes, open an issue to discuss what you'd like to change.

---

## 📞 Support

Open an issue or ping [@yourhandle](https://github.com/yourhandle) on GitHub.
```

---

### Want Me to:

- Push this `README.md` to your repo?
- Add GitHub badges (build status, license, Docker pulls)?
- Auto-deploy docs to GitHub Pages?

Just say the word!
