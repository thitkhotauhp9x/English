import logging
import threading
import time

from fastapi import FastAPI

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG
)


logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/search")
def root():
    logger.debug("%r", "Creating ...")
    thread_count = threading.active_count()
    logger.debug("threads=%r", thread_count)
    time.sleep(2)
    logger.debug("%r", "Done")
    return {}
