import logging

# Logger configuration
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

logger = logging.getLogger('analytics')

# States of dialogue with user
START, SEND_FILE, FILTERED_BY_NAME, FILTERED_BY_DATE, EXIT = range(5)
