"""Generación de gráficos separados para compradores, vendedores y admins."""

import argparse
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CARPETA_PROYECTO = Path(
    os.environ.get(
        "PROYECTO_INTEGRADOR_DIR",
        Path(__file__).resolve().parents[1],
    )
).resolve()
CARPETA_LIMPIOS = CARPETA_PROYECTO / "data" / "limpios"
CARPETA_REPORTES = CARPETA_PROYECTO / "data" / "reportes"


def leer_datos(nombre_archivo):
    ruta = CARPETA_LIMPIOS / nombre_archivo
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo requerido: {ruta}")
    return pd.read_csv(ruta)


def leer_entidad(entidad):
    nombre_archivo = f"{entidad}_limpios.csv"
    ruta = CARPETA_LIMPIOS / nombre_archivo
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo limpio requerido: {ruta}")
    return pd.read_csv(ruta)


def normalizar_estado(datos):
    valores = datos.astype("string").str.strip().str.lower()
    estados = valores.map({
        "true": "Activo",
        "si": "Activo",
        "1": "Activo",
        "false": "Inactivo",
        "no": "Inactivo",
        "0": "Inactivo",
    })
    return estados.fillna("Sin dato")


def graficar_balances(datos, entidad, color):
    if "balance" not in datos.columns:
        raise ValueError(f"Falta la columna 'balance' en los datos de {entidad}.")
    if datos.empty:
        raise ValueError(f"No hay registros para graficar en {entidad}.")

    balances = pd.to_numeric(datos["balance"], errors="coerce").dropna()
    if balances.empty:
        raise ValueError(f"No hay balances numéricos para graficar en {entidad}.")

    balances_millones = balances.to_numpy(dtype=float) / 1_000_000
    minimo = float(balances_millones.min())
    maximo = float(balances_millones.max())
    amplitud = maximo - minimo
    paso = max(50, np.ceil(amplitud / 10 / 50) * 50)
    inicio = np.floor(minimo / paso) * paso
    fin = np.floor(maximo / paso) * paso + paso
    bordes = np.arange(inicio, fin + paso, paso)
    conteos, _ = np.histogram(balances_millones, bins=bordes)
    posiciones = np.arange(len(conteos))
    etiquetas_rango = [
        f"${desde:.0f}–${hasta:.0f}"
        for desde, hasta in zip(bordes[:-1], bordes[1:])
    ]

    fig, ax = plt.subplots(figsize=(11, 6))
    barras = ax.bar(posiciones, conteos, color=color, width=0.72)
    ax.set_xticks(posiciones, etiquetas_rango, rotation=35, ha="right")
    ax.set_title(f"Personas por rango de balance — {entidad} (N={len(balances)})")
    ax.set_xlabel("Rango de balance (millones de COP)")
    ax.set_ylabel("Cantidad de personas")
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.bar_label(barras, padding=2, fontsize=9)
    if len(balances) != len(datos):
        ax.text(
            1,
            1.01,
            f"Excluidos por balance no numérico: {len(datos) - len(balances)}",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=9,
        )
    fig.tight_layout()
    fig.savefig(CARPETA_REPORTES / entidad / "balance.png", dpi=160)
    plt.close(fig)
    return int(conteos.sum())


