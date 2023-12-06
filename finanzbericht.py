#coding:utf8
import csv
import decimal

I = 'ideell'
W = 'wirtsch.'
Z = 'zweck'
V = 'verschiedene Bereiche'

import locale
locale.setlocale( locale.LC_ALL, '' )


def num(val):
    return locale.currency(val, grouping=True).replace('Eu','')

# name, bereich, bilanz2016

_KST = dict(
    ANST=('Förderprojekt Anstiftung 2019', I, 0),
    SIEB=('Siebdruck', Z, 0),
    EUG=('Essen und Getränke', W, 3338.25),
    KERAMIK=('Keramik', Z, 0),
    AV=('Audio/Video', Z, 0),
    GARTEN=('Garten', Z, 0),
    FOTO=('Foto', Z, 206.9),
    HND=('Handarbeit', Z, 618.99),
    HEY=('Hey, Alter!', I, 0),
    VR=('VR', Z, 0),
    HOLZ=('Holzwerkstatt Verbrauch', Z, 927.31),
    HOLZS=('Holzwerkstatt Verbrauch', Z, 0),
    CNC=('Holz-CNC', Z, 742.28),
    ELS=('Elektronik-Sortiment', W, 306.48),
    METAL=('Metall', Z, 25.61),
    BIKE=('Fahrrad', Z, 0),
    SOLAR=('Förderprojekt Solaranlage', I, 0),
    LASER=('Laser', Z, 0),
    DROSOS2023=('Drosos-Förderung 2023', I, 0),
    HOLZMAT=('Holz Material', W, 147.6),
    HCK=('Hackspace', I, 210.47+205.66+42.28+61.34)) #alt: hackspace+laser+plotter+modellbau
_KST[''] = ('ohne Kostenstelle', V, 0)

def kstinfo(kst):
    name, bereich, _ = _KST[kst]
    return f"{name}"

_E = 'Einnahmen'
_A = 'Ausgaben'

_KNTN = {
    '4400': ('Ausgaben', _A, W),
    '4210': ('Miete', _A, I),
    '4240': ('Gas, Strom, Wasser', _A, I),
    '4360': ('Versicherungen', _A, I),
    '4380': ('Beiträge',_A, I),
    '4390': ('sonstige Abgaben',_A ,I),
    '4401': ('Ausgaben',_A, Z),
    '4909': ('Fremdleistungen',_A, I),
    '4925': ('Telefax und Internetkosten',_A, I),
    '4950': ('Rechts- und Beratungskosten', _A, I),
    '4969': ('Abfallbeseitigung',_A, I),
    '4970': ('Kosten des Geldverkehrs',_A, I),
    '8000': ('Einnahmen',_E, Z),
    '8200': ('Einnahmen', _E, I),
    '2700': ('Einnahmen', _E, W),
    '4945': ('Fortbildungskosten', _A, I),
    '4600': ('Werbekosten', _A, I),
    '2300': ('Ausgaben', _A, I),
    '4930': ('Bürobedarf', _A, I),
    '4138': ('Beiträge zur Berufsgenossenschaft', _A, I),
    '8195': ('Erlöse als Kleinunternehmer', _E, I),
    '2400': ('Forderungsverluste', _E, I),
    '4000': ('Material- und Stoffverbrauch', _A, I),
    '3100': ('Fremdleistungen', _A, I),
    '4910': ('Porto', _A, I),
    '4900': ('Sonstige betriebliche Aufwendungen', _A, I),
    '4960': ('Mieten fuer Einrichtungen', _A, Z),
    '4980': ('Betriebsbedarf', _A, I),
    '4660': ('Reisekosten Arbeitnehmer', _A, I),
    '4100': ('Löhne und Gehälter', _A, I),
    '2380': ('Spenden', _A, I),
    '4260': ('Instandhaltung betrieblicher Räume', _A, I),
    '1840': ('Zuwendungen, Spenden', _E, I),
    '2100': ('Zinsen und ähnliche Aufwendungen', _A, I),
    }


def kontoinfo(konto):
    name, einaus, bereich = _KNTN[konto]
    kontoname = einaus + " für " + name if einaus not in name else name
    return f"{kontoname}"

def kontobereich(konto):
    _, _, bereich = _KNTN[konto]
    return bereich

all_konten = []

kassenstaende = {}

kassenstaende['2016'] = {}

for kst in _KST.keys():
    kassenstaende['2016'][kst] = decimal.Decimal(_KST[kst][2])

import pprint
pprint.pprint(kassenstaende)

