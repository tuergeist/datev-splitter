import os.path
import re
from enum import Enum
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


class FormNr(Enum):
    Abrechnung = 'LOGN15'
    AbrechnungswertePruefung = 'LOAP10'
    Begleitdaten = 'LOA104'  # Begleitzettel, Mandatendaten etc
    Lohnsteuerbescheinigung = 'LO4723'
    Meldebescheinigung = 'LOMS04'
    SVJahresarbeitsentgelt = 'LOJE11'
    Ueberweisungsprotokoll = 'LOA203'

    Unkown = 'UKNOWN'


def get_form_nr(text: str) -> FormNr:
    form = re.findall(r'AFP Form.-Nr. ([A-Z]{2}\w{4})', text)
    try:
        return FormNr(form[0])
    except IndexError:
        logger.error(f"No Form Nr found in text >>> '{text}' <<<")
    except ValueError:
        logger.error(f"Unknown Form Nr. '{form}'")
    return FormNr.Unkown


def get_name(prefix: str, old_pn: str, _text: str) -> str | None:
    text = _text.replace('ä', 'ae')
    form: FormNr = get_form_nr(text)

    match form:
        case FormNr.Abrechnung:
            title = re.findall('für ([A-Z]{1}[a-z]+) (20[0-9]{2})', text)
            suffix = "-".join(list(reversed(title[0])))
        case FormNr.Lohnsteuerbescheinigung:
            lst = re.findall('(Lohnsteuerbescheinigung) für ([0-9]{4})', text)
            suffix = "-".join(list(reversed(lst[0])))
        case FormNr.Meldebescheinigung:
            mb = re.findall('Meldebescheinigung', text)
            datum = re.findall(r'((0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(20[0-9]{2}))', text)
            suffix = mb[0] + "-" + datum[0][0]
        case _:
            return None
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
        file_name: str = "unknown_yet"
        for pdf_page in pdf_in:
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
                    file_name: str = "unknown_yet"
                logger.debug(f"reset start page to {page} for {pn}")
                start_page = page
                file_name = get_name(prefix, pn, text)

            old_pn = pn

        logger.debug('%s from %s to %s' % (file_name, start_page, page))
        mark_used(start_page, page + 1)
        if file_name:
            result.add((file_name, start_page, page))

        if export_pns:
            sorted_pns = sorted(pn_set)
            import csv
            with open(export_pns, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(sorted_pns)

        return result, ignored


def extract_pages(infile: str, dst_path: str, identify_set: set):
    skipped = []
    for entry in identify_set:
        name, start, end = entry
        logger.debug(f"Saving {name}")
        if name is None:
            logger.info(f"Skipping page {start} to {end} for a nameless file")
            skipped.append(entry)
        elif f"{INVALID_PN}-" in name:  # thats what the datev splitter adds for unknon PNs
            logger.info(f"Skip saving {name} from page {start} to {end} ")
            skipped.append(entry)
        else:
            save(infile, os.path.join(dst_path, name), start, end)
    return skipped
