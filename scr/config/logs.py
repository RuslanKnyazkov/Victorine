import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
logger_handler = logging.FileHandler(f'{__name__}.log')
logger_format = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

logger_handler.setFormatter(logger_format)
logger.addHandler(logger_handler)

logger.info(msg=f'Log file {__name__}')