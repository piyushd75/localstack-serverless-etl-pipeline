from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

from datetime import datetime
import boto3
import time


def upload_to_s3():
    s3 = boto3.client(
        "s3",
        endpoint_url="http://host.docker.internal:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="ap-south-1",
    )

    s3.upload_file(
        "/usr/local/airflow/include/sales.csv",
        "raw-sales",
        "sales_airflow.csv",
    )

    print("File uploaded successfully")
    
def wait_for_lambda():
    print("Waiting for Lambda execution...")
    time.sleep(20)
    
def validate_dynamodb():
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://host.docker.internal:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="ap-south-1",
    )

    table = dynamodb.Table("sales_summary")

    response = table.scan()

    count = response["Count"]

    print(f"Records found: {count}")

    if count == 0:
        raise ValueError(
            "No records found in DynamoDB"
        )

    print("Validation successful")


with DAG(
    dag_id="sales_etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["localstack", "etl"],
) as dag:

    start = EmptyOperator(task_id="start")

    upload = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_to_s3,
    )

    wait = PythonOperator(
        task_id="wait_for_lambda",
        python_callable=wait_for_lambda,
    )

    validate = PythonOperator(
        task_id="validate_dynamodb",
        python_callable=validate_dynamodb,
    )

    end = EmptyOperator(task_id="end")

    start >> upload >> wait >> validate >> end