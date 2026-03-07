import logging
import os

LOG_DIR = "logs"

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=f"{LOG_DIR}/ai_system.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_logger(name):
    return logging.getLogger(name)