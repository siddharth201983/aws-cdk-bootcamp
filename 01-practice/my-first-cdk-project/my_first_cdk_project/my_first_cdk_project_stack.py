#!/usr/bin/env node --no-warnings
import aws_cdk as cdk
from constructs import Construct
# from aws_cdk import (
#     Stack,
#     aws_s3 as _s3,
#     aws_iam as _iam
# )


class MyArtifactBucketStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, is_prod=False, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        print(self.node.try_get_context('prod')['region'])

        if is_prod:
            cdk.aws_s3.Bucket(self,
                              "myProdArtifactBucketId",
                              versioned=True,
                              encryption=cdk.aws_s3.BucketEncryption.S3_MANAGED,
                              removal_policy=cdk.RemovalPolicy.RETAIN)
        else:
            cdk.aws_s3.Bucket(self,
                              "myDevArtifactBucketId",
                              removal_policy=cdk.RemovalPolicy.DESTROY)
