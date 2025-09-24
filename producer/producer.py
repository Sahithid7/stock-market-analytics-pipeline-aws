import boto3, json, random, time

# AWS region and SQS queue URL
REGION = "us-east-2"
QUEUE_URL = "https://sqs.us-east-2.amazonaws.com/734228160071/StockQueue"

# Create SQS client
sqs = boto3.client("sqs", region_name=REGION)

# Stock symbols to simulate
stocks = ["AAPL", "TSLA", "AMZN", "GOOG", "MSFT"]

def generate_tick():
    """Generate a fake stock market tick"""
    sym = random.choice(stocks)
    price = round(random.uniform(100, 1500), 2)
    volume = random.randint(100, 20000)
    return {"symbol": sym, "price": price, "volume": volume}

if __name__ == "__main__":
    print(f"Sending to SQS queue: {QUEUE_URL}")
    while True:
        rec = generate_tick()
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(rec)
        )
        print("Sent:", rec)
        time.sleep(2)  # send every 2 seconds

