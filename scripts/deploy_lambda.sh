#!/bin/bash

set -e

FUNCTION_NAME="sales-transformer-v2"

if awslocal lambda get-function \
    --function-name $FUNCTION_NAME >/dev/null 2>&1; then

    echo "Updating existing Lambda..."

    awslocal lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://build/function.zip

else

    echo "Creating Lambda..."

    awslocal lambda create-function \
        --function-name $FUNCTION_NAME \
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

fi

echo "Configuring S3 notifications..."

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

echo "Lambda deployment completed!"
```
