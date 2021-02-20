""" Global config
"""

QUEUE_NAME = 'q1_standard'

# Worker message receive parameters.
BATCH_SIZE = 10
MAX_WAIT_TIME = 2
MAX_PROCESS_ATTEMPTS = 10

# Extra logging for message reader
LOG_DATA = True