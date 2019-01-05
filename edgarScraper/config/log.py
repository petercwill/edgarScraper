import logging
import os


LOG_DIR = os.path.realpath(os.path.join(__file__, '../../../logs'))
LOGGING_LEVEL = logging.DEBUG

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
formatter2 = logging.Formatter('%(message)s')


def setup_logger(name, log_file, level, formatter=formatter):

    fh = logging.FileHandler(log_file, mode='w')        
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


# daily index logger
dailyIndLogger = setup_logger(
    'dailyIndLogger',
    os.path.join(LOG_DIR, 'dailyIndLogger.log'),
    LOGGING_LEVEL
    )

# second file logger
urlLogger = setup_logger(
    'urlLogger',
    os.path.join(LOG_DIR, 'urlLogger.log'),
    logging.INFO
    )

matchLogger = setup_logger(
    'matchLogger',
    os.path.join(LOG_DIR, 'matchLogger.log'),
    logging.DEBUG.INFO,
    logging.INFO
    )

rejectedMatchLogger = setup_logger(
    'rejectedMatchLogger',
    os.path.join(LOG_DIR, 'rejectedMatchLogger.log'),
    LOGGING_LEVEL,
    formatter2
    )

edgarScraperLog = setup_logger(
    'edgarScraperLog',
    os.path.join(LOG_DIR, 'edgarScraperLog.log'),
    LOGGING_LEVEL,
    formatter
    )
