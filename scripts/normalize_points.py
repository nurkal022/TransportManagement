#!/usr/bin/env python3
"""Нормализация названий точек маршрутов (Откуда / Куда).

Приводит start_point и end_point к единому написанию:
  * убирает лишние пробелы (в начале/конце и двойные внутри);
  * сливает варианты, отличающиеся только пробелами/регистром, к самому
    частому написанию (например «ЛРТ Жасулан » -> «ЛРТ Жасулан»).
Разные по смыслу названия («ЛРТ Жасулан» и «ЛРТ Жасулан кольцо») не трогает.

Идемпотентно: повторный запуск ничего не меняет. Маршруты не удаляются,
меняется только текст названий.

Использование: python scripts/normalize_points.py [path/to/transport.db]
"""
import sys, os, re, sqlite3
from collections import defaultdict

def clean(s):
    return re.sub(r'\s+', ' ', (s or '').strip())

def key(s):
    return clean(s).lower()

def main(db_path):
    if not os.path.exists(db_path):
        sys.exit(f"База не найдена: {db_path}")
    c = sqlite3.connect(db_path)
    cnt = lambda q, *a: c.execute(q, a).fetchone()[0]
    routes_before = cnt("SELECT COUNT(*) FROM route")

    # частота каждого написания по обеим колонкам
    freq = defaultdict(int)
    for col in ('start_point', 'end_point'):
        for v, n in c.execute(f"SELECT {col}, COUNT(*) FROM route GROUP BY {col}"):
            freq[v] += n
    # канон для каждой нормализованной группы = очищенное самое частое написание
    groups = defaultdict(list)
    for v in freq:
        groups[key(v)].append(v)
    canon = {}
    for k, variants in groups.items():
        best = max(variants, key=lambda v: freq[v])
        canon[k] = clean(best)

    changed = 0
    for rid, sp, ep in c.execute("SELECT id, start_point, end_point FROM route"):
        nsp = canon.get(key(sp), clean(sp))
        nep = canon.get(key(ep), clean(ep))
        if nsp != sp or nep != ep:
            c.execute("UPDATE route SET start_point=?, end_point=? WHERE id=?", (nsp, nep, rid))
            changed += 1

    routes_after = cnt("SELECT COUNT(*) FROM route")
    ok = c.execute("PRAGMA integrity_check").fetchone()[0]
    assert routes_after == routes_before, "число маршрутов изменилось!"
    assert ok == "ok", f"integrity: {ok}"
    c.commit()

    d_start = cnt("SELECT COUNT(DISTINCT start_point) FROM route")
    d_end = cnt("SELECT COUNT(DISTINCT end_point) FROM route")
    print(f"обновлено маршрутов: {changed}")
    print(f"уникальных точек теперь: откуда={d_start}, куда={d_end}")
    print("OK — нормализация применена (или уже была применена).")

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'instance/transport.db')
