# 📈 Stock Market Real-Time Data Analytics Pipeline on AWS

A serverless data pipeline that ingests simulated stock ticks in real-time, processes and stores them for historical analytics, and sends automated alerts when anomalies occur — all built using **AWS cloud-native services**.

> **Tech Stack**: Amazon SQS · AWS Lambda · Amazon S3 · Amazon SNS · Amazon Athena · IAM · CloudWatch  
> **Language**: Python 3 with Boto3  

---

## 🏗️ Architecture

![AWS Architecture](docs/aws-architecture.png)

### Flow of Data
1. **Producer (Python Script)** generates stock tick data and publishes it to **Amazon SQS**.  
2. **Amazon SQS** acts as a reliable buffer, ensuring event-driven ingestion and decoupling producers from consumers.  
3. **AWS Lambda** is triggered by new messages in SQS:  
   - Stores processed JSON into **Amazon S3** for long-term durability.  
   - Publishes alerts to **Amazon SNS** when stock prices cross a defined threshold.  
4. **Amazon Athena** queries structured JSON data directly from S3 for historical analytics without the need for ETL pipelines.  

---

## 🔧 Why These AWS Services?

| Service        | Functionality                                                                 | Why We Used It                                                                 |
|----------------|-------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **Amazon SQS** | Fully managed message queue for decoupled, reliable ingestion                 | Ensures no stock tick events are lost, scales seamlessly for spikes             |
| **AWS Lambda** | Serverless compute triggered by events                                        | Auto-scales with incoming data, no servers to manage, cost-efficient            |
| **Amazon S3**  | Highly durable object storage                                                 | Stores JSON stock records for long-term analytics at minimal cost               |
| **Amazon SNS** | Pub/Sub messaging for notifications                                           | Sends real-time alerts to subscribers when price thresholds are breached        |
| **Amazon Athena** | Serverless SQL queries directly on S3 data                                | Allows analysts to run queries on raw JSON without complex ETL pipelines        |
| **IAM**        | Identity and access management                                                | Enforces least-privilege access for Lambda to interact with SQS, S3, and SNS    |
| **CloudWatch** | Logging and monitoring                                                        | Provides observability for Lambda execution, errors, and system health          |

---

## 🎯 Project Purpose

### ✅ Why This Project Is Needed
- Real-time analytics is critical for industries like **finance**, **retail**, and **IoT** where data arrives continuously.  
- Traditional batch ETL pipelines introduce delays — this project demonstrates **event-driven, serverless data processing**.  

### ✅ Business Purpose
- Monitor incoming stock prices **in real-time**.  
- Store all events in a **data lake (S3)** for historical trend analysis.  
- Trigger **alerts automatically** when abnormal spikes occur.  
- Enable stakeholders to run **SQL queries on demand** without infrastructure setup.  

---

## ⚙️ Functionality

1. **Real-Time Data Ingestion**  
   A Python producer simulates stock ticks and publishes them to Amazon SQS.  

2. **Event-Driven Processing**  
   AWS Lambda consumes messages from SQS, processes the payload, and branches logic:  
   - Store in Amazon S3 (`processed/` folder).  
   - Send alerts via Amazon SNS if threshold conditions are met.  

3. **Historical Querying**  
   Data in S3 can be queried via Amazon Athena using SQL statements, enabling analysis of stock patterns over time.  

4. **Notifications**  
   Amazon SNS delivers instant alerts (email/SMS) to subscribed users.  

---

## 📊 Example Use Case

- 📉 Detect unusual stock drops and send alerts to risk managers.  
- 📈 Identify when stock prices exceed a trading threshold and notify traders.  
- 📊 Store years of tick data in S3 for future analytics and machine learning workloads.  

---

## ✅ Resume-Ready Highlights

- Designed and implemented a **serverless real-time data pipeline** using AWS native services.  
- Demonstrated **event-driven architecture** (SQS → Lambda → S3 + SNS).  
- Built a **data lake solution** for stock analytics with **Athena SQL querying**.  
- Implemented **alerting mechanisms** via SNS to monitor anomalies.  
- Followed **best practices in IAM (least privilege)** and **CloudWatch logging** for observability.  

---

## 🧹 Cleanup (to avoid charges)

```bash
aws lambda delete-function --function-name StockProcessor --region us-east-2
aws sqs delete-queue --queue-url <QUEUE_URL> --region us-east-2
aws sns delete-topic --topic-arn <SNS_TOPIC_ARN> --region us-east-2
aws s3 rm s3://<BUCKET_NAME> --recursive --region us-east-2
aws s3 rb s3://<BUCKET_NAME> --force --region us-east-2


---

👩‍💻 Built by **Sahithi Devineni**  
Master’s in Information Systems @ Saint Louis University
