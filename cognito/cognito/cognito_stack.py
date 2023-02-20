from aws_cdk import (
    Stack,
    aws_cognito,
    CfnOutput
)
from constructs import Construct

class CognitoStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        user_pool = aws_cognito.UserPool(
            self, "bookshelfUserPool",
            user_pool_name="bookshelfUserPool",
            self_sign_up_enabled=True,
            sign_in_aliases=aws_cognito.SignInAliases(username=True),
            password_policy=aws_cognito.PasswordPolicy(
                min_length=6,
                require_lowercase=False,
                require_uppercase=False,
                require_digits=False,
                require_symbols=False
            )
        )

        user_pool.add_client(
            "bookshelfClient",
            generate_secret=False
        )


        CfnOutput(self, 'UserPoolArn', value=user_pool.user_pool_arn)
