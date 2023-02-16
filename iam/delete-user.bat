@echo off

call delete-access-keys.bat %1

for /f "delims=" %%i in ('aws configure get region') do set AWS_REGION=%%i
set POLICY_NAME=bookshelf-policy
set USER_NAME=%1

rem Get policy ARN
for /f "delims=" %%i in ('aws iam list-policies --query "Policies[?PolicyName=='%POLICY_NAME%'].Arn" --output text') do set POLICY_ARN=%%i

rem Detach policy from user
aws iam detach-user-policy --policy-arn %POLICY_ARN% --user-name %USER_NAME%

echo Detached policy %POLICY_ARN% from user %USER_NAME%

rem Delete IAM user
aws iam delete-user --user-name %USER_NAME%

echo Deleted IAM user %USER_NAME%

rem Delete IAM policy
aws iam delete-policy --policy-arn %POLICY_ARN%

echo Deleted IAM policy %POLICY_NAME%

del access_key.json
