import aws_cdk as cdk

# from resource_stacks.custom_vpc import CustomVpcStack

# from resource_stacks.custom_ec2 import CustomEc2Stack

# from resource_stacks.custom_ec2_with_latest_ami import CustomEc2LatestAmiStack

# from resource_stacks.custom_ec2_with_ebs_prov_iops import CustomEc2PiopsStack

# from app_stacks.vpc_stack import VpcStack

# from app_stacks.web_server_stack import WebServerStack

# from resource_stacks.custom_parameters_stack import CustomParametersSecretsStack

# from resource_stacks.custom_iam_users_groups import CustomIamUsersGroupsStack

# from resource_stacks.custom_iam_roles_policies import CustomRolesPoliciesStack

# from resource_stacks.custom_s3_resource_policy import CustomS3ResourcePolicyStack

from app_db_stack.vpc_3tier_stack import Vpc3TierStack

from app_db_stack.web_server_3tier_stack import WebServer3TierStack

from app_db_stack.rds_3tier_stack import RdsDatabase3TierStack

app = cdk.App()

env = cdk.Environment(account=app.node.try_get_context('envs')['prod']['account'], region=app.node.try_get_context('envs')['prod']['region'])

# CustomVpcStack(app, "my-custom-vpc-stack", env=env)

# CustomEc2Stack(app, "my-custom-ec2-stack", env=env)

# CustomEc2LatestAmiStack(app, "my-ec2-stack-with-latest-ami", env=env)

# CustomEc2PiopsStack(app, "my-ec2-stack-with-prov-iops", env=env)

# vpc_stack = VpcStack(app, "vpc-stack", env=env)

# WebServerStack(app, "webserver-stack-with-asg-elb", env=env, vpc=vpc_stack.vpc)

# CustomParametersSecretsStack(app, "my-ssm-params-stack", env=env)

# CustomIamUsersGroupsStack(app, "my-iam-users-groups-stack", env=env)

# CustomRolesPoliciesStack(app, "my-iam-roles-policies-stack", env=env)

# CustomS3ResourcePolicyStack(app, "custom-s3-resource-policies-stack", env=env)

vpc_3tier_stack = Vpc3TierStack(app, 
                                "multi-tier-app-vpc-stack", 
                                env=env)

app_3tier_stack = WebServer3TierStack(app, 
                                      "multi-tier-app-web-server-stack", 
                                      env=env, 
                                      vpc=vpc_3tier_stack.vpc)

db_3tier_stack = RdsDatabase3TierStack(app, 
                                       "multi-tier-app-db-stack", 
                                       env=env, 
                                       vpc=vpc_3tier_stack.vpc, 
                                       asg_security_groups=app_3tier_stack.web_server_asg.connections.security_groups)

cdk.Tags.of(app).add("Email", app.node.try_get_context('envs')['prod']['email'])

app.synth()
