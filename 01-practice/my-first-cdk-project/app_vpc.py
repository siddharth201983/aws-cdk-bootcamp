import aws_cdk as cdk

from resource_stacks.custom_vpc import CustomVpcStack

app = cdk.App()

CustomVpcStack(app, "my-custom-vpc-stack", env=cdk.Environment(account=app.node.try_get_context('envs')['prod']['account'], region=app.node.try_get_context('envs')['prod']['region']))

cdk.Tags.of(app).add("Email", app.node.try_get_context('envs')['prod']['email'])

app.synth()
