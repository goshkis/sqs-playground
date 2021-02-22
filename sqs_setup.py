"""
SQS setup script.
Creates standard queue and associated dead-letter queue.
"""

import sys
import boto3
from botocore.exceptions import ClientError
import config

sqs_resource = boto3.resource('sqs') # Your default boto config must allow access to SQS

def setup_queue():

    print("Setting-up DLQ: {}_dlq".format(config.QUEUE_NAME))
    try:
        dlq_queue = sqs_resource.create_queue(QueueName="{}_dlq".format(config.QUEUE_NAME))
    except ClientError as err:
        # import pdb;pdb.set_trace()
        print("FATAL: can't create required queue(s): {}".format(err.response['Error']['Message']))
        sys.exit(1)

    redrive_policy = '{{"deadLetterTargetArn":"{}","maxReceiveCount":5}}'.format(dlq_queue.attributes['QueueArn'])
    
    attribs={
        'VisibilityTimeout': str(config.VISIBILITY_TIMEOUT_S),
        'MaximumMessageSize': str(config.MAX_MSG_SIZE_BYTES),
        'MessageRetentionPeriod': str(config.RETENTION_PERIOD_S),
        'RedrivePolicy': redrive_policy
    }
    
    print("Setting-up main queue: {}".format(config.QUEUE_NAME))
    try:
        dlq_queue = sqs_resource.create_queue(QueueName="{}".format(config.QUEUE_NAME), Attributes=attribs)
    except ClientError as err:
        print("FATAL: can't create required queue(s): {}".format(err.response['Error']['Message']))
        sys.exit(2)

def main():
    # instead of listing all queues and potentially dealing with paging let's just test it
    try:
        queue = sqs_resource.get_queue_by_name(QueueName=config.QUEUE_NAME)
        print("Main test queue found: {}".format(queue.url))

    except ClientError as err:
        print("Code:{}".format(err.response['Error']['Code']))
        setup_queue()

    print("DONE setting up the queues")

if __name__ == "__main__":
    main()