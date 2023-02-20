@echo off

call get_pools.bat

aws cognito-idp sign-up --client-id %APP_CLIENT_ID% --username %1 --password %2

aws cognito-idp admin-confirm-sign-up --user-pool-id %USER_POOL_ID% --username %1