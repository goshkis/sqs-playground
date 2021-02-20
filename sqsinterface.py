import sys
import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()

sqs_resource = boto3.resource('sqs') # Your default boto config must allow access to SQS

class simpleSQSInterface():
    def __init__(self, queue_name):
        self.sqs = sqs_resource
        self.queue = self.get_queue(queue_name)
        
    def get_queue(self, name):
        """
        Get SQS queue by name

        :param name: the name that was used to create the queue
        :return: sqs queue object
        """
        try:
            queue = self.sqs.get_queue_by_name(QueueName=name)
            logger.info("Queue object inited: name='%s' URL='%s'", name, queue.url)
        except ClientError as error:
            logger.exception("Failed to get queue %s", name)
            raise error
        else:
            return queue

    def send_message(self, message_body, message_attributes=None):
        """
        Send a message to an Amazon SQS queue.

        :param message_body: The body text of the message.
        :param message_attributes: Custom attributes of the message. These are key-value
                                pairs that can be whatever you want.
        :return: The response from SQS that contains the assigned message ID.
        """
        if not message_attributes:
            message_attributes = {}

        try:
            response = self.queue.send_message(
                MessageBody=message_body,
                MessageAttributes=message_attributes
            )
        except ClientError as error:
            logger.exception("Send message failed: %s", message_body)
            raise error
        else:
            return response


    def receive_messages(self, max_number, wait_time):
        """
        Receive a batch of messages from an SQS queue.

        :param max_number: max number of messages to receive.
        :param wait_time: non-zero means long pooling.
        :return: list of Message objects received.
        """
        try:
            messages = self.queue.receive_messages(
                AttributeNames=['All'],
                MessageAttributeNames=['All'],
                MaxNumberOfMessages=max_number,
                WaitTimeSeconds=wait_time
            )
            for msg in messages:
                logger.info("Received message: %s: %s", msg.message_id, msg.body)
        except ClientError as error:
            logger.exception("Couldn't receive messages from queue: %s", self.queue)
            raise error
        else:
            return messages


    def delete_messages(self, messages):
        """
        Delete a batch of messages from a queue. Log but not fail on single messages.

        :param messages: list of messages to delete.
        :return: list of successful and failed message operations.
        """
        try:
            entries = [{'Id': str(ind), 'ReceiptHandle': msg.receipt_handle} for ind, msg in enumerate(messages)]
            response = self.queue.delete_messages(Entries=entries)
            if 'Successful' in response:
                for msg_meta in response['Successful']:
                    logger.info("Deleted message %s", messages[int(msg_meta['Id'])].message_id,)
            if 'Failed' in response:
                for msg_meta in response['Failed']:
                    logger.warning("Could not delete %s", messages[int(msg_meta['Id'])].message_id)
        except ClientError:
            logger.exception("Couldn't delete messages from queue %s", self.queue)
        else:
            return response
