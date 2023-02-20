@echo off

call get_pools.bat

aws cognito-idp sign-up --client-id %APP_CLIENT_ID% --username reader --password books1

aws cognito-idp admin-confirm-sign-up --user-pool-id %USER_POOL_ID% --username reader