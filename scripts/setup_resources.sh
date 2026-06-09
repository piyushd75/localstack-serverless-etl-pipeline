awslocal s3 mb s3://raw-sales

awslocal dynamodb create-table \
    --table-name sales_summary \
    --attribute-definitions AttributeName=order_id,AttributeType=S \
    --key-schema AttributeName=order_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

awslocal lambda create-function \
    --function-name sales-transformer \
    --runtime python3.12 \
    --handler transform.lambda_handler \
    --zip-file fileb://lambda/function.zip \
    --role $ROLE_ARN \
    --environment "Variables={LOCALSTACK_ENDPOINT=http://host.docker.internal:4566}"