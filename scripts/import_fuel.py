#!/usr/bin/env python3
"""Импорт выгрузки топливных карт в БД.
Использование: python scripts/import_fuel.py path/to/cards.xlsx
"""
import sys
import app

def main(path):
    with app.app.app_context():
        added, updated = app.import_fuel_xlsx(open(path, 'rb'))
        print(f"added={added} updated={updated} total={app.FuelTransaction.query.count()}")
        mapped = app.FuelCard.query.filter(app.FuelCard.vehicle_id.isnot(None)).count()
        print(f"cards={app.FuelCard.query.count()} mapped={mapped}")
        d = app._fuel_data(None, None)
        print(f"liters={d['totals']['liters']} amount={d['totals']['amount']} corr_r={d['corr_r']}")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'cards.xlsx')
