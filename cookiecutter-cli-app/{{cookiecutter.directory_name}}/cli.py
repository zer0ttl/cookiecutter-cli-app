from argparse import ArgumentParser, Namespace


def parse_arguments() -> Namespace:
    """Function to parse command line arguments"""
    parser = ArgumentParser(
        description='some description about the program/script',
        usage='%(prog)s <command> [options]'
    )

    # Positional Arguments: required or optional piece of information that a script/program uses to perform its intended action
    # username
    parser.add_argument(
        'name',
        type=str,
        help='user name'
    )

    # Positional Arguments with default values. nargs is required (https://stackoverflow.com/a/60796254)
    # output csv
    parser.add_argument(
        'output_csv',
        help='the output csv where information will be written',
        default='output.csv',
        nargs='?' # '?': a single value, which can be optional 
    )

    # config file
    config_file = '.env'
    parser.add_argument(
        'config',
        help=f'the config file in ini format. default: {config_file}',
        default=config_file,
        nargs='?'
    )

    # Optional Arguments: argument that modifies the script/program's behavior
    # version
    parser.add_argument(
        # -v is usually used for verbose
        '--version',
        action='version',
        version='%(prog)s 0.1'
    )
    return parser.parse_args()