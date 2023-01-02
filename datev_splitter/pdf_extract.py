import os.path
import re
from typing import Optional

import fitz  # pip install PyMuPDF
from loguru import logger

PERSONAL_NR_PATTERN = r'Pers\.-Nr\. ([0-9]{5})'

INVALID_PN = 'X'


def get_pn(text):
    r = re.findall(PERSONAL_NR_PATTERN, text)
    if len(r) == 0:
        logger.trace(text)
        pn = INVALID_PN
    else:
        pn = r[0]
    return pn

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


def get_personal_name(text: str):
    splitted = text.split('\n')
    found = False
    for line in splitted:
        if re.findall(PERSONAL_NR_PATTERN, line):
            found = True
            continue
        if found:  # next line is the name
            logger.info(line)
            return line
    return


def identify_pages(infile: str, prefix: str = 'prefix', export_pns: Optional[str] = None):
    result = set()
    pn_set: set = set()

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
            file_name: str = "unknown_yet"
            page += 1
            logger.debug('--> Page %s --> ' % page)
            text = pdf_page.get_text()
            personal_name = get_personal_name(text)

            pn = get_pn(text)
            if pn != INVALID_PN:
                pn_set.add((f"{prefix}{pn}", pn, personal_name))

            if pn != old_pn:
                if old_pn != INVALID_PN:
                    logger.debug('%s from %s to %s' % (file_name, start_page, page - 1))
                    add_to_result(file_name, start_page, page)
                logger.debug(f"reset start page to {page} for {pn}")
                start_page = page
                file_name = get_name(prefix, pn, text)

            old_pn = pn

        logger.debug('%s from %s to %s' % (file_name, start_page, page))
        mark_used(start_page, page + 1)
        result.add((file_name, start_page, page))

        if export_pns:
            sorted_pns = sorted(pn_set)
            import csv
            with open(export_pns, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(sorted_pns)

        return result, ignored



def extract_pages(infile: str, dst_path: str, identify_set: set):
    for entry in identify_set:
        name, start, end = entry
        save(infile, os.path.join(dst_path, name), start, end)
