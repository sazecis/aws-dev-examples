@echo off

REM Retrieve the first user pool in the account
set USER_POOL_ID=
for /f "delims=" %%i in ('aws cognito-idp list-user-pools --max-results 1 --query "UserPools[0].Id" --output text') do set USER_POOL_ID=%%i

if "%USER_POOL_ID%"=="" (
    echo Error: Failed to retrieve User Pool ID
    exit /b 1
)

echo User Pool ID: %USER_POOL_ID%

REM Retrieve the first app client in the user pool
set APP_CLIENT_ID=
for /f "delims=" %%i in ('aws cognito-idp list-user-pool-clients --user-pool-id %USER_POOL_ID% --max-results 1 --query "UserPoolClients[0].ClientId" --output text') do set APP_CLIENT_ID=%%i

if "%APP_CLIENT_ID%"=="" (
    echo Error: Failed to retrieve App Client ID
    exit /b 1
)

echo App Client ID: %APP_CLIENT_ID%
