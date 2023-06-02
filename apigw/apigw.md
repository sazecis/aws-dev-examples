## Managing API Gateway endpoints

Amazon API Gateway is a fully managed service that makes it easy to create, publish, and secure APIs at any scale. API Gateway provides a wide range of features to help you manage your APIs, including support for Swagger, which is an open-source framework for designing and documenting APIs.

Swagger is a powerful tool for API development, allowing developers to define APIs in a human-readable format that can be easily shared and understood. API Gateway supports importing Swagger files to create or update REST APIs.

To import a Swagger file into API Gateway using the AWS CLI, use the `create-rest-api` or the AWS Management Console.

This command will create a new REST API in API Gateway using the Swagger definition in the specified YAML file. Note that you must have the `AmazonAPIGatewayFullAccess` permission in your AWS account to run this command.

It's important to note that while Swagger is a powerful tool for designing and documenting APIs, it is not required to use API Gateway. API Gateway also provides a web-based interface for creating and managing APIs, which may be more suitable for some use cases.

For the Bookshelf demo, we won't be using Swagger to manage our API Gateway endpoints, but it's a powerful tool that can be useful in many other contexts.
