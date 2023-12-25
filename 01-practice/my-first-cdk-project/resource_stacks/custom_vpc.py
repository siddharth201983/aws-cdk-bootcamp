import aws_cdk as cdk
from constructs import Construct


class CustomVpcStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prod_configs = self.node.try_get_context('envs')['prod']

        custom_vpc = cdk.aws_ec2.Vpc(
            self,
            "customVpcId",
            ip_addresses=cdk.aws_ec2.IpAddresses.cidr(prod_configs['vpc_configs']['vpc_cidr']),
            # cidr=prod_configs['vpc_configs']['vpc_cidr'], # deprecated.
            max_azs=3,
            nat_gateways=1,
            subnet_configuration=[
                cdk.aws_ec2.SubnetConfiguration(
                    name="publicSubnet",
                    cidr_mask=prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type=cdk.aws_ec2.SubnetType.PUBLIC
                ),
                cdk.aws_ec2.SubnetConfiguration(
                    name="privateSubnet",
                    cidr_mask=prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type=cdk.aws_ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
                cdk.aws_ec2.SubnetConfiguration(
                    name="dbSubnet",
                    cidr_mask=prod_configs['vpc_configs']['cidr_mask'],
                    subnet_type=cdk.aws_ec2.SubnetType.PRIVATE_ISOLATED
                )
            ]
        )

        cdk.CfnOutput(self,
                      "customVpcIdOutput",
                      value=custom_vpc.vpc_id,
                      export_name="customVpcId"
                      )
