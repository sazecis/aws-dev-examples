# AWS Dev Examples

This is a collection of examples and demos that I use in Developing on AWS classes. These examples cover various AWS services and development tools like: `AWS CLI`, `SAM`, `CloudFormation`, `CDK` and some more.
The whole application deployment is willingly not done with full automation. Manual steps are part of the demo. The manual steps are described below and are dependent on each other. Follow the step-by-step execution from top to bottom.

## 1. IAM

- [Managing users using AWS CLI and `Windows Batch`](/iam/iam.md)

## 2. S3

- [Managing S3 buckets and objects with `python SDK`](/s3/s3.md)

## 3. DynamoDB

- [Creating and managing DynamoDB tables with `.NET SDK`](/dynamodb/dynamodb.md)

## 4. Lambda

- [Creating and deploying Lambda functions with `SAM` and `Java SDK`](/lambda/lambda.md)

## 5. API Gateway

- [Managing API Gateway endpoints with `Swagger UI`](/apigw/apigw.md)

## 6. Cognito

- [Creating and managing Cognito user pools with `AWS CDK`](/cognito/cognito.md)

## 7. Lambda, API Gateway and Cognito built together <a name="lambda-apigw-cognito"></a>

- [Use Cognito authorizer to authenticate users using the Bookshelf API Gateway - `SAM`](/apigw/auth.md)

## 8. Cleanup

For cleaning up the created resources I prepared a batch file located in the root folder: `cleanup.bat`.
To be able to clean the user which we created to do the whole demo you need to switch to another, e.g. Admin user.
For this case I have a profile prepared so I just need to set my profile to that profile:
```
set AWS_PROFILE=<admin_profile>
```
After this just execute the `cleanup.bat`.