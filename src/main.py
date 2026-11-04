import argparse
import os
from pathlib import Path

if __package__:
    from .consultas_datos import consultar_datasets
    from .ensuciar_datos import ensuciar_datasets
    from .exportar_datos import exportar_datasets
    from .limpiar_datos import limpiar_datasets
    from .reporte_datos import generar_reportes
    from .simular_datos import simular_datasets
else:
    from consultas_datos import consultar_datasets
    from ensuciar_datos import ensuciar_datasets
    from exportar_datos import exportar_datasets
    from limpiar_datos import limpiar_datasets
    from reporte_datos import generar_reportes
    from simular_datos import simular_datasets


def ejecutar_pipeline(carpeta_proyecto):
    carpeta_proyecto = Path(carpeta_proyecto).resolve()

    print("Etapa 1/6: simulando compradores, vendedores y administradores...")
    cantidades = simular_datasets(carpeta_proyecto)
    for entidad, cantidad in cantidades.items():
        print(f"  {entidad.capitalize()}: {len(cantidad)} registros simulados.")

    print("Etapa 2/6: exportando los CSV por entidad...")
    archivos_exportados = exportar_datasets(cantidades, carpeta_proyecto)
    print(f"  {len(archivos_exportados)} datasets exportados.")

    print("Etapa 3/6: ensuciando los datos exportados...")
    resultados_sucios = ensuciar_datasets(carpeta_proyecto)
    for entidad, (originales, sucios, _) in resultados_sucios.items():
        print(f"  {entidad}: {originales} exportados -> {sucios} sucios.")

    print("Etapa 4/6: limpiando los datasets...")
    resultados = limpiar_datasets(carpeta_proyecto)
    for archivo, (cantidad_cruda, cantidad_limpia) in resultados.items():
        print(
            f"  {archivo}: {cantidad_cruda} crudos -> "
            f"{cantidad_limpia} limpios."
        )

    print("Etapa 5/6: consultando los datos limpios...")
    consultar_datasets(carpeta_proyecto)

    print("Etapa 6/6: generando gráficos por entidad...")
    generar_reportes(carpeta_proyecto)
    print("Proceso completo. Los datos de propiedades no fueron modificados.")


if __name__ == "__main__":
    raiz_predeterminada = Path(
        os.environ.get(
            "PROYECTO_INTEGRADOR_DIR",
            Path(__file__).resolve().parents[1],
        )
    )
    parser = argparse.ArgumentParser(
        description=(
            "Ejecuta el pipeline completo de compradores, vendedores y "
            "administradores. No procesa propiedades."
        )
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=raiz_predeterminada,
        help="Carpeta raíz del proyecto (opcional).",
    )
    argumentos = parser.parse_args()
    ejecutar_pipeline(argumentos.project_dir)
