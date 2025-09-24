# 📈 Stock Market Real-Time Data Analytics Pipeline on AWS

A production-style, serverless data pipeline that ingests simulated stock ticks in real time, processes them, stores historics for analytics, and sends anomaly alerts — all on AWS.

> **Tech**: Amazon SQS · AWS Lambda · Amazon S3 · Amazon SNS · Amazon Athena · IAM · CloudWatch  
> **Language**: Python 3

---

## 🏗️ Architecture

![AWS Architecture](docs/aws-architecture.png)
> Tip: Use an architecture image with **official AWS icons** (SQS, Lambda, S3, SNS, Athena). Save it as `docs/aws-architecture.png`.

**Flow**

1) **Producer (Python)** → publishes stock ticks to **Amazon SQS**  
2) **AWS Lambda** (SQS trigger) → enriches each message, writes JSON to **Amazon S3**  
3) **Amazon SNS** → alert email when price ≥ threshold  
4) **Amazon Athena** → SQL over S3 (historical analytics)

---

## 📂 Repository Structure

.
├─ producer/
│ └─ producer.py # Sends simulated ticks to SQS
├─ lambda/
│ └─ process_stock.py # Lambda handler (SQS -> S3 + SNS)
├─ docs/
│ └─ aws-architecture.png # Architecture diagram (real AWS icons)
└─ README.md

yaml
Copy code

---

## 🔧 Why These AWS Services?

| Service      | What it does                                                                 | Why we used it here                                                                                      |
|--------------|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------|
| **SQS**      | Fully-managed message queue                                                   | Simple, durable ingestion layer; decouples producer from processing; available in all account types       |
| **Lambda**   | Serverless compute triggered by events                                        | Event-driven processing with zero server management and near-instant scaling                               |
| **S3**       | Object storage for data lake / artifacts                                     | Cheap, durable storage for JSON records; perfect for analytics via Athena                                  |
| **SNS**      | Pub/Sub notifications (email, SMS, webhooks)                                 | Instant alerts when price spikes above configurable threshold                                              |
| **Athena**   | Serverless SQL queries over S3                                               | No ETL/infra to manage; run SQL directly on JSON data                                                     |
| **IAM**      | Access control for AWS                                                        | Least-privilege roles/policies for Lambda (logs, SQS read, S3 write, SNS publish)                         |
| **CloudWatch** | Logs + metrics                                                              | Debugging, observability, and operational insight                                                          |

---

## ✅ Prerequisites

- AWS CLI configured (`aws configure`)  
- Python 3.x and `boto3` (`pip install boto3`)  
- Region: **us-east-2** (Ohio) — we aligned all resources here

---

## 🚀 Quick Start (TL;DR)

