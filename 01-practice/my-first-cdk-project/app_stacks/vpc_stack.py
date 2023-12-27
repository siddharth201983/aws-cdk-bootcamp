import aws_cdk as cdk
from constructs import Construct


class VpcStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = cdk.aws_ec2.Vpc(
            self,
            "customVpcId",
            ip_addresses=cdk.aws_ec2.IpAddresses.cidr("10.10.0.0/16"),
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                cdk.aws_ec2.SubnetConfiguration(
                    name="publicSubnet",
                    cidr_mask=24,
                    subnet_type=cdk.aws_ec2.SubnetType.PUBLIC
                ),
                cdk.aws_ec2.SubnetConfiguration(
                    name="privateSubnet",
                    cidr_mask=24,
                    subnet_type=cdk.aws_ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
                cdk.aws_ec2.SubnetConfiguration(
                    name="dbSubnet",
                    cidr_mask=24,
                    subnet_type=cdk.aws_ec2.SubnetType.PRIVATE_ISOLATED
                )
            ]
        )

        cdk.CfnOutput(self,
                      "customVpcIdOutput",
                      value=self.vpc.vpc_id,
                      export_name="VpcId"
                      )
