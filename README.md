# AWS Dev Examples

This is a collection of examples and demos that I use in Developing on AWS classes. These examples cover various AWS services and use cases.
The whole application deployment is willingly not done with full automation. Manual steps are part of the demo. The manual steps are described below and are dependent on each other. Follow the step-by-step execution from top to bottom.

## Table of Contents

- [IAM](#iam)
- [S3](#s3)
- [DynamoDB](#dynamodb)
- [Lambda](#lambda)
- [API Gateway](#api-gateway)
- [Cognito](#cognito)
- [StepFunctions](#stepfunctions)
- [CodePipeline](#codepipeline)

## 1. IAM

- [Managing users using AWS CLI and `Windows Batch`](/iam/iam.md)

## 2. S3

- [Managing S3 buckets and objects with `python SDK`](/s3/s3.md)

## DynamoDB

- [Creating and managing DynamoDB tables with `.NET`](/dynamodb/dynamodb.md)

## Lambda

- [Creating and deploying Lambda functions with `SAM` and `Java`](/lambda/lambda.md)

## API Gateway

- [Managing API Gateway endpoints with `Swagger UI`](/apigw/apigw.md)

## Cognito

- [Creating and managing Cognito user pools with `AWS CDK`](/cognito/pool.md)

## Lambda, API Gateway and Cognito built together <a name="lambda-apigw-cognito"></a>

## StepFunctions

- [Creating and managing StepFunctions workflows](/stepfunctions/workflow.md)
- [Using StepFunctions with Lambda functions](/stepfunctions/lambda.md)

## CodePipeline

- [Creating and managing CodePipeline pipelines](/codepipeline/pipeline.md)
- [Automating deployments with CodePipeline](/codepipeline/deployment.md)