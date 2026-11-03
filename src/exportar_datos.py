import argparse
import os
from pathlib import Path

import pandas as pd

CARPETA_PROYECTO = Path(
    os.environ.get(
        "PROYECTO_INTEGRADOR_DIR",
        Path(__file__).resolve().parents[1],
    )
).resolve()
ARCHIVOS_POR_ENTIDAD = {
    "compradores": "compradores.csv",
    "vendedores": "vendedores.csv",
    "administradores": "administradores.csv",
}


def exportar_csv(datos, ruta):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    datos.to_csv(ruta, index=False, encoding="utf-8-sig")
    return ruta


def exportar_datasets(datos_por_entidad, carpeta_proyecto=None):
    carpeta_proyecto = Path(carpeta_proyecto or CARPETA_PROYECTO).resolve()
    carpeta_crudos = carpeta_proyecto / "data" / "crudos"
    rutas = {}
    for entidad, nombre_archivo in ARCHIVOS_POR_ENTIDAD.items():
        if entidad not in datos_por_entidad:
            raise ValueError(f"No se recibieron datos para {entidad}.")
        destino = carpeta_crudos / nombre_archivo
        rutas[entidad] = exportar_csv(datos_por_entidad[entidad], destino)
    return rutas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Simula y exporta los datos Faker iniciales por entidad. "
            "Para ejecutar el flujo completo, usa main.py."
        )
    )
    parser.add_argument("--project-dir", type=Path, default=CARPETA_PROYECTO)
    argumentos = parser.parse_args()
    if __package__:
        from .simular_datos import simular_datasets
    else:
        from simular_datos import simular_datasets
    datasets = simular_datasets(argumentos.project_dir)
    for entidad, ruta in exportar_datasets(
        datasets,
        argumentos.project_dir,
    ).items():
        print(f"{entidad.capitalize()} exportados en: {ruta}")
