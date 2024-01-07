import aws_cdk as cdk
from constructs import Construct


class CustomIamUsersGroupsStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # AWS IAM User Groups
        user1_pass = cdk.aws_secretsmanager.Secret(
            self,
            "user1pass",
            description="Password for User1",
            secret_name="user1_pass"
        )
        
        # Add User1 with SecretsManager Password
        user1 = cdk.aws_iam.User(self,
                                 "user1",
                                 password=user1_pass.secret_value,
                                 user_name="user1"
                                 )
        
        # Add User2 with Literal Password
        user2 = cdk.aws_iam.User(self,
                                 "user2",
                                 password=cdk.SecretValue.unsafe_plain_text(
                                     "D0nt-Use-B@d-Passw0rds"),
                                 user_name="user2"
                                 )
        
        # Add IAM Group
        user_group1 = cdk.aws_iam.Group(self,
                                        "user_group1",
                                        group_name="user_group1"
                                        )
        
        # Add user2 in group1
        user_group1.add_user(user2)
        
        # User Login URL Autogeneration
        output_1 = cdk.CfnOutput(self,
                                 "user2LoginUrl",
                                 description="Login URL for User2",
                                 value=f"https://{cdk.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
                                 )
        
        