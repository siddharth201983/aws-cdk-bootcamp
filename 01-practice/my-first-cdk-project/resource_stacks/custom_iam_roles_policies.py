import aws_cdk as cdk
from constructs import Construct


class CustomRolesPoliciesStack(cdk.Stack):

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
        
        # Add IAM Group
        user_group1 = cdk.aws_iam.Group(self,
                                        "user_group1",
                                        group_name="user_group1"
                                        )
        
        # Add user1 in group1
        user_group1.add_user(user1)
        
        # Add Managed Policy to User Group1
        user_group1.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3ReadOnlyAccess")
        )
        
        # SSM Parameter1
        param1 = cdk.aws_ssm.StringParameter(
            self,
            "parameter1",
            parameter_name="/usergroup1/keys/fish",
            string_value="130481",
            tier=cdk.aws_ssm.ParameterTier.STANDARD
        )
        
        # SSM Parameter2
        param2 = cdk.aws_ssm.StringParameter(
            self,
            "parameter2",
            parameter_name="/usergroup1/keys/fish/gold",
            string_value="130482",
            tier=cdk.aws_ssm.ParameterTier.STANDARD
        )
        
        # Grant UserGroup1 permission to param1
        param1.grant_read(user_group1)
        
        # Grant Group1 to LIST ALL SSM Parameters in Console
        grpStmt1 = cdk.aws_iam.PolicyStatement(
            effect=cdk.aws_iam.Effect.ALLOW,
            resources=["*"],
            actions=["ssm:DescribeParameters"]
        )
        grpStmt1.sid="DescribeAllParametersInConsole"
        
        # Add Permissions to UserGroup
        user_group1.add_to_policy(grpStmt1)
        
        # Create IAM Role
        user_group1_role = cdk.aws_iam.Role(
            self,
            "userGroup1OpsRole",
            assumed_by=cdk.aws_iam.AccountPrincipal(f"{cdk.Aws.ACCOUNT_ID}"),
            role_name="user_group1_role"
        )
        
        # Create Managed Policy & Attach to the IAM Role
        list_ec2_policy = cdk.aws_iam.ManagedPolicy(
            self,
            "listEc2Instances",
            description="list ec2 instances in the account",
            managed_policy_name="list_ec2_policy",
            statements=[
                cdk.aws_iam.PolicyStatement(
                    effect=cdk.aws_iam.Effect.ALLOW,
                    actions=[
                        "ec2:Describe*",
                        "cloudwatch:Describe*",
                        "cloudwatch:Get*"
                    ],
                    resources=["*"]
                )
            ],
            roles=[
                user_group1_role
            ]
        )
        
        # User Login URL Autogeneration
        cdk.CfnOutput(self,
                    "user1LoginUrl",
                    description="Login URL for User1",
                    value=f"https://{cdk.Aws.ACCOUNT_ID}.signin.aws.amazon.com/console"
                    )
        