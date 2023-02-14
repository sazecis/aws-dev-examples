@echo off

set USER_NAME=%1

for /f "delims=" %%a in ('aws iam list-access-keys --user-name %USER_NAME% --query "AccessKeyMetadata[].AccessKeyId" --output text') do (
    set ACCESS_KEY_LIST=%%a
)

for %%a in (%ACCESS_KEY_LIST%) do (
    echo Deleting access key %%a for user %USER_NAME%...
    aws iam delete-access-key --access-key-id "%%a" --user-name %USER_NAME%
)

echo Deleted all access keys for IAM user %USER_NAME%

set ACCESS_KEY_LIST=