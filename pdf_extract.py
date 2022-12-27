import os.path
import re
import sys

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


infile = sys.argv[2]
prefix = sys.argv[1]


def save(infile: str, name: str, start_page: int, end_page: int):
    pages = list(range(start_page - 1, end_page))
    with fitz.open(infile) as pdf:
        pdf.select(pages)
        logger.info(f"Saving {name} with pages {pages}")
        pdf.save(name, garbage=3, deflate=True)


def identify_pages(infile: str, prefix: str = 'prefix'):
    result = set()
    with fitz.open(infile) as pdf_in:
        page: int = 0
        old_pn: str = INVALID_PN
        start_page: int = 1
        company: str = None
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
                    result.add((name, start_page, page - 1))

                start_page = page
                name = get_name(prefix, pn, text)
            old_pn = pn
        logger.debug('%s from %s to %s' % (name, start_page, page))
        result.add((name, start_page, page))
        return result


def extract_pages(infile: str, dst_path: str, identify_set: set):
    for entry in identify_set:
        name, start, end = entry
        save(infile, os.path.join(dst_path, name), start, end)


dst_path = 'tmp'
result = identify_pages(infile, prefix)
extract_pages(infile, dst_path, result)
