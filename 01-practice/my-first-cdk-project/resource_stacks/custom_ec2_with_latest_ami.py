import aws_cdk as cdk
from constructs import Construct


class CustomEc2LatestAmiStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = cdk.aws_ec2.Vpc.from_lookup(
            self,
            # is_default=True,
            "importedVPC",
            vpc_id="vpc-01bff703c3919e59b"
        )

        # Read Bootstrap script
        with open("bootstrap_scripts/install_httpd.sh") as file:
            data = file.read()

        amazn_linux_ami = cdk.aws_ec2.MachineImage.latest_amazon_linux2(
            edition=cdk.aws_ec2.AmazonLinuxEdition.STANDARD,
            storage=cdk.aws_ec2.AmazonLinuxStorage.EBS,
            virtualization=cdk.aws_ec2.AmazonLinuxVirt.HVM
        )
        
        # WebServer Instance 001
        web_server = cdk.aws_ec2.Instance(
            self,
            "webServer002Id",
            vpc=vpc,
            vpc_subnets=cdk.aws_ec2.SubnetSelection(
                subnet_type=cdk.aws_ec2.SubnetType.PUBLIC
            ),
            instance_name="WebServer002",
            instance_type=cdk.aws_ec2.InstanceType("t3.micro"),
            # machine_image=cdk.aws_ec2.MachineImage.generic_linux({"us-east-1": "ami-079db87dc4c10ac91"}),
            machine_image=amazn_linux_ami,
            user_data=cdk.aws_ec2.UserData.custom(data)
        )

        cdk.CfnOutput(self,
                      "webServer002IpOutput",
                      value=f"http://{web_server.instance_public_ip}",
                      export_name="webServer002PublicIp"
                      )

        # Allow Web Traffic to webserver002
        web_server.connections.allow_from_any_ipv4(
            cdk.aws_ec2.Port.tcp(80), description="Allow Web Traffic"
        )

        # Add permissions to web server instance profile
        web_server.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMManagedInstanceCore"
            )
        )

        web_server.role.add_managed_policy(
            cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonS3ReadOnlyAccess"
            )
        )
        