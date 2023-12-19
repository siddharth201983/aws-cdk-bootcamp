#!/usr/bin/env node --no-warnings
import aws_cdk as core
from aws_cdk import (
    Stack,
    aws_s3 as _s3,
    aws_iam as _iam
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
            versioned=False,
            encryption=_s3.BucketEncryption.S3_MANAGED,
            block_public_access=_s3.BlockPublicAccess.BLOCK_ALL,
        )

        mybucket = _s3.Bucket(
            self,
            "myBucketId1"
        )

        snstopicname = "abcxyz1234"
        if not core.Token.is_unresolved(snstopicname) and len(snstopicname) > 10:
            raise ValueError("Max value length can be 10 char only")
        print(mybucket.bucket_name)

        _iam.Group(
            self,
            "gid"
        )

        output_1 = core.CfnOutput(
            self,
            "myBucketOutput1",
            value=mybucket.bucket_arn,
            description="My first CDK Bucket",
            export_name="myBucketOutput1"
        )
