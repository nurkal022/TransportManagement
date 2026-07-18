#!/usr/bin/env python3
"""Миграция: сделать типы груза общими и синхронизировать данные.

Действия (идемпотентно — повторный запуск безопасен):
  1. Слить типы-дубли по названию (без учёта регистра/пробелов): оставить тип
     с наибольшим числом маршрутов, переназначить маршруты, удалить дубли.
  2. Удалить демо-типы (Мебель, Продукты, Электроника), если у них 0 маршрутов.

Ни один маршрут не остаётся без типа груза. Меняются только строки cargo_type
и ссылки route.cargo_type_id. Схема БД не меняется.

Использование:  python scripts/migrate_shared_cargo_types.py [path/to/transport.db]
По умолчанию: instance/transport.db
"""
import sys, os, sqlite3
from collections import defaultdict

DEMO_TO_REMOVE = ['Мебель', 'Продукты', 'Электроника']

def norm(s):
    return (s or '').strip().casefold()

def main(db_path):
    if not os.path.exists(db_path):
        sys.exit(f"База не найдена: {db_path}")
    c = sqlite3.connect(db_path)
    c.row_factory = sqlite3.Row
    cnt = lambda q, *a: c.execute(q, a).fetchone()[0]

    routes_before = cnt("SELECT COUNT(*) FROM route")
    null_before = cnt("SELECT COUNT(*) FROM route WHERE cargo_type_id IS NULL")
    types_before = cnt("SELECT COUNT(*) FROM cargo_type")
    print(f"BEFORE: routes={routes_before} cargo_types={types_before} null_cargo={null_before}")

    # 1) merge duplicates by normalized name
    groups = defaultdict(list)
    for r in c.execute("SELECT id, name FROM cargo_type"):
        groups[norm(r['name'])].append(r['id'])
    merged = 0
    for _, ids in groups.items():
        if len(ids) < 2:
            continue
        # keep the id with the most routes
        ids.sort(key=lambda i: cnt("SELECT COUNT(*) FROM route WHERE cargo_type_id=?", i),
                 reverse=True)
        keep = ids[0]
        for dup in ids[1:]:
            n = c.execute("UPDATE route SET cargo_type_id=? WHERE cargo_type_id=?",
                          (keep, dup)).rowcount
            c.execute("DELETE FROM cargo_type WHERE id=?", (dup,))
            merged += 1
            print(f"  merged #{dup} -> #{keep} ({n} routes remapped)")

    # 2) delete demo types with 0 routes
    for name in DEMO_TO_REMOVE:
        row = c.execute("SELECT id FROM cargo_type WHERE name=?", (name,)).fetchone()
        if not row:
            continue
        rc = cnt("SELECT COUNT(*) FROM route WHERE cargo_type_id=?", row['id'])
        if rc == 0:
            c.execute("DELETE FROM cargo_type WHERE id=?", (row['id'],))
            print(f"  deleted demo '{name}' (#{row['id']}, 0 routes)")
        else:
            print(f"  kept '{name}' (#{row['id']}) — has {rc} routes")

    # integrity checks before commit
    dangling = cnt("""SELECT COUNT(*) FROM route WHERE cargo_type_id IS NOT NULL
                      AND cargo_type_id NOT IN (SELECT id FROM cargo_type)""")
    routes_after = cnt("SELECT COUNT(*) FROM route")
    null_after = cnt("SELECT COUNT(*) FROM route WHERE cargo_type_id IS NULL")
    types_after = cnt("SELECT COUNT(*) FROM cargo_type")
    ok = c.execute("PRAGMA integrity_check").fetchone()[0]

    assert routes_after == routes_before, "число маршрутов изменилось!"
    assert null_after == null_before, "появились маршруты без типа груза!"
    assert dangling == 0, "битые ссылки на удалённые типы!"
    assert ok == "ok", f"integrity_check: {ok}"

    c.commit()
    print(f"AFTER:  routes={routes_after} cargo_types={types_after} "
          f"null_cargo={null_after} dangling={dangling} merged={merged}")
    print("OK — миграция применена (или уже была применена).")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'instance/transport.db')
