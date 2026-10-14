#Rutina para convertir una lista de diccionarios en multiples fuentes de información

import json
from pathlib import Path

#1. Configuración (cambiar segun su tabla)
NOMBRE_ENTIDAD = "propiedad"

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
# print(f"Carpeta del proyecto: {CARPETA_PROYECTO}")
CARPETA_CRUDOS = CARPETA_PROYECTO / "datos"/"crudos"
CARPETA_LIMPIOS = CARPETA_PROYECTO / "datos"/"limpios"
CARPETA_REPORTES = CARPETA_PROYECTO / "datos"/"reportes"

#2. Funciones genericas para elaborar los archivos de salida

#2.1 CREAR LA CARPETA
def preparar_carpeta(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True, exist_ok=True)
    return carpeta

#2.2 EXPORTAR A CSV
def exportar_csv(datos_df, carpeta, nombre_archivo):
    ruta=preparar_carpeta(carpeta)/f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, index=False, sep=";", encoding="utf-8-sig")
    return ruta

#2.3 EXPORTAR A JSON
def exportar_json(datos_df, carpeta, nombre_archivo):
    ruta=preparar_carpeta(carpeta)/f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", date_format="iso", indent=2)
    return ruta

#2.4 EXPORTAR A EXCEL
def exportar_excel(datos_df, carpeta, nombre_archivo):
    ruta=preparar_carpeta(carpeta)/f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, index=False, engine="openpyxl")
    return ruta

#3. Genero los archivos en mi proyecto
def exportar_properties_crudos(datos_sucios_df):
    return [
    exportar_csv(datos_sucios_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),

    exportar_json(datos_sucios_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),

    exportar_excel(datos_sucios_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo")
    ]