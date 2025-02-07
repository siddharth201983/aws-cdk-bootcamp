#!/usr/bin/env python3
# import os
import aws_cdk as cdk

from my_first_cdk_project.my_first_cdk_project_stack import MyArtifactBucketStack
app = cdk.App()
env_US = cdk.Environment(account=app.node.try_get_context('dev')['account'], region=app.node.try_get_context('dev')['region'])
env_AU = cdk.Environment(account=app.node.try_get_context('prod')['account'], region=app.node.try_get_context('prod')['region'])

print(app.node.try_get_context('dev')['account'])
MyArtifactBucketStack(app, "myDevStack", env=env_US
                      # If you don't specify 'env', this stack will be environment-agnostic.
                      # Account/Region-dependent features and context lookups will not work,
                      # but a single synthesized template can be deployed anywhere.

                      # Uncomment the next line to specialize this stack for the AWS Account
                      # and Region that are implied by the current CLI configuration.

                      # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

                      # Uncomment the next line if you know exactly what Account and Region you
                      # want to deploy the stack to. */

                      # env=cdk.Environment(account='123456789012', region='us-east-1'),

                      # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                      )
MyArtifactBucketStack(app, "myProdStack", is_prod=True, env=env_AU)
app.synth()
