import logging, sys

def configure_logging():
    handler = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(fmt)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.handlers = [handler]
