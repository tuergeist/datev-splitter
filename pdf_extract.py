import re

import fitz  # pip install PyMuPDF

def get_company(text: str) -> str:
    if re.findall('ExB Labs GmbH', text):
        return 'Labs'
    else:
        return 'RD'


INVALID_PN = 'X'


def get_name(company: str, old_pn: str, text: str) -> str:
    prefix = ""
    lst = re.findall('(Lohnsteuerbescheinigung) für ([0-9]{4})', text)
    title = re.findall('für ([A-Z]{1}[a-z]+) (20[0-9]{2})', text)
    mb = re.findall('Meldebescheinigung', text)
    if len(title) > 0:
        prefix = "-".join(list(reversed(title[0])))
    elif len(lst) > 0:
        prefix = "-".join(list(reversed(lst[0])))
    elif len(mb) > 0:
        prefix = mb[0]
    return f'{company}-{old_pn}-{prefix}.pdf'

infile = 'labs.pdf'

def save(infile, name, start, end):
    with fitz.open(infile) as pdf:
        pdf.select(list(range(start-1,end )))
        pdf.save(name)

with fitz.open(infile) as pdf_in:
    page: int = 0
    old_pn: str = INVALID_PN
    start_page: int = 1
    company: str = None
    for pdf_page in pdf_in:
        page += 1
        print('---------------------------------------- %s' % page)
        text = pdf_page.get_text()
        if not company:
            company = get_company(text)
        # print(text)
        r = re.findall('Pers\.-Nr\. ([0-9]{5})', text)

        # print(r, title, lst)
        if len(r) == 0:
            # print(text)
            pn = INVALID_PN
        else:
            pn = r[0]
        print(pn)
        if pn != old_pn:
            if old_pn != INVALID_PN:
                # save
                # name = get_name(company, old_pn, title, lst)
                print('save %s from %s to %s' % (name, start_page, page - 1))
                save(infile, name, start_page, page - 1)

            start_page = page
            name = get_name(company, pn, text)
            # print("calc name", name)

        old_pn = pn
    print('save %s from %s to %s' % (name, start_page, page))
    save(infile, name, start_page, page)