def graficar_estados(datos, entidad, color):
    estados_posibles = ("Activo", "Inactivo", "Sin dato")
    if "status" not in datos.columns:
        raise ValueError(f"Falta la columna 'status' en los datos de {entidad}.")
    if datos.empty:
        raise ValueError(f"No hay registros para graficar en {entidad}.")

    conteos = normalizar_estado(datos["status"]).value_counts().reindex(
        estados_posibles, fill_value=0
    ).astype(int)
    estados = tuple(estado for estado in estados_posibles if conteos[estado] > 0)
    conteos = conteos.reindex(estados)
    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar(estados, conteos, color=color, width=0.6)
    ax.set_title(f"Estado de las cuentas — {entidad} (N={len(datos)})")
    ax.set_ylabel("Cantidad de personas")
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.bar_label(barras, padding=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(CARPETA_REPORTES / entidad / "estado_cuentas.png", dpi=160)
    plt.close(fig)
    return int(conteos.sum())


def graficar_ventas_vendedor(vendedores):
    columna = "propiedadesVendidas"
    if columna not in vendedores.columns:
        raise ValueError(f"Falta la columna '{columna}' en los datos de vendedores.")
    if vendedores.empty:
        raise ValueError("No hay vendedores para graficar.")

    ventas = pd.to_numeric(vendedores[columna], errors="coerce").dropna()
    if ventas.empty:
        raise ValueError("No hay cantidades de propiedades vendidas para graficar.")
    conteos = ventas.astype(int).value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(9, 5))
    barras = ax.bar(
        conteos.index.astype(str),
        conteos.values,
        color="#f97316",
        width=0.7,
    )
    ax.set_title(f"Propiedades vendidas por vendedor (N={len(ventas)})")
    ax.set_xlabel("Cantidad de propiedades vendidas")
    ax.set_ylabel("Cantidad de vendedores")
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.bar_label(barras, padding=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(
        CARPETA_REPORTES / "vendedores" / "propiedades_vendidas.png",
        dpi=160,
    )
    plt.close(fig)
    return int(conteos.sum())


def graficar_intereses(compradores):
    if "propiedad_de_interes" not in compradores.columns:
        raise ValueError("Falta la columna 'propiedad_de_interes' en los datos de compradores.")
    if compradores.empty:
        raise ValueError("No hay compradores para graficar.")
    intereses_datos = compradores["propiedad_de_interes"].astype("string").str.strip()
    intereses_datos = intereses_datos.mask(intereses_datos.eq(""), "Sin dato").fillna("Sin dato")
    intereses = intereses_datos.value_counts().sort_values()
    if intereses.empty:
        raise ValueError("No hay intereses de compra para graficar.")

    fig, ax = plt.subplots(figsize=(9, 5))
    intereses.plot.barh(ax=ax, color="#14b8a6")
    ax.set_title(f"Tipo de propiedad de interés (N={len(compradores)} compradores)")
    ax.set_xlabel("Cantidad de compradores")
    ax.set_ylabel("")
    ax.grid(axis="x", alpha=0.2)
    ax.set_axisbelow(True)
    ax.bar_label(ax.containers[0], padding=3, fontsize=9)
    fig.tight_layout()
    fig.savefig(CARPETA_REPORTES / "compradores" / "intereses.png", dpi=160)
    plt.close(fig)
    return int(intereses.sum())


def graficar_administradores(datos, datos_crudos):
    if "adminType" not in datos.columns:
        raise ValueError("Falta la columna 'adminType' en los datos de administradores.")
    if datos.empty:
        raise ValueError("No hay administradores para graficar.")

    tipos = datos["adminType"].astype("string").str.strip().str.lower()
    tipos = tipos.map({
        "admin": "Admin",
        "superadmin": "Superadmin",
    }).fillna("Sin dato / inválido")
    conteos = tipos.value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar(conteos.index, conteos.values, color="#8b5cf6", width=0.6)
    ax.set_title(f"Tipos de administrador (N={len(datos)})")
    ax.set_ylabel("Cantidad de administradores")
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.bar_label(barras, padding=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(
        CARPETA_REPORTES / "administradores" / "tipos_cantidad.png",
        dpi=160,
    )
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.pie(
        conteos.values,
        labels=conteos.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=("#8b5cf6", "#c4b5fd", "#a78bfa")[:len(conteos)],
        wedgeprops={"width": 0.42, "edgecolor": "white"},
    )
    ax.set_title(f"Proporción por tipo de administrador (N={int(conteos.sum())})")
    fig.tight_layout()
    fig.savefig(
        CARPETA_REPORTES / "administradores" / "tipos_proporcion.png",
        dpi=160,
    )
    plt.close(fig)

    columna_id = "user_id"
    if columna_id not in datos_crudos.columns:
        raise ValueError("Falta la columna 'user_id' en administradores crudos.")
    id_unicos = datos_crudos[columna_id].dropna().nunique()
    cantidad_limpia = datos[columna_id].dropna().nunique()
    valores_calidad = pd.Series(
        {
            "Filas crudas": len(datos_crudos),
            "IDs crudos únicos": id_unicos,
            "Admins limpios": cantidad_limpia,
        }
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    barras = ax.bar(
        valores_calidad.index,
        valores_calidad.values,
        color="#8b5cf6",
        width=0.6,
    )
    ax.set_title("Control de calidad de administradores")
    ax.set_ylabel("Cantidad de registros")
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    ax.bar_label(barras, padding=2, fontsize=9)
    fig.tight_layout()
    fig.savefig(
        CARPETA_REPORTES / "administradores" / "calidad_datos.png",
        dpi=160,
    )
    plt.close(fig)
    return int(conteos.sum())


def generar_reportes(carpeta_proyecto):
    global CARPETA_PROYECTO, CARPETA_LIMPIOS, CARPETA_REPORTES

    CARPETA_PROYECTO = Path(carpeta_proyecto).resolve()
    CARPETA_LIMPIOS = CARPETA_PROYECTO / "data" / "limpios"
    CARPETA_REPORTES = CARPETA_PROYECTO / "data" / "reportes"
    for entidad in ("compradores", "vendedores", "administradores"):
        (CARPETA_REPORTES / entidad).mkdir(parents=True, exist_ok=True)

    datos_compradores = leer_entidad("compradores")
    datos_vendedores = leer_entidad("vendedores")
    datos_administradores = leer_entidad("administradores")
    ruta_administradores_crudos = (
        CARPETA_PROYECTO
        / "data"
        / "sucios"
        / "administradores_sucios.csv"
    )
    if not ruta_administradores_crudos.is_file():
        raise FileNotFoundError(
            "No se encontró el archivo crudo de administradores: "
            f"{ruta_administradores_crudos}"
        )
    datos_administradores_crudos = pd.read_csv(ruta_administradores_crudos)

    graficar_balances(datos_compradores, "compradores", "#2563eb")
    graficar_estados(datos_compradores, "compradores", "#2563eb")
    graficar_intereses(datos_compradores)
    graficar_balances(datos_vendedores, "vendedores", "#f97316")
    graficar_estados(datos_vendedores, "vendedores", "#f97316")
    graficar_ventas_vendedor(datos_vendedores)
    graficar_administradores(
        datos_administradores,
        datos_administradores_crudos,
    )
    print(f"Gráficos generados en: {CARPETA_REPORTES}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Genera gráficos separados por entidad."
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=CARPETA_PROYECTO,
        help="Carpeta raíz del proyecto (opcional).",
    )
    argumentos = parser.parse_args()
    generar_reportes(argumentos.project_dir)
