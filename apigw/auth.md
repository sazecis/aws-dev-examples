# Use Cognito authorizer to authenticate users using the Bookshelf API Gateway

In the prevoius steps we created
- a user in IAM
- an S3 bucket
- a DynamoDB table
- a Lambda function
- an API Gatway endpoint
- a Cognito user pool

Now we will take two steps back and will deploy our SAM template with some parameters which will create us a new API Gateway REST API. It will also set the created User Pool as authorizer for it. After this we also need to update our webpage content so it would use the new endpoint and the corect user pool.

## Deploying SAM with condition

Our `SAM` template is prepared in such a way that in case if we provide a value for the `BookshelfUserPoolArn` parameter then it will deploy for us an API Gateway with a Cognito authorizer.
`API Gateway` provides built-in support for using `Cognito user pools` as an `authorizer` for your APIs. This allows you to add authentication and authorization to your APIs using Cognito, without having to write any custom code. When you enable Cognito authorizer for your API Gateway endpoints, API Gateway will `automatically validate JWT tokens` generated by Cognito user pools, and grant or deny access to your APIs based on the token's claims. This makes it easy to secure your APIs and control access to your resources.

To make this deployment easier you just need to use the `/lambda/bookshelf/build_deploy_with_api.bat` file. It will do the build and deplyoment for you. What you just need to provide is the parameter of the Cognito User Pool:
```
build_deploy_with_api.bat <cognito_user_pool_arn>
```
The User Pool ARN was noted down after the creation with CDK at [Cognito section](/cognito/cognito.md#user-pool-arn).

After successful execution you will have a new Lambda function with a connected and protected API Gateway endpoint.

>**Note**
>There is a manual step required to make the whole solution to work. On the Management Console at the API Gateway service in the bookshelf >API at the /books/OPTIONS method at the Method Request the Authorizer must be set to None, must be saved and the whole API needs to be >redeployed.

### Noting down the API endpoint <a name="api-endpoint"></a>

```
------------------------------------------------------------------------------------------
Outputs                                                                                                                                                                        
------------------------------------------------------------------------------------------
Key                 BookshelfApi
Description         API Gateway endpoint URL for Prod stage for Bookshelf function
Value               https://<some_code>.execute-api.eu-central-1.amazonaws.com/Prod/books/
```
Note down the enpoint which you receive at the Value field.

## Updating the S3 static webpage

We arrived at the final preparation steps to have our end-to-end serverless Bookshelf application fully functional.

We need to specify in the `Javascript` code of our web page the API Gateway endpoint, Cognito User Pool Id and then we will also need to create a test user with which we can sign in into our application.

### Update the books.html

In the `s3` directory execute the `up_books_html.py`:
```
python up_books_html.py <api_gateway_url>
```
The `api_gateway_url` is the one which you noted down at [Noting down the API endpoint](/apigw/auth.md#api-endpoint)

### Update the HTML files

Go to the `cognito` directory and execute:
```
get_pools.bat
```
This will provide you with the `user pool id` and `app client id` values.
>**Note**
>In case you have other User Pools already created you need to lookup these values manually.


In the `s3` directory execute the `up_index_html.py`:
```
python up_index_html.py <user_pool_id> <app_client_id>
```

Now you have your html files updated, you just need to upload them to the S3 bucket which you created in [Managing S3 buckets and objects with `python SDK`](/s3/s3.md).
The whole webpage content is located in `/s3/web` folder. You can upload the whole folder with the `demo_s3.py` command:
```
python demo_s3.py upload-file web <my-bucket-name> --public
```
The bucket is already configured as a static website. The files uploaded are made public using the `--public` option. Your webpage is ready, now you just need to create a user in the cognito user pool. To create the user use the `create-user.bat` in `cognito` folder:
```
create_user.bat <user_name> <password>
```
>**Note**
>The `create_user.bat` calls the `get_pools.bat` which runs with the assumptions that there is only one cognito user pool in the account region where you are running this demo. If you have multiple user pools then you can try to update the batch or you can get the `UserPoolId` and `AppClientId` from the AWS Management Console.

## You are ready

You just need to look up the URL of your S3 static website, which can be found on the S3 dasboard: `bucket > properties > Static website hosting` and click on the link.
This will open the `Bookshelf` website for you where you can log in with the above created user name and see the list of books which you added into the `DynomoDB` table.