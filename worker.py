""" Queue-processor
"""

import time
import random
import threading
import logging.config

import config

from datetime import datetime
from sqsinterface import simpleSQSInterface

logging.config.fileConfig('log.conf')
logger = logging.getLogger('reader')
logger.setLevel(logging.INFO)

data_logger = logging.getLogger('reader_data')

def message_handler(message, extra_logging=False):
    """
    Process event/message

    Log all messages and metadata for detailed offline analysis.

    :param message: Message object to process
    :return: boolean result of message processing
    """
    
    # Processing here. Fail with some probability for fun
    try:
        if random.randint(0, 10) == 5:
            raise RuntimeError()
        processing_result = "pass"
    except RuntimeError: 
        processing_result = "fail" 

    if extra_logging:
        # TODO: Add unittests for expected attributes in SQS reply
        (sender_id, sent_ts, recv_count) = (message.attributes[x] for x in ('SenderId', 'SentTimestamp','ApproximateReceiveCount'))

        # miliseconds to match AWS timestamps
        utc_now = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()*1000)
        log_line = '{},{},{},{},{},{},"{}"'.format(utc_now, sent_ts, processing_result,
                        recv_count,sender_id, message.message_id, message.body)
        data_logger.info(log_line)

    return False if processing_result == "fail" else True

def worker(queue, arg):
    """ 
    """
    while not arg['stop']:
        received_messages = queue.receive_messages(config.BATCH_SIZE, config.MAX_WAIT_TIME)
        processed_messages = []

        for message in received_messages:
            if message_handler(message, extra_logging=config.LOG_DATA):
                processed_messages.append(message)

        if processed_messages:
            queue.delete_messages(processed_messages)

        if len(received_messages) > 0:
            logger.info("Messages received/processed: %s/%s", len(received_messages), len(processed_messages))

def main():
    """ Main routine
    """

    queue = simpleSQSInterface(config.QUEUE_NAME)

    logger.info("Processing messages for queue %s, batch size = %s",
                config.QUEUE_NAME, config.BATCH_SIZE)

    info = {'stop': False}

    threads = list()
    for index in range(config.READER_THREADS):
        logger.info("Starting thread %d.", index)
        thread = threading.Thread(target=worker, args=(queue,info,))
        threads.append(thread)
        thread.start()

    while True:
        try:
            logger.info('heartbeat')
            time.sleep(5)
        except KeyboardInterrupt:
            info['stop'] = True
            break

    for index, thread in enumerate(threads):
        thread.join()
        logger.info("Thread %d done", index)

if __name__ == "__main__":
    main()
