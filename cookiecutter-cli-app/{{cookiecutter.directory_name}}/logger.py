import logging
import logging.config
import sys
import time
import yaml
from pathlib import Path
from datetime import datetime


class UTCFormatter(logging.Formatter):
    """Format logging asctime to UTC"""
    converter = time.gmtime


def setup_log_dirs():
    """Creates logging directories and log files.

    Returns:
        file_log (Path): The Path object for the log file generated on every run of the script.
        file_rotating_log (Path): The Path object for the rotating log file. 
    """
    dir_logs = Path.cwd().joinpath('logs') # Log directory name
    if not dir_logs.exists():
        Path.mkdir(Path.cwd().joinpath('logs'))
    fmt_date = datetime.utcnow().strftime('%Y%m%d-%H%M%SZ')
    file_log = Path.cwd().joinpath(dir_logs, fmt_date + ".log") # Single Log file name
    file_rotating_log = Path.cwd().joinpath(dir_logs, "debug.log") # Rotating Log file name
    return file_log, file_rotating_log

def setup_logging():
    """Configures logging using settings from the yaml config file."""
    file_log, file_rotating_log = setup_log_dirs()
    file_log_config = Path.cwd().joinpath('logger.yaml') # Log configuration file
    if not file_log_config.exists():
        sys.exit(1)
    with open(file_log_config, 'rt') as file:
        config_log = yaml.safe_load(file.read())
        config_log['handlers']['rotatingFileHandler']['filename'] = file_rotating_log # Doing this because I cannot find a way to input python code into yaml.
        config_log['handlers']['singleFileHandler']['filename'] = file_log
        logging.config.dictConfig(config_log)
    return None