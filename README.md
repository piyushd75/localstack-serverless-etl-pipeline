![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LocalStack](https://img.shields.io/badge/LocalStack-Latest-green)
![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange)
![Amazon S3](https://img.shields.io/badge/AWS-S3-red)
![Amazon DynamoDB](https://img.shields.io/badge/AWS-DynamoDB-blue)
![Pytest](https://img.shields.io/badge/Tested_with-Pytest-success)

# 🚀 LocalStack Serverless ETL Pipeline

An event-driven ETL pipeline built using **LocalStack**, **AWS Lambda**, **Amazon S3**, and **Amazon DynamoDB**. The project simulates a serverless AWS architecture entirely on a local machine, enabling rapid development, testing, and learning without incurring cloud costs.

---

## 📌 Project Overview

This project demonstrates how to build a serverless ETL (Extract, Transform, Load) workflow using LocalStack to emulate AWS services locally.

### Workflow

1. A CSV file is uploaded to an S3 bucket (`raw-sales`).
2. S3 notifications automatically trigger a Lambda function (`sales-transformer-v2`).
3. The Lambda function:

   * Reads the CSV file from S3.
   * Transforms each record.
   * Calculates the `total_amount` field.
4. The transformed records are stored in a DynamoDB table (`sales_summary`).

---

## 🏗️ Architecture

```text
                  +------------------+
                  | Upload CSV File  |
                  |      to S3       |
                  +--------+---------+
                           |
                           v
                +----------------------+
                |  S3 Notification     |
                +----------+-----------+
                           |
                           v
              +----------------------------+
              | sales-transformer-v2       |
              |       Lambda Function      |
              +-------------+--------------+
                            |
         +------------------+-------------------+
         |                  |                   |
         v                  v                   v
+----------------+ +----------------+ +------------------+
|   S3 Service   | | Transformation | | DynamoDB Service |
| Read CSV File  | |     Logic      | |  Persist Records |
+----------------+ +----------------+ +------------------+
                                                   |
                                                   v
                                      +----------------------+
                                      |      DynamoDB        |
                                      |   sales_summary      |
                                      +----------------------+
```

---

## 🛠️ Technologies Used

* Python 3.10+
* LocalStack
* AWS Lambda (LocalStack)
* Amazon S3 (LocalStack)
* Amazon DynamoDB (LocalStack)
* Boto3
* Pytest
* Docker

---

## 📂 Project Structure

```text
localstack-etl-pipeline/
│
├── src/
│   └── app/
│       ├── __init__.py
│       ├── clients.py
│       ├── config.py
│       ├── handler.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   └── sales_record.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   ├── s3_service.py
│       │   ├── transformation_service.py
│       │   └── dynamodb_service.py
│       │
│       └── verification/
│           ├── __init__.py
│           ├── verify_connection.py
│           ├── verify_s3_service.py
│           ├── verify_dynamodb_service.py
│           └── verify_transformation.py
│
├── tests/
│   └── test_transformation_service.py
│
├── scripts/
├── build/
├── data/
├── .env.example
├── requirements.txt
└── README.md
```

---

## ⚙️ Prerequisites

Before running this project, ensure the following are installed:

* Docker Desktop
* Python 3.10+
* LocalStack CLI
* AWS CLI
* `awslocal`

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd localstack-etl-pipeline
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment Variables

Create a `.env` file:

```env
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_DEFAULT_REGION=ap-south-1

LOCALSTACK_ENDPOINT=http://localhost:4566

S3_BUCKET=raw-sales
DYNAMODB_TABLE=sales_summary
```

---

### 4. Start LocalStack

```bash
LOCALSTACK_GATEWAY_LISTEN=0.0.0.0:4566 \
LOCALSTACK_HOST=localhost \
localstack start -d
```

Verify:

```bash
curl http://localhost:4566/_localstack/health
```

---

## ☁️ Infrastructure Setup

### Create S3 Bucket

```bash
awslocal s3 mb s3://raw-sales
```

---

### Create DynamoDB Table

```bash
awslocal dynamodb create-table \
    --table-name sales_summary \
    --attribute-definitions AttributeName=order_id,AttributeType=S \
    --key-schema AttributeName=order_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

---

## 🧪 Sample Data

Create a CSV file:

```csv
order_id,product,quantity,price
1,Laptop,2,60000
2,Mouse,3,500
3,Keyboard,1,1500
```

Save it as:

```text
data/sales.csv
```

---

## 📦 Package Lambda

```bash
find src -type d -name "__pycache__" -exec rm -rf {} +

rm -rf build/package build/function.zip

mkdir -p build/package

cp -R src/app build/package/

rm -rf build/package/app/verification

cd build/package
zip -r ../function.zip app
cd ../..
```

---

## 🔧 Deploy Lambda

```bash
awslocal lambda create-function \
    --function-name sales-transformer-v2 \
    --runtime python3.12 \
    --handler app.handler.lambda_handler \
    --zip-file fileb://build/function.zip \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --environment "Variables={
        AWS_ACCESS_KEY_ID=test,
        AWS_SECRET_ACCESS_KEY=test,
        AWS_DEFAULT_REGION=ap-south-1,
        LOCALSTACK_ENDPOINT=http://host.docker.internal:4566,
        DYNAMODB_TABLE=sales_summary,
        S3_BUCKET=raw-sales
    }"
```

---

## 🔔 Configure S3 Notifications

```bash
awslocal s3api put-bucket-notification-configuration \
    --bucket raw-sales \
    --notification-configuration '{
        "LambdaFunctionConfigurations": [
            {
                "Id": "sales-transformer-v2-trigger",
                "LambdaFunctionArn": "arn:aws:lambda:ap-south-1:000000000000:function:sales-transformer-v2",
                "Events": ["s3:ObjectCreated:*"]
            }
        ]
    }'
```

---

## ▶️ Trigger the Pipeline

Upload a CSV file:

```bash
awslocal s3 cp data/sales.csv s3://raw-sales/sales.csv
```

---

## ✅ Verify Results

### Check DynamoDB Records

```bash
awslocal dynamodb scan \
    --table-name sales_summary
```

---

### Run Unit Tests

```bash
python -m pytest
```

---

### View LocalStack Logs

```bash
localstack logs
```

---

## 🧩 Core Components

| Component               | Responsibility                     |
| ----------------------- | ---------------------------------- |
| `handler.py`            | Lambda entry point                 |
| `clients.py`            | Creates boto3 clients/resources    |
| `config.py`             | Centralized configuration          |
| `SalesRecord`           | Data model for transformed records |
| `S3Service`             | Reads CSV files from S3            |
| `TransformationService` | Applies transformation logic       |
| `DynamoDBService`       | Persists data into DynamoDB        |
| `verification/`         | Manual verification scripts        |
| `tests/`                | Automated unit tests               |

---

## 📈 Current Features

* ✅ Event-driven ETL workflow
* ✅ Local AWS simulation using LocalStack
* ✅ S3-triggered Lambda execution
* ✅ CSV processing and transformation
* ✅ DynamoDB persistence
* ✅ Service-oriented architecture
* ✅ Verification utilities
* ✅ Unit testing with Pytest

---

## 🔮 Future Enhancements

* Apache Airflow integration
* Docker Compose setup
* Terraform-based infrastructure provisioning
* CI/CD pipeline using GitHub Actions
* Data validation and schema enforcement
* Monitoring and alerting

---

## 👨‍💻 Author

**Piyush Diwaker**

Software Engineer III @ Walmart

---
