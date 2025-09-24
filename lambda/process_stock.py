import os, json, time, boto3

s3 = boto3.client("s3")
sns = boto3.client("sns")

BUCKET = os.environ.get("BUCKET")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")
ALERT_THRESHOLD = float(os.environ.get("ALERT_THRESHOLD", "1200"))

def lambda_handler(event, context):
    for record in event["Records"]:
        # SQS body is JSON string
        payload = json.loads(record["body"])
        payload["processed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        # Save to S3
        key = f"processed/{payload['symbol']}/{int(time.time())}.json"
        s3.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=json.dumps(payload)
        )

        # Publish alert if price above threshold
        if float(payload["price"]) >= ALERT_THRESHOLD and SNS_TOPIC_ARN:
            msg = f"ALERT: {payload['symbol']} price ${payload['price']} at {payload['processed_at']}"
            sns.publish(TopicArn=SNS_TOPIC_ARN, Message=msg)

    return {"status": "ok"}