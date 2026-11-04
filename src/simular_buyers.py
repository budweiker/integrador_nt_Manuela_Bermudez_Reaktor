import os
from pathlib import Path
import random
import uuid
import pandas as pd
from faker import Faker

# 1. Configurar Faker para Colombia
faker = Faker("es_CO")
CARPETA_PROYECTO = Path(
    os.environ.get(
        "PROYECTO_INTEGRADOR_DIR",
        Path(__file__).resolve().parents[1],
    )
).resolve()
CARPETA_CRUDOS = CARPETA_PROYECTO / "data" / "crudos"
CARPETA_SUCIOS = CARPETA_PROYECTO / "data" / "sucios"

# 3. Opciones controladas para los datos simulados
STATUS_OPCIONES = [True, False]
PROPIEDAD_DE_INTERES_ACTUAL = ["apartamento", "casa", "finca", "apartaestudio"]
FILAS = 300


def generar_datos_limpios(numero_datos=FILAS):
    filas = []
    for _ in range(numero_datos):
        filas.append({
            "user_id": str(uuid.uuid4()),
            "password": faker.password(length=12),
            "nombre": faker.name(),
            "telefono": generar_telefono(),
            "correo": faker.email(),
            "status": random.choice(STATUS_OPCIONES),
            "propiedad_de_interes": random.choice(PROPIEDAD_DE_INTERES_ACTUAL),
            "balance": round(random.uniform(0, 500000000), 2)
        })
    return pd.DataFrame(filas)


def generar_telefono():
    return "3" + "".join(str(random.randint(0, 9)) for _ in range(9))


def generar_muestra(datos, porcentaje):
    return datos.sample(
        frac=porcentaje,
        random_state=random.randint(0, 999)
    ).index


def escribir_mal(texto):
    variantes = [texto.lower(), f" {texto.title()} ", texto.capitalize()]
    return random.choice(variantes)


def convertir_booleano_en_texto(valor):
    if valor:
        return random.choice(["Si", "1"])
    else:
        return random.choice(["No", "0"])


def ensuciar(datos_df):
    datos_df = datos_df.copy()

    filas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas, "nombre"] = (
        " " + datos_df.loc[filas, "nombre"] + " "
    )

    filas = generar_muestra(datos_df, 0.15)
    datos_df.loc[filas, "nombre"] = (
        datos_df.loc[filas, "nombre"].str.upper()
    )

    filas = generar_muestra(datos_df, 0.08)
    datos_df.loc[filas, "telefono"] = datos_df.loc[
        filas, "telefono"
    ].map(lambda telefono: f"+57 {telefono[:3]}-{telefono[3:6]}-{telefono[6:]}")

    filas = generar_muestra(datos_df, 0.06)
    datos_df.loc[filas, "correo"] = (
        datos_df.loc[filas, "correo"].str.replace("@", " ", regex=False)
    )

    datos_df["status"] = datos_df["status"].astype(object)
    filas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas, "status"] = (
        datos_df.loc[filas, "status"].map(convertir_booleano_en_texto)
    )

    filas = generar_muestra(datos_df, 0.05)
    datos_df = pd.concat([datos_df, datos_df.loc[filas]], ignore_index=True)

    return datos_df


if __name__ == "__main__":
    df = generar_datos_limpios()
    df_sucio = ensuciar(df)

    CARPETA_CRUDOS.mkdir(parents=True, exist_ok=True)
    CARPETA_SUCIOS.mkdir(parents=True, exist_ok=True)

    ruta_exportada = CARPETA_CRUDOS / "compradores.csv"
    ruta_sucia = CARPETA_SUCIOS / "compradores_sucios.csv"
    df.to_csv(ruta_exportada, index=False, encoding="utf-8-sig")
    df_sucio.to_csv(ruta_sucia, index=False, encoding="utf-8-sig")

    print(f"Datos exportados ({df.shape[0]} filas): {ruta_exportada}")
    print(f"Datos sucios ({df_sucio.shape[0]} filas): {ruta_sucia}")