```powershell
# 0) Create S3 bucket (for processed data)
aws s3 mb s3://<YOUR_BUCKET_NAME> --region us-east-2

# 1) Create SQS queue
aws sqs create-queue --queue-name StockQueue --region us-east-2

# 2) Create SNS topic & email subscription (confirm email!)
aws sns create-topic --name StockAlerts --region us-east-2
# copy TopicArn into SNS_TOPIC_ARN
aws sns subscribe --topic-arn <SNS_TOPIC_ARN> --protocol email --notification-endpoint you@example.com --region us-east-2

# 3) Create IAM role for Lambda (or via console)
# - Trust: lambda.amazonaws.com
# - Policies:
#   * Logging: logs:CreateLogGroup/CreateLogStream/PutLogEvents
#   * S3 write: s3:PutObject on arn:aws:s3:::<YOUR_BUCKET_NAME>/processed/*
#   * SQS consumer: sqs:ReceiveMessage/DeleteMessage/GetQueueAttributes on arn:aws:sqs:us-east-2:<YOUR_ACCOUNT_ID>:StockQueue
#   * SNS publish: sns:Publish on <SNS_TOPIC_ARN>

# 4) Deploy Lambda
# zip lambda/process_stock.py -> lambda/function.zip
aws lambda create-function ^
  --function-name StockProcessor ^
  --runtime python3.11 ^
  --role arn:aws:iam::<YOUR_ACCOUNT_ID>:role/StockPipelineLambdaRole ^
  --handler process_stock.lambda_handler ^
  --zip-file fileb://lambda/function.zip ^
  --environment "Variables={BUCKET=<YOUR_BUCKET_NAME>,SNS_TOPIC_ARN=<SNS_TOPIC_ARN>,ALERT_THRESHOLD=1200}" ^
  --region us-east-2

# 5) Connect SQS -> Lambda
aws lambda create-event-source-mapping ^
  --function-name StockProcessor ^
  --batch-size 10 ^
  --event-source-arn arn:aws:sqs:us-east-2:<YOUR_ACCOUNT_ID>:StockQueue ^
  --region us-east-2

# 6) Run the producer (from ./producer)
python producer.py
🧪 Detailed Setup (Step-by-Step)
1) S3 bucket (processed data)
Create: aws s3 mb s3://<YOUR_BUCKET_NAME> --region us-east-2

Records will land under processed/<SYMBOL>/<EPOCH>.json

2) SQS queue
Create: aws sqs create-queue --queue-name StockQueue --region us-east-2

Note the QueueUrl and the ARN: arn:aws:sqs:us-east-2:<YOUR_ACCOUNT_ID>:StockQueue

3) SNS topic & subscription
Create topic (name: StockAlerts) and confirm your email subscription.

Save SNS_TOPIC_ARN for Lambda environment variables.

4) IAM role (Lambda execution role)
Trust policy: allow lambda.amazonaws.com to assume.

Policies (least privilege):

CloudWatch Logs: logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents on *

S3 write: s3:PutObject on arn:aws:s3:::<YOUR_BUCKET_NAME>/processed/*

SQS consume: sqs:ReceiveMessage, sqs:DeleteMessage, sqs:GetQueueAttributes on the StockQueue ARN

SNS publish: sns:Publish on <SNS_TOPIC_ARN>

5) Lambda (deployment)
Code: lambda/process_stock.py (Python 3.11)

Env vars:

BUCKET=<YOUR_BUCKET_NAME>

SNS_TOPIC_ARN=<SNS_TOPIC_ARN>

ALERT_THRESHOLD=1200 (change to test)

Deploy via CLI (see Quick Start) or console (Upload zip).

6) Event source mapping (SQS → Lambda)
aws lambda create-event-source-mapping ...

State becomes Enabled after creation.

7) Producer (run locally)
File: producer/producer.py

Set:

python
Copy code
REGION = "us-east-2"
QUEUE_URL = "https://sqs.us-east-2.<AWS>.com/<YOUR_ACCOUNT_ID>/StockQueue"
Run: python producer.py

8) Athena (historical queries over S3)
Set query results S3 location in Athena settings.

Create DB:

sql
Copy code
CREATE DATABASE stock_data;
Create table (replace bucket):

sql
Copy code
CREATE EXTERNAL TABLE stock_data.records (
  symbol string,
  price double,
  volume int,
  processed_at string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://<YOUR_BUCKET_NAME>/processed/';
Example queries:

sql
Copy code
SELECT symbol, AVG(price) AS avg_price
FROM stock_data.records
GROUP BY symbol;

SELECT symbol, MAX(price) AS max_price
FROM stock_data.records
GROUP BY symbol;

SELECT * FROM stock_data.records WHERE volume > 15000;
🔍 Observability & Troubleshooting
CloudWatch Logs → /aws/lambda/StockProcessor for handler logs

Common issues

Lambda not firing: Event source mapping not Enabled; region mismatch (keep everything in us-east-2).

No S3 files: IAM policy missing s3:PutObject, or wrong bucket/env var; check CloudWatch logs.

No email alerts: Confirmed the SNS email subscription? Lower ALERT_THRESHOLD to test.

Athena empty: Verify S3 LOCATION path (processed/), and that data has arrived.

💸 Cost Notes
SQS, Lambda, S3, SNS, and Athena are low-cost at small scale.

Delete resources when done (see Cleanup) to avoid ongoing charges.

🔐 Security
Least privilege IAM on the Lambda role

Private S3 bucket (no public access needed)

No secrets hardcoded in code; use environment variables and IAM roles

🧹 Cleanup
powershell
Copy code
# Disable and remove event source mapping
aws lambda list-event-source-mappings --function-name StockProcessor --region us-east-2
aws lambda delete-event-source-mapping --uuid <UUID> --region us-east-2

# Delete Lambda
aws lambda delete-function --function-name StockProcessor --region us-east-2

# Delete SQS
aws sqs delete-queue --queue-url https://sqs.us-east-2.amazonaws.com/<YOUR_ACCOUNT_ID>/StockQueue --region us-east-2

# Delete SNS topic (and any subscriptions)
aws sns delete-topic --topic-arn <SNS_TOPIC_ARN> --region us-east-2

# Empty & delete S3 bucket
aws s3 rm s3://<YOUR_BUCKET_NAME> --recursive --region us-east-2
aws s3 rb s3://<YOUR_BUCKET_NAME> --force --region us-east-2

---

👩‍💻 Built by **Sahithi Devineni**  
Master’s in Information Systems @ Saint Louis University
