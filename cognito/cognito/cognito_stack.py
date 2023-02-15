from aws_cdk import (
    Stack,
    aws_cognito,
    aws_iam
)
from constructs import Construct

class CognitoStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        user_pool = aws_cognito.UserPool(
            self, "myUserPool",
            user_pool_name="myUserPool",
            self_sign_up_enabled=True,
            auto_verify=aws_cognito.AutoVerifiedAttrs(email=True),
            sign_in_aliases=aws_cognito.SignInAliases(email=True),
            password_policy=aws_cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True
            )
        )

        app_client = user_pool.add_client(
            "myAppClient",
            generate_secret=False,
            o_auth=aws_cognito.OAuthSettings(
                flows=aws_cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=True
                ),
                scopes=[aws_cognito.OAuthScope.EMAIL,
                        aws_cognito.OAuthScope.OPENID]
            )
        )

        identity_pool = aws_cognito.CfnIdentityPool(
            self, "myIdentityPool",
            allow_unauthenticated_identities=False,
            cognito_identity_providers=[
                {
                    "clientId": app_client.user_pool_client_id,
                    "providerName": "cognito-idp." + self.region + ".amazonaws.com/" + user_pool.user_pool_id,
                    "serverSideTokenCheck": False
                }
            ]
        )

        authenticated_role = aws_iam.Role(
            self, "your-authenticated-role",
            assumed_by=aws_iam.FederatedPrincipal(
                "cognito-identity.amazonaws.com",
                {
                    "StringEquals": {"cognito-identity.amazonaws.com:aud": identity_pool.ref},
                    "ForAnyValue:StringLike": {"cognito-identity.amazonaws.com:amr": "authenticated"}
                },
                "sts:AssumeRoleWithWebIdentity"
            )
        )

        authenticated_role.add_to_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=[
                    "s3:Get*",
                    "s3:List*"
                ],
                resources=[
                    "arn:aws:s3:::my-bucket",
                    "arn:aws:s3:::my-bucket/*"
                ]
            )
        )

        role_mapping = aws_cognito.CfnIdentityPoolRoleAttachment(
            self, "myIdentityPoolRoleMapping",
            identity_pool_id=identity_pool.ref,
            roles={
                "authenticated": authenticated_role.role_arn
            }
        )
