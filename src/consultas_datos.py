"""Consultas y resúmenes para los datos limpios de cada entidad."""

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


def consultar_datasets(carpeta_proyecto):
    carpeta = Path(carpeta_proyecto).resolve() / "data" / "limpiar"
    archivos = {
        "Compradores": Path("compradores") / "compradores_limpios.csv",
        "Vendedores": Path("vendedores") / "vendedores_limpios.csv",
        "Administradores": Path("administradores") / "administradores_limpios.csv",
    }
    resultados = {}
    for entidad, nombre_archivo in archivos.items():
        ruta = carpeta / nombre_archivo
        if not ruta.is_file():
            raise FileNotFoundError(f"No se encontró el dataset limpio: {ruta}")
        datos = pd.read_csv(ruta)
        resultados[entidad] = datos
        print(f"\n{entidad}: {len(datos)} registros")
        if "status" in datos.columns:
            print("Estado:")
            print(datos["status"].value_counts(dropna=False).to_string())
        if "adminType" in datos.columns:
            print("Tipo:")
            print(datos["adminType"].value_counts(dropna=False).to_string())
        if "balance" in datos.columns:
            balance = pd.to_numeric(datos["balance"], errors="coerce")
            print(
                "Balance promedio: "
                f"${balance.mean():,.2f} COP; "
                f"mínimo: ${balance.min():,.2f}; "
                f"máximo: ${balance.max():,.2f}"
            )
        if "propiedad_de_interes" in datos.columns:
            print("Interés:")
            print(
                datos["propiedad_de_interes"]
                .value_counts(dropna=False)
                .to_string()
            )
    return resultados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Muestra resúmenes de los datasets limpios."
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=CARPETA_PROYECTO,
        help="Carpeta raíz del proyecto (opcional).",
    )
    argumentos = parser.parse_args()
    consultar_datasets(argumentos.project_dir)
