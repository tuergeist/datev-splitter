import pytest

@pytest.fixture
def text_2022_12():
    return """Abrechnung der Brutto/Netto-Bezüge für Dezember 2022
AFP Form.-Nr. LOGN15
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
124444/10101/222
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
Eine GmbH*St.-Claus-Str. 0*88888 München
Hinweise zur Abrechnung"""


@pytest.fixture
def text_2023_03():
    return """Abrechnung der Brutto/Netto-Bezüge
AFP Form.-Nr. LOGN15
Personal-Nr.
Geburtsdatum
StKl
Konfession
Ki.Frbtr.
Freibetrag jährl.
Freibetrag mtl.
Midijob
Anw. Std.
Urlaub Std.
Krankh. Std.
Fehlz. Std.
1
1
SV-Nummer
PGRS
BGRS
Eintritt
Austritt
Anw. Tage
Urlaub Tage
Krankh. Tg.
Fehlz. Tage
VJ Url. üb.
Url. Anspr.
Url.Tg.gen.
Resturlaub
Zeitlohn Std.
Überstd.
Hinweise zur Abrechnung
Brutto-Bezüge
Betrag
Lohnart
Bezeichnung
Einheit
Menge
Faktor 3 Prozentsatz
St
SV GB
4
4
5
Gesamt-Brutto
Steuerrechtliche Abzüge
Netto-Verdienst
Betrag
Auszahlungsbetrag
SV-rechtliche Abzüge
Steuer/Sozialversicherung
Netto-Bezüge/Netto-Abzüge
St
Steuer-Brutto
Lohnsteuer
Kirchensteuer
Solidaritätszuschlag
St4
SV4
KV-Brutto
RV-Brutto
AV-Brutto
PV-Brutto
KV-Beitrag
RV-Beitrag
AV-Beitrag
PV-Beitrag6
SV-Brutto
KV-Beitrag
RV-Beitrag
AV-Beitrag
PV-Beitrag
VWL gesamt
Kug-Auszahlung



Nr.
Bezeichnung
SV-AG-Anteil
Gesamtkosten
Zus. AG-Kosten
Bank
Konto
Verdienstbescheinigung
Gesamt-Brutto
Steuer-Brutto
Lohnsteuer
Kirchensteuer
Solidaritätszuschlag
Steuerfreie Bezüge
P. verst. Zuk.sich.

Pfändung Rest
Darlehen Rest
Blatt:
Faktor
DBA
St.-Tg.
Um. SV-Tg.
Bez. Std.
3
2
1
2

3

H = Hinzurechnungsbetrag
Std = Stunden, T = Tage, Km = Kilometer, St = Stück
EUR = Euro, Tsd = Tausend Euro, Mio = Million Euro
Gegebenenfalls Netto-Lohn/Netto-Stundenlohn 

L = Laufender Bezug, S = Sonstiger Bezug, F = Frei,
E = Einmalbezug, P = Pauschalierung, A = Abfindung,
M = mehrjährige Versteuerung, N = Nachberechnung
V = Vorjahr, W = Entgeltguthaben 

5
6
7
8 


J = Bestandteil des Gesamt-Bruttos
Z = Einschl. Beitragszuschlag zur PV für Kinderlose
MFB = Mehrfachbeschäftigung
Maßgeblicher Beitragssatz zur KV inkl. Zusatzbeitrag  


4




Steuer-ID
MFB
- Dies ist eine Entgeltbescheinigung nach § 108 Abs. 3 Satz 1 der Gewerbeordnung -
7
Krankenkasse
KK % 8
Eine & Keine GmbH*St.-Susi-Str. 4*88888 München
                                                B/N
*Pers.-Nr. 00004*                              HOJ
Klaus Dieter
Erich-Maier-Str. 7
01523 Ortschaft
                                                               HMA/HOJ  124444/12345/4
                              für März 2023                          17.03.2023      1
00004 210679 4                                            30
22220799D033 AOK Plus                      1610101 1111 2 30
                                               010111

"""
