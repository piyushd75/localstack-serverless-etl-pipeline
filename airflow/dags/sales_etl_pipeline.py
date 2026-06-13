from datetime import datetime
import time

import boto3

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import (
    PythonOperator,
    get_current_context,
)


def upload_to_s3():
    """
    Upload the user-provided CSV file
    from Airflow include/uploads to S3.
    """

    context = get_current_context()

    dag_run = context["dag_run"]

    file_name = dag_run.conf.get("file_name")

    if not file_name:
        raise ValueError(
            "file_name is required."
        )

    csv_path = (
        f"/usr/local/airflow/include/uploads/{file_name}"
    )

    print(f"Uploading {csv_path} to S3...")

    s3 = boto3.client(
        "s3",
        endpoint_url="http://host.docker.internal:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="ap-south-1",
    )

    s3.upload_file(
        csv_path,
        "raw-sales",
        file_name,
    )

    print(
        f"{file_name} uploaded successfully"
    )


def wait_for_lambda():
    """
    Wait for LocalStack Lambda execution.
    """

    print(
        "Waiting for Lambda execution..."
    )

    time.sleep(20)


def validate_dynamodb():
    """
    Verify that records have been written
    to DynamoDB.
    """

    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://host.docker.internal:4566",
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="ap-south-1",
    )

    table = dynamodb.Table(
        "sales_summary"
    )

    response = table.scan()

    count = response["Count"]

    print(
        f"Records found: {count}"
    )

    if count == 0:
        raise ValueError(
            "No records found in DynamoDB"
        )

    print(
        "Validation successful"
    )


with DAG(
    dag_id="sales_etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=[
        "localstack",
        "etl",
        "streamlit",
    ],
) as dag:

    start = EmptyOperator(
        task_id="start"
    )

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

    end = EmptyOperator(
        task_id="end"
    )

    start >> upload >> wait >> validate >> end