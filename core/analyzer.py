import openpyxl
import pandas as pd


def analyze(data):
    rows = []

    for item in data:
        row = item.get('elements')[0]

        encumbrances = []
        for encumbrance in row.get('encumbrances'):
            if encumbrance.get('typeDesc') != None:
                encumbrances.append(encumbrance.get('typeDesc'))



        rows.append({
            'cadNumber': row.get('cadNumber'),
            'status': row.get('status'),
            'area': row.get('area'),
            'flat': row.get('address').get('apartment'),
            'encumbrances': ", ".join(encumbrances)
        })

    df = pd.DataFrame(rows)

    df.to_excel(r'./stats2.xlsx', index=False, header=True)

