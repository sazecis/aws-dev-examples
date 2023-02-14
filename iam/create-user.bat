@echo off

for /f "delims=" %%i in ('aws configure get region') do set AWS_REGION=%%i

set POLICY_NAME=s3-full-access
set POLICY_DOCUMENT=s3-policy.json
set USER_NAME=%1
set ACCESS_KEY_ID=
set SECRET_ACCESS_KEY=

rem Create IAM policy with full access to S3
aws iam create-policy --policy-name %POLICY_NAME% --policy-document file://%POLICY_DOCUMENT%

echo Created IAM policy %POLICY_NAME%

rem Create IAM user
aws iam create-user --user-name %USER_NAME%

echo Created IAM user %USER_NAME%

rem Get policy ARN
for /f "delims=" %%i in ('aws iam list-policies --query "Policies[?PolicyName=='%POLICY_NAME%'].Arn" --output text') do set POLICY_ARN=%%i

echo Retrieved policy ARN: %POLICY_ARN%

rem Attach policy to user
aws iam attach-user-policy --policy-arn %POLICY_ARN% --user-name %USER_NAME%

echo Attached policy %POLICY_ARN% to user %USER_NAME%

rem Generate access key for user
aws iam create-access-key --user-name %USER_NAME% > access_key.json

for /f %%a in ('jq -r ".AccessKey.AccessKeyId" access_key.json') do (
  set ACCESS_KEY_ID=%%a
)

for /f %%a in ('jq -r ".AccessKey.SecretAccessKey" access_key.json') do (
  set SECRET_ACCESS_KEY=%%a
)

aws configure set aws_access_key_id %ACCESS_KEY_ID% --profile %USER_NAME%
aws configure set aws_secret_access_key %SECRET_ACCESS_KEY% --profile %USER_NAME%

echo Created IAM user %USER_NAME% with programmatic access
echo AWS CLI credentials configured for user %USER_NAME% using profile %USER_NAME%

set ACCESS_KEY_ID=
set SECRET_ACCESS_KEY=

