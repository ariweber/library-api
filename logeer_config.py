import logging


logging.basicConfig(
    level="INFO",
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)
