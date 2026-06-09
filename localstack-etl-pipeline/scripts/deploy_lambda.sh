cd lambda

zip function.zip transform.py

awslocal lambda update-function-code \
    --function-name sales-transformer \
    --zip-file fileb://function.zip