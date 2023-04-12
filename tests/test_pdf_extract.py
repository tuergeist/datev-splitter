import re

import pytest

from datev_splitter.pdf_extract import get_pn, INVALID_PN, get_name, FormNr


def test_get_pn_invalid():
    text = "*Pers.-Nr. 0022*"
    assert get_pn(text) == INVALID_PN  # too short


def test_get_pn():
    text = "*Pers.-Nr. 00222*"
    assert get_pn(text) == "00222"


def test_get_pn_2022_12(text_2022_12):
    assert get_pn(text_2022_12) == '00213'


def test_name_2022_12(text_2022_12):
    name = get_name("RD", "00000", text_2022_12)
    assert name == "RD00000-2022-Dezember.pdf"


def test_name_2023_03_umlaut(text_2023_03):
    name = get_name("", "", text_2023_03)
    assert name == "-2023-Maerz.pdf"


def test_form_nr():
    melde: str = 'LOMS04'
    form = FormNr(melde)
    assert form == FormNr.Meldebescheinigung

    with pytest.raises(ValueError):
        FormNr('foobar')


def test_afp_form_nr():
    text = '''Dezember 2022
AFP Form.-Nr. LOGN15
Personal-Nr.Freibetrag ja'''
    res = re.findall('AFP Form.-Nr. ([A-Z]{2}\w{4})', text)
    assert res
    assert res[0] == 'LOGN15'


def test_meldedatum():
    text = """124444/10000/00011
                                                                             17.03.2023
                                                                                      1
                                                 00001         17.03.2023 / 12:38
                                                 12345696S565
"""
    datum = re.findall('((0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(20[0-9]{2}))', text)
    assert datum == [('17.03.2023', '17', '03', '2023'), ('17.03.2023', '17', '03', '2023')]
    assert datum[0][0] == '17.03.2023'
