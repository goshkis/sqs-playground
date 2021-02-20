""" Queue-processor
"""

import random
import logging.config

import config

from datetime import datetime
from sqsinterface import simpleSQSInterface

logging.config.fileConfig('log.conf')
logger = logging.getLogger('reader')
logger.setLevel(logging.INFO)

data_logger = logging.getLogger('reader_data')

def message_handler(message):
    """
    Process event/message

    Give up on messages with ReceiveCount higher than MAX_PROCESS_ATTEMPTS

    :param message: Message object to process
    :return: boolean result of message processing
    """

    # TODO: Add unittests for expected attributes in SQS reply
    (sender_id, sent_ts, recv_count) = (message.attributes[x] for x in ('SenderId', 'SentTimestamp','ApproximateReceiveCount'))
     
    # import pdb;pdb.set_trace()
    logger.debug("ApproximateReceiveCount: '%s'", recv_count)
    if int(recv_count) > config.MAX_PROCESS_ATTEMPTS:
        # give up, emmit metric and send it to dead letter queue
        processing_result = "expire"
    else:
        # Processing here. Fail with some probability for fun
        try:
            if random.randint(0, 10) == 5:
                raise RuntimeError()
            processing_result = "pass"
        except RuntimeError: 
            processing_result = "fail" 

    # Logging message processing
    # miliseconds to match AWS timestamps
    utc_now = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()*1000)
    log_line = '{},{},{},{},{},{},"{}"'.format(utc_now, sent_ts, processing_result, recv_count,sender_id, message.message_id, message.body)
    data_logger.info(log_line)

    return False if processing_result == "fail" else True

def main():
    """ Main routine
    """

    queue = simpleSQSInterface(config.QUEUE_NAME)

    logger.info("Processing messages for queue %s, batch size = %s",
                config.QUEUE_NAME, config.BATCH_SIZE)

    while True:
        received_messages = queue.receive_messages(config.BATCH_SIZE, config.MAX_WAIT_TIME)
        processed_messages = []

        for message in received_messages:
            if message_handler(message):
                processed_messages.append(message)

        if processed_messages:
            queue.delete_messages(processed_messages)

        if len(received_messages) > 0:
            logger.info("Messages received/processed: %s/%s", len(received_messages), len(processed_messages))

if __name__ == "__main__":
    main()
