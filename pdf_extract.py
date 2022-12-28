import argparse
import os.path
import re
import sys
from typing import Optional

import fitz  # pip install PyMuPDF
from loguru import logger

INVALID_PN = 'X'


def get_name(prefix: str, old_pn: str, text: str) -> str:
    suffix = ""
    lst = re.findall('(Lohnsteuerbescheinigung) für ([0-9]{4})', text)
    title = re.findall('für ([A-Z]{1}[a-z]+) (20[0-9]{2})', text)
    mb = re.findall('Meldebescheinigung', text)
    if len(title) > 0:
        suffix = "-".join(list(reversed(title[0])))
    elif len(lst) > 0:
        suffix = "-".join(list(reversed(lst[0])))
    elif len(mb) > 0:
        suffix = mb[0]
    return f'{prefix}{old_pn}-{suffix}.pdf'


def save(infile: str, name: str, start_page: int, end_page: int):
    pages = list(range(start_page - 1, end_page))
    with fitz.open(infile) as pdf:
        pdf.select(pages)
        logger.info(f"Saving {name} with pages {pages}")
        pdf.save(name, garbage=3, deflate=True)


def identify_pages(infile: str, prefix: str = 'prefix', export_pns: Optional[str] = None):
    result = set()

    def add_to_result(name, start_page, page):
        mark_used(start_page, page)
        result.add((name, start_page, page - 1))

    def mark_used(start, stop):
        for p in range(start, stop):
            logger.debug('mark page %s as used' % p)
            ignored.remove(p)

    with fitz.open(infile) as pdf_in:
        page: int = 0
        old_pn: str = INVALID_PN
        start_page: int = 1
        ignored = set(range(1, pdf_in.page_count + 1))
        logger.debug(pdf_in.metadata)
        for pdf_page in pdf_in:
            page += 1
            logger.debug('--> Page %s --> ' % page)
            text = pdf_page.get_text()
            r = re.findall('Pers\.-Nr\. ([0-9]{5})', text)
            if len(r) == 0:
                logger.trace(text)
                pn = INVALID_PN
            else:
                pn = r[0]

            if pn != old_pn:
                if old_pn != INVALID_PN:
                    logger.debug('%s from %s to %s' % (name, start_page, page - 1))
                    add_to_result(name, start_page, page)
                logger.debug(f"reset start page to {page} for {pn}")
                start_page = page
                name = get_name(prefix, pn, text)
            old_pn = pn
        logger.debug('%s from %s to %s' % (name, start_page, page))
        mark_used(start_page, page + 1)
        result.add((name, start_page, page))
        return result, ignored


def extract_pages(infile: str, dst_path: str, identify_set: set):
    for entry in identify_set:
        name, start, end = entry
        save(infile, os.path.join(dst_path, name), start, end)


def _arg_parser(args: Optional[list] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', metavar='infile', type=str,
                        help='Datev file to process')
    parser.add_argument('-q', '--quiet', action='store_true', help="Show only warnings and errors")
    parser.add_argument('-d', '--debug', action='store_true', help="Show more context")
    parser.add_argument('-t', '--trace', action='store_true', help="Show even more context / trace")
    parser.add_argument('-p', '--prefix', type=str, help="Prefix for all result files")
    parser.add_argument('-o', '--output', type=str, default='',
                        help="Where to write the output files (path must exist)")
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
def main():
    args = _arg_parser()
    _setup_logger(args)

    result, ignored = identify_pages(args.infile, args.prefix, args.exportpns)
    extract_pages(args.infile, args.output, result)
    logger.info(f"Ignored pages: {ignored}")


if __name__ == '__main__':
    main()
