# finanzbericht

## install

```
git clone https://github.com/Eigenbaukombinat/finanzbericht.git
cd finanzbericht
python3 -m venv .
bin/pip install -r requirements.txt
```

## prepare

You have to have exports of all buchungen for all years since 2017 in the directory, named like `buchungen_YYYY.csv`.

Get them from collmex by clicking on "Buchungen anzeigen", put the year into the "Geschäftsjahr" Field and click the "Exportieren" button.

## use

```
bin/python finanzbericht.py
```
