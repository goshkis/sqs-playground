""" Queue-processor
"""

import time
import random
import threading
import logging.config
from datetime import datetime
import config
from sqsinterface import simpleSQSInterface

logging.config.fileConfig('log.conf')
logger = logging.getLogger('reader')
logger.setLevel(logging.INFO)

data_logger = logging.getLogger('reader_data')

class SimpleMessageProcessor(simpleSQSInterface):
    """ Process messages with multiple threads
    """
    def __init__(self, queue_name, datalogger=None):
        super().__init__(queue_name)
        self.datalogger = datalogger if datalogger else logging.getLogger()

    def message_handler(self, message, extra_logging=False):
        """
        Process event/message

        :param message: Message object to process
        :param extra_logging: Enable all messages and metadata for detailed offline analysis.
        :param data_logger: pre-configured logging object
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
            (sender_id, sent_ts, recv_count) = (message.attributes[x] for x in ('SenderId',
                                                'SentTimestamp','ApproximateReceiveCount'))

            # miliseconds to match AWS timestamps
            utc_now = int((datetime.utcnow() - datetime(1970, 1, 1)).total_seconds()*1000)
            log_line = '{},{},{},{},{},{},"{}"'.format(utc_now, sent_ts, processing_result,
                            recv_count,sender_id, message.message_id, message.body)
            self.datalogger.info(log_line)

        return processing_result == "pass"

    def worker(self, arg):
        """
        Receive and process messages in a loop

        :param arg: signaling dict {'stop': False}. Exit once 'stop' flipped to True.
        :return: boolean result of message processing
        """
        while not arg['stop']:
            received_messages = self.receive_messages(max_number=config.BATCH_SIZE,
                                                    wait_time=config.MAX_WAIT_TIME)
            processed_messages = []

            for message in received_messages:
                if self.message_handler(message, extra_logging=config.LOG_DATA):
                    processed_messages.append(message)

            if processed_messages:
                self.delete_messages(processed_messages)

            if len(received_messages) > 0:
                logger.info("Messages received/processed: %s/%s", len(received_messages),
                            len(processed_messages))

    def run(self, num_threads):
        """ Run threads and start processing messages
        """
        exec_control = {'stop': False}
        threads = list()
        for index in range(num_threads):
            logger.info("Starting thread %d.", index)
            thread = threading.Thread(target=self.worker, args=(exec_control,))
            threads.append(thread)
            thread.start()

        while True:
            try:
                logger.info('heartbeat')
                time.sleep(5)
            except KeyboardInterrupt:
                exec_control['stop'] = True
                break

        for index, thread in enumerate(threads):
            thread.join()
            logger.info("Thread %d done", index)


def main():
    """ Main routine
    """

    sqs_reader = SimpleMessageProcessor(queue_name=config.QUEUE_NAME, datalogger=data_logger)

    logger.info("Processing messages for queue %s, batch size = %s",
                config.QUEUE_NAME, config.BATCH_SIZE)

    sqs_reader.run(config.READER_THREADS)


if __name__ == "__main__":
    main()
