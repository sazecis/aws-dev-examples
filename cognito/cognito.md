## Creating and managing Cognito user pools with AWS CDK

Amazon `Cognito` is a fully managed service that makes it easy to add user sign-up, sign-in, and access control to your web and mobile apps. With Cognito, you can easily create and manage user pools and identity pools so you can authenticate and authorize access to your AWS resources.

For the Bookshelf demo, we'll be using Cognito to authenticate users with a user pool and use the JWT token to access the API Gateway content. We'll be using the AWS `Cloud Development Kit` (CDK) to create and manage our Cognito resources.

Before we get started with creating our Cognito user pool with CDK, we need to ensure that we have CDK installed and initialized in our project directory. To install CDK, you can use the following command:

```
npm install -g aws-cdk
```
More information in the [getting started guide](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html)

Once CDK is installed, you can initialize a new CDK project by running the following commands:
```
cdk init app --language python
cdk bootstrap
```


These commands will create a new CDK project and initialize the required AWS resources to deploy your CDK stack.

To create the Cognito user pool with CDK, we used the `cognito.UserPool` construct provided by the AWS CDK. The `UserPool` construct defines a new Cognito user pool with the specified settings.

To generate the CloudFormation template for our Cognito user pool, we can use the `cdk synth` command.

To deploy the UserPool execute the deploy command in the `cognito` directory:
```
cdk deploy
```

