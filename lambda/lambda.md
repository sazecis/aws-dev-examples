# Creating and deploying Lambda functions

BookshelfFunction is an AWS Lambda function written in Java 11 that reads a list of books from the Bookshelf DynamoDB table. The function is designed to be used in conjunction with other services, such as an API Gateway, but during development and testing, the function can be executed from the AWS Management Console using the "Test" button. The function queries the Bookshelf table in DynamoDB for all books by a specified author, and returns the list of books as a JSON object. This Lambda function is a key component of the Bookshelf application, allowing users to view and search for books in the Bookshelf table.

## Prerequisites

To set up a Java development environment with Java 11, you'll need to have the following prerequisites installed:

- Java SE Development Kit 11 or later: https://www.oracle.com/java/technologies/javase-jdk11-downloads.html
- Apache Maven: https://maven.apache.org/install.html
- Docker: https://www.docker.com/get-started - `Optional`

Make sure to add the JDK and Maven to your system path.

You'll also need to install the AWS SAM CLI, which is a command line interface for building and deploying serverless applications using SAM. Here is the link to the AWS SAM CLI installation guide: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

Once you have the AWS SAM CLI installed, you can use it to create, build, and deploy your serverless application using the SAM template and your Lambda function code.

## Building the Lambda with SAM

To build the Lambda with SAM, follow these steps:

1. Open a command prompt or terminal.
2. Change the directory to the `lambda` folder.
3. Run the following command to build the Lambda:
```
sam build
```

This will use the `template.yaml` file to build the Lambda.

## Deploying the Lambda with SAM

To deploy the Lambda with SAM, follow these steps:

1. After the build process completes, run the following command to deploy the Lambda:
```
sam deploy --guided
```

This will use the `template.yaml` file to deploy the Lambda. You'll be prompted for information such as the AWS region and the S3 bucket to store the deployment package.

You can then use the Lambda function to interact with the Bookshelf table in DynamoDB. The source code for the Lambda function is located in the `lambda/bookshelf/BookshelfFunction/src/main/java/bookshelf` folder.

To read more about SAM command check the [README.md](/lambda/bookshelf/README.md)

More about SAM and Lambda will come in [Lambda, API Gateway and Cognito built together](/README.md#lambda-apigw-cognito)

