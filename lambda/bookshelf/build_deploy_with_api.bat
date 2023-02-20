call sam build --parameter-overrides BookshelfUserPoolArn=%1
call sam deploy --stack-name bookshelf --parameter-overrides BookshelfUserPoolArn=%1
