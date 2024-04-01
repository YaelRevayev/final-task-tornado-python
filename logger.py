import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler('./logs/python_info.log'),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

error_logger = logging.getLogger('errors')
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(logging.FileHandler('./logs/python_error.log'))
 