for yearfn in ('2017', '2018', '2019', '2020', '2021', '2022', '2023'):
    kassenstaende_jahr = kassenstaende[yearfn] = {}
    for kst in _KST.keys():
        kassenstaende_jahr[kst] = kassenstaende[str(int(yearfn)-1)][kst]

    with open(f'buchungen_{yearfn}.csv', newline='', encoding='latin1') as csvfile:
        print(f"# {yearfn}")
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        buchungen = []
        buchungen_keys = []
        einnahmen = {}
        ausgaben = {}
        einnahmen_kto = {}
        ausgaben_kto = {}
        einnahmen_b = {}
        ausgaben_b = {}

        gesamt_einnahmen = 0
        gesamt_ausgaben = 0
        for row in spamreader:
            if row[0] == 'Firma':
                buchungen_keys = row
                continue
            soll_haben = row[9]
            jahr = row[1]
            konto = row[7]
            betrag_raw = row[10]
            kst = row[18]
            konto_name = row[8]
            betrag_dot = betrag_raw.replace(',', '.')

            if konto in ('1000', '1200', '1360', '1400', '1600', '1604'):
                # geldtransit-konten bzw. verbindlichkeiten und forderungen
                # das sind nur die von uns verwendeten konten!!
                continue

            all_konten.append(konto)

            betrag = decimal.Decimal(betrag_dot)

            bereich = kontobereich(konto)

            if soll_haben == 'Soll':
                gesamt_ausgaben += betrag
                if kst not in ausgaben:
                    ausgaben[kst] = 0
                if konto not in ausgaben_kto:
                    ausgaben_kto[konto] = 0
                if bereich not in ausgaben_b:
                    ausgaben_b[bereich] = 0
                ausgaben[kst] += betrag
                ausgaben_kto[konto] += betrag
                ausgaben_b[bereich] += betrag
                kassenstaende_jahr[kst] += -betrag



            elif soll_haben == 'Haben':
                gesamt_einnahmen += -betrag
                if kst not in einnahmen:
                    einnahmen[kst] = 0
                if konto not in einnahmen_kto:
                    einnahmen_kto[konto] = 0
                if bereich not in einnahmen_b:
                    einnahmen_b[bereich] = 0
                einnahmen[kst] += -betrag
                einnahmen_kto[konto] += -betrag
                einnahmen_b[bereich] += -betrag
                kassenstaende_jahr[kst] += -betrag

            #print(konto, konto_name, betrag, soll_haben,kst)

        #if int(yearfn) not in (2019, 2020, 2021):
        #    continue

        erlös = gesamt_einnahmen - gesamt_ausgaben
        print("")
        print ("## nach Kostenstelle")
        print("")
        print("| Kostenstelle | Einnahmen | Ausgaben | Ergebnis | Kassenstand |")
        print("|:--------------|-----------:|----------:|----------:|--:|")
        for kst in _KST.keys():
            ein = einnahmen.get(kst,0)
            aus = ausgaben.get(kst,0)
            print(f"| {kstinfo(kst) or 'keine Kostenstelle'} | {num(ein)} | {num(aus)} | {num(ein-aus)} | {num(kassenstaende_jahr[kst])}")
        print("")
        print ("## nach Konto")
        print("")
        print("| Konto |Bereich       | Einnahmen | Ausgaben | Ergebnis |")
        print("|:-------|:--------------|-----------:|-----------:|----------:|")
        for konto in sorted(set(einnahmen_kto.keys()).union(set(ausgaben_kto.keys())), key=kontoinfo):
            ein = einnahmen_kto.get(konto,0)
            aus = ausgaben_kto.get(konto,0)
            print(f"| {kontoinfo(konto)} | {kontobereich(konto)} | {num(ein)} | {num(aus)} | {num(ein-aus)} |")
        print("")
        print ("## nach Bereich")
        print("")
        print("| Bereich       | Einnahmen | Ausgaben | Ergebnis |")
        print("|:--------------|-----------:|-----------:|----------:|")
        for bereich in sorted(set(einnahmen_b.keys()).union(set(ausgaben_b.keys()))):
            ein = einnahmen_b.get(bereich,0)
            aus = ausgaben_b.get(bereich,0)
            print(f"| {bereich} | {num(ein)} |{num(aus)}|{num(ein-aus)}|")
        print("")
        print("## Gesamt")
        print("")
        print("|Gesamteinnahmen| Gesamtausgaben| Gesamtergebnis|")
        print("|--:|--:|--:|")
        print(f"|{num(gesamt_einnahmen)}|{num(gesamt_ausgaben)}|{num(erlös)}|")
        print()
        print()
        print()

