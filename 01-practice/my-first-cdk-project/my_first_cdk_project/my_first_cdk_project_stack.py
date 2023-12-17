#!/usr/bin/env node --no-warnings

from aws_cdk import (
    Stack,
    aws_s3 as _s3
)
from constructs import Construct


class MyFirstCdkProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        _s3.Bucket(
            self,
            "myBucketId",
            bucket_name="myfirstcdkproject-sid-2024",
            versioned=True,
            encryption=_s3.BucketEncryption.S3_MANAGED,
        )
