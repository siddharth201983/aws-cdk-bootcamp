import aws_cdk as cdk

from resource_stacks.custom_vpc import CustomVpcStack

app = cdk.App()

CustomVpcStack(app, "my-custom-vpc-stack")

cdk.Tags.of(app).add("Email", app.node.try_get_context('envs')['prod']['email'])

app.synth()
