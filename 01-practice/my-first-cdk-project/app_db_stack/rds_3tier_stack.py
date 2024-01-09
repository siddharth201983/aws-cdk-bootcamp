import aws_cdk as cdk
from constructs import Construct
import json

class RdsDatabase3TierStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc, asg_security_groups, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Create an RDS Database        
        my_3tier_db = cdk.aws_rds.DatabaseInstance(
            self,
            "myRdsDatabase",
            credentials=cdk.aws_rds.Credentials.from_generated_secret("Dbadmin"),
            database_name="myRdsDatabase",
            engine=cdk.aws_rds.DatabaseInstanceEngine.MYSQL,
            vpc=vpc,
            port=3306,
            allocated_storage=30,
            multi_az=False,
            cloudwatch_logs_exports=["audit", "error", "general", "slowquery"],
            instance_type=cdk.aws_ec2.InstanceType.of(
                cdk.aws_ec2.InstanceClass.BURSTABLE2,
                cdk.aws_ec2.InstanceSize.MICRO
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            deletion_protection=False,
            delete_automated_backups=True,
            backup_retention=cdk.Duration.days(1)
            )
        
        for sg in asg_security_groups:
            my_3tier_db.connections.allow_default_port_from(sg, "Allow EC2 ASG access to RDS MySQL")
        
        cdk.CfnOutput(self, 
                  "db_endpoint",
                  value = my_3tier_db.db_instance_endpoint_address)
        
        cdk.CfnOutput(self,
                    "DbConnectionCommand",
                    value=f"mysql -h {my_3tier_db.db_instance_endpoint_address} -P 3306 -u mystiquemaster -p",
                    description="Connect to the database using this command"
                    )
        