@echo off

echo Cognito cleanup started
cd cognito
call cdk destroy --force
cd ..
echo Cognito destroyed

echo Lambda bookshelf stack cleanup started
aws cloudformation delete-stack --stack-name bookshelf
echo Lambda bookshelf stack destroyed

for /f "delims=" %%i in ('aws apigateway get-rest-apis --query "items[?name=='Bookshelf API'].id" --output text') do (
    set REST_API_ID=%%i
)

echo ApiGw imported from Swagger cleanup started
aws apigateway delete-rest-api --rest-api-id %REST_API_ID%
echo ApiGw imported from Swagger deleted

echo DynamoDb table cleanup started
cd dynamodb
call dotnet run -- delete
cd ..
echo DynamoDb table deleted

echo S3 bucket cleanup started
cd s3
demo_s3.py delete-bucket bookshelf-demo
cd ..
echo S3 bucket deleted

echo IAM user cleanup started
cd iam
delete-user.bat oscar
cd ..
echo IAM user deleted

ap demo