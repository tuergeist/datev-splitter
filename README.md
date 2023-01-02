# Datev Lohnbescheinigung Splitter

Datev Lohnabrechnungen beinhalten immer alle Lohnbescheinigungen und Meldebescheinigungen für alle Mitarbeitenden.
Um diese automatisiert nach Personalnummer in einzelne pdf splitten zu können, gibt es dieses script.

## Erwarteter Input

Datev Datei (pdf) mit Entgeltabrechnungen, Lohnbescheinigungen und/oder Meldebescheinigungen zur Sozialversicherung.

## Ergebnis

Einzelne pdf Dateien, die jeweils die Informationen für zu einer einzelnen Personalnummer enthalten. Im Original
zusammenhängende Seiten zu einer Personalnummer werden auch zusammen exportiert.

## Benutzung

```bash
usage: datev_splitr [-h] [-q] [-d] [-t] [-p PREFIX] [-o OUTPUT] [-e EXPORT_PNS] infile

positional arguments:
  infile                Datev file to process

options:
  -h, --help            show this help message and exit
  -q, --quiet           Show only warnings and errors
  -d, --debug           Show more context
  -t, --trace           Show even more context / trace
  -p PREFIX, --prefix PREFIX
                        Prefix for all result files
  -o OUTPUT, --output OUTPUT
                        Where to write the output files (path must exist)
  -e EXPORT_PNS, --export-pns EXPORT_PNS
                        Export csv file with processed Personalnummern.
```

### Beispiel

`datev_splitr -p PREFIX- -o tmp -d auswertungen.pdf`

oder in der Entwicklungsumgebung

`pdm run python pdf_extract.py -p PREFIX- -o tmp -d auswertungen.pdf`

Erstellt im Unterordner `tmp` alle Dateien mit dem prefix `PREFIX-`.
D.h. Die Dateien heißen dann bspw.: `PREFIX-00203-2022-Dezember.pdf` für eine Lohnabrechnung Dezember 2022, 
Personalnummer `00203`

`-e pns.csv` Exportiert die Personalnummern mit und ohne Prefix und den gefundenen Namen.
Mit dem Prefix `RD-` sieht das Ergebnis bspw so aus:

```csv
RD-00004,00004,vorname name
RD-00006,00006,vorname2 name2
RD-00014,00014,vorname3 name3
```

## Welche Seiten werden exportiert?

- Praktisch alle auf denen eine Personalnummer zu finden ist

![Lohnabrechnungen](/docs/datev-abrechnung.png)
![Lohnsteuerbescheinigungnen](/docs/datev-lohnsteuerbescheinigung.png)
![Meldebescheinigungen](/docs/datev-meldebescheinigung.png)