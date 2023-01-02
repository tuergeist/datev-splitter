from datev_splitter.pdf_extract import get_pn, INVALID_PN


def test_get_pn_invalid():
    text = "*Pers.-Nr. 0022*"
    assert get_pn(text) == INVALID_PN  # too short


def test_get_pn():
    text = "*Pers.-Nr. 00222*"
    assert get_pn(text) == "00222"

    text = """Abrechnung der Brutto/Netto-Bezüge für Dezember 2022
Personal-Nr.Freibetrag jährl.
Geburtsdatum StKl Faktor
Ki.Frbtr. Konfession
00222 010189 4
SV-Nummer
1
1 DBA
Freibetrag mtl.
MidijobSt.-Tg.
BGRSUm. SV-Tg.
20
124452/10101/222
22.12.2022 Blatt: 1
VJ Url. üb.Url. Anspr.Url.Tg.gen.Resturlaub
Anw. TageUrlaub TageKrankh. Tg.Fehlz. Tage
Anw. Std.Urlaub Std.Krankh. Std.Fehlz. Std.
30
KK % 8 PGRS
Krankenkasse
321321321 AOK Plus
1580101 1111 2 30
Eintritt
Austritt
011022
Steuer-ID
B/N
83I
*Pers.-Nr. 00213*
MFB 7
Zeitlohn Std. Überstd.
Bez. Std.
21221
Eine GmbH*St.-Martin-Str. 0*88888 München
Hinweise zur Abrechnung"""
    assert get_pn(text) == '00213'
