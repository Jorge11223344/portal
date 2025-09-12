import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto.settings")

import django
django.setup()

from django.db import connection


def main():
    sql = """
        SELECT r.nombre AS region, i.nombre, i.descripcion
        FROM portal_inmueble AS i
        JOIN portal_comuna   AS c ON c.id = i.comuna_id
        JOIN portal_region   AS r ON r.id = c.region_id
        ORDER BY r.nombre ASC, i.nombre ASC;
    """
    with connection.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    lines = []
    current_region = None
    for region, nombre, descripcion in rows:
        if region != current_region:
            if current_region is not None:
                lines.append("")
            lines.append(f"=== REGIÓN: {region} ===")
            current_region = region
        lines.append(f"- {nombre}\n  {descripcion}")

    if not rows:
        lines.append("No hay inmuebles.")

    output_file = BASE_DIR / "portal" / "exports" / "inmuebles_por_region.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")

    print(f"OK -> {output_file}")


if __name__ == "__main__":
    main()
