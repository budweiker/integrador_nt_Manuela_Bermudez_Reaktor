import argparse
import os
from pathlib import Path

import pandas as pd

if __package__:
    from .exportar_datos import exportar_csv
else:
    from exportar_datos import exportar_csv

CARPETA_PROYECTO = Path(
    os.environ.get(
        "PROYECTO_INTEGRADOR_DIR",
        Path(__file__).resolve().parents[1],
    )
).resolve()


def normalizar_correo(serie):
    correos = serie.astype("string").str.strip().str.lower()
    correos = correos.str.replace(r"\s+", "@", n=1, regex=True)
    correos = correos.str.replace(r"\s+", "", regex=True)
    valido = correos.str.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+")
    return correos.where(valido)


def normalizar_telefono(serie):
    telefonos = serie.astype("string").str.replace(r"\D", "", regex=True)
    telefonos = telefonos.str.replace(r"^57(?=\d{10}$)", "", regex=True)
    valido = telefonos.str.fullmatch(r"\d{7}|\d{10}|01800\d{7}")
    return telefonos.where(valido)


def normalizar_estado(serie):
    estados = serie.astype("string").str.strip().str.lower().map({
        "true": True,
        "1": True,
        "si": True,
        "sí": True,
        "false": False,
        "0": False,
        "no": False,
    })
    if estados.notna().any():
        return estados.fillna(estados.mode().iloc[0]).astype(bool)
    return pd.Series(False, index=serie.index, dtype=bool)


def limpiar_personas(datos):
    requeridas = {
        "user_id",
        "password",
        "nombre",
        "telefono",
        "correo",
        "status",
        "balance",
    }
    faltantes = requeridas.difference(datos.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas requeridas: {', '.join(sorted(faltantes))}.")

    limpio = datos.copy()
    for columna in limpio.select_dtypes(include=["object", "string"]).columns:
        limpio[columna] = limpio[columna].astype("string").str.strip()
        limpio[columna] = limpio[columna].replace("", pd.NA)

    limpio["user_id"] = limpio["user_id"].astype("string").str.strip()
    limpio["nombre"] = limpio["nombre"].astype("string").str.title()
    limpio["correo"] = normalizar_correo(limpio["correo"])
    limpio["telefono"] = normalizar_telefono(limpio["telefono"])
    limpio["status"] = normalizar_estado(limpio["status"])
    limpio["balance"] = pd.to_numeric(limpio["balance"], errors="coerce")

    columnas_obligatorias = [
        "user_id",
        "password",
        "nombre",
        "telefono",
        "correo",
        "balance",
    ]
    limpio = limpio.dropna(subset=columnas_obligatorias)
    limpio = limpio.drop_duplicates(subset="user_id", keep="first")

    if "propiedad_de_interes" in limpio.columns:
        limpio["propiedad_de_interes"] = (
            limpio["propiedad_de_interes"]
            .astype("string")
            .str.strip()
            .str.lower()
        )
        limpio["propiedad_de_interes"] = limpio[
            "propiedad_de_interes"
        ].replace("", pd.NA)
        limpio["propiedad_de_interes"] = limpio[
            "propiedad_de_interes"
        ].fillna("sin dato")

    if "propiedadesVendidas" in limpio.columns:
        limpio["propiedadesVendidas"] = pd.to_numeric(
            limpio["propiedadesVendidas"], errors="coerce"
        )
        limpio = limpio.dropna(subset=["propiedadesVendidas"])
        limpio["propiedadesVendidas"] = limpio[
            "propiedadesVendidas"
        ].astype(int)

    return limpio.reset_index(drop=True)


def limpiar_administradores(datos):
    requeridas = {"user_id", "adminType"}
    faltantes = requeridas.difference(datos.columns)
    if faltantes:
        raise ValueError(
            f"Faltan columnas requeridas en administradores: "
            f"{', '.join(sorted(faltantes))}."
        )
    limpio = datos.copy()
    limpio["user_id"] = limpio["user_id"].astype("string").str.strip()
    limpio["adminType"] = (
        limpio["adminType"].astype("string").str.strip().str.lower()
    )
    limpio["adminType"] = limpio["adminType"].where(
        limpio["adminType"].isin(("admin", "superadmin"))
    )
    limpio = limpio.dropna(subset=["user_id", "adminType"])
    limpio = limpio.drop_duplicates(subset="user_id", keep="first")
    limpio["adminType"] = limpio["adminType"].str.title()
    return limpio.reset_index(drop=True)


def limpiar_datasets(carpeta_proyecto):
    carpeta_proyecto = Path(carpeta_proyecto).resolve()
    carpeta_sucios = carpeta_proyecto / "data" / "sucios"
    carpeta_limpios = carpeta_proyecto / "data" / "limpios"

    tareas = (
        (
            "compradores",
            "compradores_sucios.csv",
            "compradores_limpios.csv",
            limpiar_personas,
        ),
        (
            "vendedores",
            "vendedores_sucios.csv",
            "vendedores_limpios.csv",
            limpiar_personas,
        ),
        (
            "administradores",
            "administradores_sucios.csv",
            "administradores_limpios.csv",
            limpiar_administradores,
        ),
    )
    resultados = {}
    for entidad, entrada, salida, funcion_limpiar in tareas:
        ruta_entrada = carpeta_sucios / entrada
        if not ruta_entrada.is_file():
            raise FileNotFoundError(f"No se encontró el archivo sucio: {ruta_entrada}")
        datos = pd.read_csv(ruta_entrada)
        datos_limpios = funcion_limpiar(datos)
        exportar_csv(datos_limpios, carpeta_limpios / salida)
        resultados[salida] = (len(datos), len(datos_limpios))

    return resultados


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Limpia los CSV sucios de compradores, vendedores y administradores."
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=CARPETA_PROYECTO,
        help="Carpeta raíz del proyecto (opcional).",
    )
    argumentos = parser.parse_args()
    for archivo, (entrada, salida) in limpiar_datasets(
        argumentos.project_dir
    ).items():
        print(f"{archivo}: {entrada} crudos -> {salida} limpios")
