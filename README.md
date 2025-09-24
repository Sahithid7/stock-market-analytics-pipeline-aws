# 📈 Stock Market Real-Time Data Analytics Pipeline on AWS

## 📌 Overview
This project demonstrates a **real-time data analytics pipeline** built with AWS services.  
It ingests stock market events, processes them with Lambda, stores data in S3, sends alerts via SNS,  
and allows historical queries with Athena.

---

## 🏗️ Architecture
**Flow:**  
Producer (Python) → Amazon SQS → AWS Lambda → Amazon S3 → Amazon Athena  
&nbsp;&nbsp;&nbsp;&nbsp; ↘ Amazon SNS (email alerts)

![Architecture Diagram](docs/Stock_Market_Analytics_Pipeline_AWS_Style.png)

---

## 🚀 AWS Services Used
- **Amazon SQS** – Reliable message queue for event ingestion  
- **AWS Lambda** – Serverless compute for data processing  
- **Amazon S3** – Durable storage for processed events  
- **Amazon SNS** – Real-time notifications for anomaly alerts  
- **Amazon Athena** – SQL-based analytics on S3 data  

---

## 📊 Features
- ✅ Python **Producer** simulates live stock ticks and publishes to SQS  
- ✅ **Lambda** consumes SQS messages, enriches data, and stores JSON into S3  
- ✅ **SNS Alerts** notify when stock price ≥ threshold (e.g., 1200)  
- ✅ **Athena Queries** enable SQL analysis on historical stock data  

---

## 📂 Documentation
📄 See full [Project Report](docs/Stock_Market_Analytics_Pipeline_With_Diagram.pdf)  
(includes architecture diagram, resume bullets, and interview Q&A)

---

👩‍💻 Built by **Sahithi Devineni**  
Master’s in Information Systems @ Saint Louis University
