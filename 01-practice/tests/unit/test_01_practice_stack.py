import aws_cdk as core
import aws_cdk.assertions as assertions

from 01_practice.01_practice_stack import 01PracticeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in 01_practice/01_practice_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = 01PracticeStack(app, "01-practice")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
