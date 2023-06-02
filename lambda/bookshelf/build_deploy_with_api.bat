call sam build --parameter-overrides BookshelfUserPoolArn=%1
call sam deploy --guided --stack-name bookshelf --parameter-overrides BookshelfUserPoolArn=%1
