#coding:utf8
import csv
import decimal

for yearfn in ('2019', '2020', '2021', '2022'):
    with open(f'buchungen_{yearfn}.csv', newline='', encoding='latin1') as csvfile:
        print(f"# {yearfn}")
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        buchungen = []
        buchungen_keys = []
        einnahmen = {}
        ausgaben = {}
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
            betrag_dot = betrag_raw.replace(',', '.')
            if konto in ('1000', '1200', '1360', '1400', '1600'):
                # geldtransit-konten bzw. verbindlichkeiten und forderungen
                continue

            konto_name = row[8]

            betrag = decimal.Decimal(betrag_dot)
            kst = row[18]

            if soll_haben == 'Soll':
                gesamt_ausgaben += betrag
                if kst not in ausgaben:
                    ausgaben[kst] = 0
                ausgaben[kst] += betrag

            elif soll_haben == 'Haben':
                gesamt_einnahmen += -betrag
                if kst not in einnahmen:
                    einnahmen[kst] = 0
                einnahmen[kst] += -betrag

            #print(konto, konto_name, betrag, soll_haben,kst)


        erlös = gesamt_einnahmen - gesamt_ausgaben
        import pprint

        for kst in set(einnahmen.keys()).union(set(ausgaben.keys())):
            ein = einnahmen.get(kst,0)
            aus = ausgaben.get(kst,0)
            print(f"* {kst or 'Keine Kostenstelle'}: {ein-aus} ")
            print(f"  * Einnahmen: {ein}")
            print(f"  * Ausgaben: {aus}")
        print("========================")
        print(f"Gesamteinnahmen: {gesamt_einnahmen}")
        print(f"Gesamtausgaben: {gesamt_ausgaben}")
        print()
        print(f"Erlös: {erlös}")
        print(f"Rücklagen erlaubt: {erlös*decimal.Decimal('0.333333333')}")
        print()
        print()
