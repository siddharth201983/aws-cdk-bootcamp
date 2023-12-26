import aws_cdk as cdk

from resource_stacks.custom_vpc import CustomVpcStack

from resource_stacks.custom_ec2 import CustomEc2Stack

app = cdk.App()

env = cdk.Environment(account=app.node.try_get_context('envs')['prod']['account'], region=app.node.try_get_context('envs')['prod']['region'])

CustomVpcStack(app, "my-custom-vpc-stack", env=env)

CustomEc2Stack(app, "my-custom-ec2-stack", env=env)

cdk.Tags.of(app).add("Email", app.node.try_get_context('envs')['prod']['email'])

app.synth()
