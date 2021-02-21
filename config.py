""" Global config
"""

QUEUE_NAME = 'q1_standard'

# SQS queue parameters
VISIBILITY_TIMEOUT_S = 5  # One msg estimated processing time during normal operations (0.1) *
                          # BATCH_SIZE (10) * acceptable delay (5x from normal time - random for now)
MAX_MSG_SIZE_BYTES = 2048 # Value suitable for testing
RETENTION_PERIOD_S = 900  # Value suitable for testing

# SQS ReceiveMessage parameters.
BATCH_SIZE = 10   # Keep in mind visibility timeout and single msg processing time
MAX_WAIT_TIME = 2 # non-zero means long pool

# Extra logging for message reader
LOG_DATA = False

READER_THREADS = 3