import logging
import logging.handlers
import os

def setup_logger(name="log", log_file="logs/etl_log.log", level=logging.INFO):
    """
    Sets up a logger with the specified name, log file, and logging level.
    
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level (int): Logging level, e.g., logging.INFO or logging.DEBUG.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    
    # prevent duplicate log entries if logger is already configured
    if logger.handlers:
        return logger

    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
