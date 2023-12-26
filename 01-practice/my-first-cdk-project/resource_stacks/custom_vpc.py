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

        cdk.Tags.of(custom_vpc).add("Owner", self.node.try_get_context('envs')['prod']['admin'])
        # cdk.Tag("Owner", "Sid")

        cdk.CfnOutput(self,
                      "customVpcIdOutput",
                      value=custom_vpc.vpc_id,
                      export_name="customVpcId"
                      )

        my_bkt = cdk.aws_s3.Bucket(self, "customBktId")
        cdk.Tags.of(my_bkt).add("Admin", "Siddharth")

        # Resource in same account
        bkt1 = cdk.aws_s3.Bucket.from_bucket_name(
            self,
            "MyImportedBucket",
            "www.thelaughingbuddha.store"
        )

        bkt2 = cdk.aws_s3.Bucket.from_bucket_arn(
            self,
            "crossAccountBucket",
            "arn:aws:s3:::terraform-aws-eks-0"
        )

        cdk.CfnOutput(
            self,
            "myImportedBucketOutput",
            value=bkt1.bucket_name,
            export_name="myImportedBucket"
        )

        cdk.CfnOutput(
            self,
            "myCrossBucketOutput",
            value=bkt2.bucket_arn,
            export_name="myCrossBucket"
        )

        vpc2 = cdk.aws_ec2.Vpc.from_lookup(
            self,
            "importedVpc2",
            is_default=True
        )

        cdk.CfnOutput(
            self,
            "importedVpc2Output",
            value=vpc2.vpc_id,
            export_name="myImportedVpc2"
        )

        cdk.aws_ec2.CfnVPCPeeringConnection(
            self,
            "peerVpc12",
            peer_vpc_id=custom_vpc.vpc_id,
            vpc_id=vpc2.vpc_id
        )
