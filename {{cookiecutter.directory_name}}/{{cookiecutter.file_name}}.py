import logging
import sys
import time
import traceback

from argparse import Namespace
from configparser import ConfigParser, NoOptionError
from signal import signal, SIGINT

# custom imports
from cli import parse_arguments
from decorators import timer
from logger import setup_logging


def signal_handler(received_signal, frame):
    """Function to handle Ctrl-C and Keyboard interrupts
    
    Args:
        received_signal:
        frame: 
    """
    logging.info(f'SIGINT or CTRL-C detected. Exiting gracefully...')
    sys.exit(0)


def cleanup(start_time: float, message: str, error_code: int) -> None:
    """Function to perform cleanup activities

    Args:
        start_time (float): Start time of the script
        message (str): The error message to be logged
        error_code (int): The error code to be displayed
    """
    logging.error(message)
    elapsed_time = time.perf_counter() - start_time
    logging.debug(f'Time taken to run the script {__file__}: {elapsed_time:0.2f} seconds.')
    sys.exit(error_code)


def get_option(config: ConfigParser, section: str, option: str):
    """Function to get option value from config file
    
    Args:
        config (ConfigParser): the ConfigParser object that contains 
        section (str): name of the section
        option (str): name of the option under the section
    """
    # reading configuration options
    option_value = ''
    message = ''
    try:
        option_value = config.get(section=section, option=option)
    except NoOptionError as e:
        logging.error(f'Error reading option {option}. {e}')
    finally:
        return option_value, message

@timer
def do_something_fun(output_csv: str):
    logging.info(f'Writing output to {output_csv}')
    pass

def main(args: Namespace):
    """Main function"""
    # signal handling
    signal(SIGINT, signal_handler)

    start_time = time.perf_counter()
    logging.debug(f"--------------------------------------------------------")
    logging.debug(f"Script Execution Started.")

    # read configuration file
    config_file = args.config
    logging.info(f'Reading config file - {config_file}')
    config = ConfigParser()
    try:
        config.read_file(open(config_file))
    except FileNotFoundError as e:
        logging.error(f'Error reading config file. {e}')
        message = f'The file "{config_file}" was not found. Please create a new file in the current directory. Exiting...'
        cleanup(start_time, message, 1001)

    # reading configuration options
    option = 'Api-Keys' # 'option' is case insensitive
    api_key, message = get_option(config=config, section='api', option=option)
    if not api_key:
        message = f'The file {config_file} does not contain an option named {option}. Please Make sure the {config_file} file contains the line "{option}=abcd123". Exiting...'
        cleanup(start_time, message, 1002)

    # main logic
    try:
        do_something_fun(args.output_csv)
    except Exception as e:
        message = f'Error occurred - {e}'
        cleanup(start_time, message, 1003)

if __name__ == '__main__':
    setup_logging()
    args = parse_arguments()
    try:
        main(args)
    except Exception as e:
        logging.error(traceback.format_exc())