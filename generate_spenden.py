import csv
import decimal
from num2words import num2words
from jinja2 import Template

with open('Vorlage_Sammelbestätigung.xml') as xmlfile:
    template = Template(xmlfile.read())

for gesyear in ('2019', '2020', '2021', '2022'):

    with open(f'spenden_{gesyear}.csv', newline='', encoding='latin1') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        mems = {}
        for row in spamreader:
            if row[0] == 'Name_Anschrift':
                continue
            ansch, z1, z2, z3, z4, z5, z6, betrag, datum, buchung = row
            if ansch not in mems:
                mems[ansch] = dict(total=0, total_w='', lines=[], anschrift=ansch.split(','))
            betrag_dot = betrag.replace(',', '.')
            mems[ansch]['total'] += decimal.Decimal(betrag_dot)
            mems[ansch]['total_w'] = num2words(mems[ansch]['total'], lang='de', to='currency')
            mems[ansch]['lines'].append(dict(date=datum, betrag=betrag_dot, line_id=len(mems[ansch]['lines'])+1))


    for mem_id, mem in mems.items():
        mem['zeitraum_start'] = mem['lines'][0]['date']
        mem['zeitraum_ende'] = mem['lines'][-1]['date']

        result = (template.render(mem=mem))
        with open(f'output_{gesyear}/{mem["anschrift"][0]}.xml', 'w') as outf:
            outf.write(result)

