import argparse
import sys
from typing import Optional

from loguru import logger

from datev_splitter.pdf_extract import identify_pages, extract_pages


def _arg_parser(args: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', metavar='infile', type=str,
                        help='Datev file to process')
    parser.add_argument('-q', '--quiet', action='store_true', help="Show only warnings and errors")
    parser.add_argument('-d', '--debug', action='store_true', help="Show more context")
    parser.add_argument('-t', '--trace', action='store_true', help="Show even more context / trace")
    parser.add_argument('-p', '--prefix', type=str, help="Prefix for all result files")
    parser.add_argument('-o', '--output', type=str, default='',
                        help="Where to write the output files (path must exist, defaults to .)")
    parser.add_argument('-e', '--exportpns', type=str, help='Export csv file with processed Personalnummern.')
    args = parser.parse_args(args)
    logger.debug(args)
    return args


def _setup_logger(args):
    level = "INFO"
    if args.trace:
        level = "TRACE"
    elif args.debug:
        level = "DEBUG"
    elif args.quiet:
        level = "WARN"
    logger.remove()
    logger.add(sys.stdout, colorize=True, level=level)


@logger.catch
def datev_split():
    args = _arg_parser()
    _setup_logger(args)

    result, ignored = identify_pages(args.infile, args.prefix, args.exportpns)
    extract_pages(args.infile, args.output, result)
    logger.info(f"Ignored pages: {ignored}")
