import os
import sys
from pathlib import Path

# Asegurar que la carpeta raíz (donde está manage.py) está en sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto.settings")

import django
django.setup()

from django.db import connection


def main():
    sql = """
        SELECT c.nombre AS comuna, i.nombre, i.descripcion
        FROM portal_inmueble AS i
        JOIN portal_comuna   AS c ON c.id = i.comuna_id
        ORDER BY c.nombre ASC, i.nombre ASC;
    """
    with connection.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    lines = []
    current_comuna = None
    for comuna, nombre, descripcion in rows:
        if comuna != current_comuna:
            if current_comuna is not None:
                lines.append("")
            lines.append(f"=== COMUNA: {comuna} ===")
            current_comuna = comuna
        lines.append(f"- {nombre}\n  {descripcion}")

    if not rows:
        lines.append("No hay inmuebles.")

    # Guardar en portal/exports/
    output_file = BASE_DIR / "portal" / "exports" / "inmuebles_por_comuna.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")

    print(f"OK -> {output_file}")


if __name__ == "__main__":
    main()
