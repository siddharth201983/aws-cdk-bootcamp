import aws_cdk as cdk
from constructs import Construct
import json


class CustomParametersSecretsStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # AWS Secrets & SSM parameters
        param1 = cdk.aws_ssm.StringParameter(
            self,
            "parameter1",
            description="Load Testing Configuration",
            parameter_name="NoOfConcurrentUsers",
            string_value="100",
            tier=cdk.aws_ssm.ParameterTier.STANDARD,
        )
        
        param2 = cdk.aws_ssm.StringParameter(
            self,
            "parameter2",
            description="Load Testing Configuration",
            parameter_name="/locust/configs/NoOfConcurrentUsers",
            string_value="100",
            tier=cdk.aws_ssm.ParameterTier.STANDARD,
        )
        
        param3 = cdk.aws_ssm.StringParameter(
            self,
            "parameter3",
            description="Load Testing Configuration",
            parameter_name="/locust/configs/DurationInSec",
            string_value="300",
            tier=cdk.aws_ssm.ParameterTier.STANDARD,
        )
        
        secret1 = cdk.aws_secretsmanager.Secret(
            self,
            "secret1",
            description="Customer DB password",
            secret_name="cust_db_pass"
        )
        
        templated_secret = cdk.aws_secretsmanager.Secret(
            self,
            "templated_secret",
            description="Customer DB password in the form of templated secret",
            secret_name="cust_secret_attrobute",
            generate_secret_string=cdk.aws_secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps(
                    {"username": "user1"}
                ),
            generate_string_key="secret_password"
            )
        )
        
        cdk.CfnOutput(
            self,
            "param1Output",
            description="NoOfConcurrentUsers",
            value=f"{param1.string_value}",
        )
        
        cdk.CfnOutput(
            self,
            "secret1Output",
            description="secret1",
            value=f"{secret1.secret_value}",
        )
        