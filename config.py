""" Global config
"""

QUEUE_NAME = 'q1_standard'

# SQS queue parameters
VISIBILITY_TIMEOUT_S = 15
MAX_MSG_SIZE_BYTES = 2048
RETENTION_PERIOD_S = 900

# SQS ReceiveMessage parameters.
BATCH_SIZE = 10
MAX_WAIT_TIME = 2 # non-zero means long pool

# Extra logging for message reader
LOG_DATA = False

READER_THREADS = 3