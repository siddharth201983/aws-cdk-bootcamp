# from aws_cdk import (
#     # Duration,
#     # aws_sqs as sqs
# )
from aws_cdk.core import Stack
from constructs import Construct


class MyFirstCdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "MyFirstCdkProjectQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
