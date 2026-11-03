import argparse
import os
from pathlib import Path

import pandas as pd

if __package__:
    from . import simular_Admin, simular_buyers, simular_sellers
else:
    import simular_Admin
    import simular_buyers
    import simular_sellers


def simular_datasets(carpeta_proyecto):
    carpeta_proyecto = Path(carpeta_proyecto).resolve()
    compradores_limpios = simular_buyers.generar_datos_limpios()
    vendedores_limpios = simular_sellers.generar_datos_limpios()
    usuarios = pd.concat(
        [
            compradores_limpios[["user_id"]].rename(columns={"user_id": "id"}),
            vendedores_limpios[["user_id"]].rename(columns={"user_id": "id"}),
        ],
        ignore_index=True,
    ).drop_duplicates(subset="id")

    simular_Admin.CARPETA_PROYECTO = carpeta_proyecto
    administradores = simular_Admin.generar_datos_limpios(
        df_user=usuarios
    )

    return {
        "compradores": compradores_limpios,
        "vendedores": vendedores_limpios,
        "administradores": administradores,
    }


if __name__ == "__main__":
    raiz_predeterminada = Path(
        os.environ.get(
            "PROYECTO_INTEGRADOR_DIR",
            Path(__file__).resolve().parents[1],
        )
    )
    parser = argparse.ArgumentParser(
        description="Simula datos crudos de compradores, vendedores y administradores."
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=raiz_predeterminada,
        help="Carpeta raíz del proyecto (opcional).",
    )
    argumentos = parser.parse_args()
    if __package__:
        from .exportar_datos import exportar_datasets
    else:
        from exportar_datos import exportar_datasets
    conjuntos = simular_datasets(argumentos.project_dir)
    rutas = exportar_datasets(conjuntos, argumentos.project_dir)
    for entidad, datos in conjuntos.items():
        print(f"{entidad.capitalize()}: {len(datos)} registros simulados.")
    print(f"Datos exportados en: {rutas}")
