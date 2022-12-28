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
usage: pdf_extract.py [-h] [-q] [-d] [-t] [-p PREFIX] [-o OUTPUT] [-e EXPORT_PNS] infile

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

`pdm run python pdf_extract.py -p PREFIX- -o tmp -d auswertungen.pdf`

Erstellt im Unterordner `tmp` alle Dateien mit dem prefix `PREFIX-`.
D.h. Die Dateien heißen dann bspw.: `PREFIX-00203-2022-Dezember.pdf` für eine Lohnabrechnung Dezember 2022, 
Personalnummer `00203`
