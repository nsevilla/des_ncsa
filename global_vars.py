import os
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s [%(name)-12s] %(levelname)-8s %(message)s',
)
log = logging.getLogger("desdm-public")
try:
    log.setLevel(os.environ['LOG_LEVEL'])
except:
    log.setLevel('WARNING')
