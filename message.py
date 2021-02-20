""" Queue-writer
    Handlers for /message REST calls. See server.py and swagger spec.
    No logging here, in favor of logging within SQS interface.
"""

from botocore.exceptions import ClientError
from flask import make_response, abort
from sqsinterface import simpleSQSInterface

import config

queue = simpleSQSInterface(config.QUEUE_NAME)

def create(message):
    """
    Send new message to the queue
    Passthrough 400, 415 and 429 errors from SQS client, and mask the rest with 500.
    Catch all exceptions, don't die but log\issue metric to be used in addition
    to metric for 500s. 

    :param message: object containing message to enqueue
    :return:        201 on success, 400 on message body parameter missed,
                    500 on all service-side errors
    """
    msg = message.get("body", None)

    if not msg:
        abort(400, "body parameter is missing or empty")

    try:
        #retry logic is controlled by boto3
        queue.send_message(message_body=msg)
    except ClientError as err:
        ret_code = int(err.response['Error']['Code'])
        # import pdb;pdb.set_trace()
        if ret_code in (400, 415, 429):
            abort(ret_code, err.response['Error']['Message'])
        # Hiding the rest
        abort(500, "Failed to enqueue message")
    except:
        # print("Unexpected error:", sys.exc_info()[0])
        abort(500, "Failed to enqueue message")

    return make_response({"status":"Ok", "message":"Message enqueued"}, 201)
