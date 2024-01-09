import aws_cdk as cdk
from constructs import Construct


class CustomS3ResourcePolicyStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        my_s3_bkt = cdk.aws_s3.Bucket(
            self,
            "mys3bucket",
            versioned=True,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
        
        # Add S3 Bucket Resource Policy
        my_s3_bkt.add_to_resource_policy(
            cdk.aws_iam.PolicyStatement(
                effect=cdk.aws_iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                resources=[my_s3_bkt.arn_for_objects("*.html")],
                principals=[cdk.aws_iam.AnyPrincipal()]
            )
        )
        
        my_s3_bkt.add_to_resource_policy(
            cdk.aws_iam.PolicyStatement(
                effect=cdk.aws_iam.Effect.DENY,
                actions=["s3:*"],
                resources=[f"{my_s3_bkt.bucket_arn}/*"],
                principals=[cdk.aws_iam.AnyPrincipal()],
                conditions={
                    "Bool": {"aws:SecureTransport": False}
                }
            )
        )
        