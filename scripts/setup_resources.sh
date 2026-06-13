#!/bin/bash

awslocal s3 mb s3://raw-sales || true

awslocal dynamodb create-table \
    --table-name sales_summary \
    --attribute-definitions AttributeName=order_id,AttributeType=S \
    --key-schema AttributeName=order_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST || true