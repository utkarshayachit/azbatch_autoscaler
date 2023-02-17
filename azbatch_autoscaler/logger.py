import logging

default_log_level = logging.INFO

def set_default_log_level(level):
    global default_log_level
    default_log_level = getattr(logging, level)

def get_logger(name):
    # create logger
    logger = logging.getLogger(f'azbatch_autoscaler.{name}')
    logger.setLevel(default_log_level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(default_log_level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger
