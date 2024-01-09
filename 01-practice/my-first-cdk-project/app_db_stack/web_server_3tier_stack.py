import aws_cdk as cdk
from constructs import Construct


class WebServer3TierStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read Bootstrap script
        with open("bootstrap_scripts/install_httpd.sh") as file:
            data = file.read()
                
        amazn_linux_ami = cdk.aws_ec2.MachineImage.latest_amazon_linux2(
            edition=cdk.aws_ec2.AmazonLinuxEdition.STANDARD,
            storage=cdk.aws_ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            virtualization=cdk.aws_ec2.AmazonLinuxVirt.HVM
            )

        
        # Create Load Balancer
        alb = cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self,
            "myAlbId",
            vpc=vpc,
            internet_facing=True,
            load_balancer_name="WebServerAlb"
        )
        
        
        # Allow ALB to recieve internet traffic.
        alb.connections.allow_from_any_ipv4(
            cdk.aws_ec2.Port.tcp(80), 
            description="Allow Internet access on ALB Port 80"
        )
        
        # Add listener to ALB instance.
        listener = alb.add_listener("listenerId",
                                    port=80,
                                    open=True)
        
        # Webserver IAM Role
        web_server_role = cdk.aws_iam.Role(
            self,
            "webServerRoleId",
            assumed_by=cdk.aws_iam.ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonSSMManagedInstanceCore"
                ),
                cdk.aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonS3ReadOnlyAccess"
                )
            ]
        )
        
        # WebServer Autoscaling Group
        self.web_server_asg = cdk.aws_autoscaling.AutoScalingGroup(
            self,
            "webServerAsgId",
            vpc=vpc,
            vpc_subnets=cdk.aws_ec2.SubnetSelection(
                subnet_type=cdk.aws_ec2.SubnetType.PRIVATE_WITH_EGRESS
            ),
            instance_type=cdk.aws_ec2.InstanceType(instance_type_identifier="t3.micro"),
            machine_image=amazn_linux_ami,
            role=web_server_role,
            min_capacity=2,
            max_capacity=2,
            user_data=cdk.aws_ec2.UserData.custom(data)
        )
        
        # Allow ASG SG receive traffic from ALB
        self.web_server_asg.connections.allow_from(alb, cdk.aws_ec2.Port.tcp(80), description="Allow ASG SG receive traffic from ALB")
        
        
        # Add ASG Group Instances to ALB target group.
        listener.add_targets("listenerId", port=80, targets=[self.web_server_asg])
        
        # O/P of the ALB domain name
        cdk.CfnOutput(self,
                      "albDomainNameOutput",
                      value=f"http://{alb.load_balancer_dns_name}",
                      export_name="WebServerALBDomainName"
                      )
