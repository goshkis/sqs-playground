""" Global config
"""

QUEUE_NAME = 'q1_standard'

# SQS ReceiveMessage parameters.
BATCH_SIZE = 10
MAX_WAIT_TIME = 2

# Extra logging for message reader
LOG_DATA = False

READER_THREADS = 3