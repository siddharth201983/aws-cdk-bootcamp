import aws_cdk as cdk
from constructs import Construct


class RdsDatabase3TierStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create an RDS Database
        