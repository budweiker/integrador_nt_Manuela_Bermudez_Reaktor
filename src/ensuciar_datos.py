import argparse
import os
from pathlib import Path

import pandas as pd

from .simulaciones import simular_Admin

if __package__:
    from . import simular_buyers, simular_sellers
    from .exportar_datos import exportar_csv
else:
    import simulaciones.simular_Admin as simular_Admin
    import simular_buyers
    import simular_sellers
    from exportar_datos import exportar_csv

CARPETA_PROYECTO = Path(
    os.environ.get(
        "PROYECTO_INTEGRADOR_DIR",
        Path(__file__).resolve().parents[1],
    )
).resolve()
FUNCIONES_ENSUCIAR = {
    "compradores": simular_buyers.ensuciar,
    "vendedores": simular_sellers.ensuciar,
    "administradores": simular_Admin.ensuciar,
}
ARCHIVOS_POR_ENTIDAD = {
    "compradores": "compradores.csv",
    "vendedores": "vendedores.csv",
    "administradores": "administradores.csv",
}


def ensuciar_datasets(carpeta_proyecto):
    carpeta_proyecto = Path(carpeta_proyecto).resolve()
    carpeta_exportar = carpeta_proyecto / "data" / "exportar"
    carpeta_ensuciar = carpeta_proyecto / "data" / "ensuciar"
    resultados = {}

    for entidad, nombre_archivo in ARCHIVOS_POR_ENTIDAD.items():
        origen = carpeta_exportar / entidad / nombre_archivo
        if not origen.is_file():
            raise FileNotFoundError(
                f"No se encontró el archivo exportado de {entidad}: {origen}"
            )
        datos = pd.read_csv(
            origen,
            dtype={"user_id": "string", "telefono": "string"},
        )
        sucios = FUNCIONES_ENSUCIAR[entidad](datos)
        destino = carpeta_ensuciar / entidad / f"{entidad}_sucios.csv"
        exportar_csv(sucios, destino)
        resultados[entidad] = (len(datos), len(sucios), destino)

    return resultados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ensucia los datasets exportados por entidad."
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=CARPETA_PROYECTO,
        help="Carpeta raíz del proyecto (opcional).",
    )
    argumentos = parser.parse_args()
    for entidad, (originales, sucios, destino) in ensuciar_datasets(
        argumentos.project_dir
    ).items():
        print(
            f"{entidad.capitalize()}: {originales} exportados -> "
            f"{sucios} sucios ({destino})"
        )
