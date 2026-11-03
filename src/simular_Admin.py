
import os
from pathlib import Path
import random
import pandas as pd
from faker import Faker

# 1. Configurar Faker para Colombia
faker = Faker("es_CO")

# 3. Definir los datos de ADMIN
# user_id: clave foránea hacia USER.id
# adminType: tipo de administrador

ADMIN_TYPES = ["superadmin", "admin"]
FILAS = 300

# 4. Rutas de los archivos
CARPETA_PROYECTO = Path(
    os.environ.get(
        "PROYECTO_INTEGRADOR_DIR",
        Path(__file__).resolve().parents[1],
    )
).resolve()
CARPETA_CRUDOS = CARPETA_PROYECTO / "data" / "crudos"
CARPETA_SUCIOS = CARPETA_PROYECTO / "data" / "sucios"


# 5. Generar los datos iniciales de administradores
def generar_datos_limpios(numero_datos=FILAS, df_user=None):
    if df_user is None:
        rutas_usuarios = (
            CARPETA_PROYECTO
            / "data"
            / "crudos"
            / f"{entidad}.csv"
            for entidad in (
                "compradores",
                "vendedores",
            )
        )
        usuarios = []
        for ruta in rutas_usuarios:
            if not ruta.is_file():
                raise FileNotFoundError(
                    "Primero genera compradores y vendedores; "
                    f"no se encontró el archivo requerido: {ruta}"
                )
            usuarios.append(
                pd.read_csv(
                    ruta,
                    usecols=["user_id"],
                    dtype={"user_id": "string"},
                ).rename(columns={"user_id": "id"})
            )
        df_user = pd.concat(usuarios, ignore_index=True)
    elif "id" not in df_user.columns:
        raise ValueError("Los datos de usuarios deben tener una columna 'id'.")

    if "id" not in df_user.columns:
        raise ValueError("El archivo de usuarios debe tener una columna 'id'.")

    # Evitar identificadores vacíos y repetidos
    user_ids = df_user["id"].dropna().drop_duplicates()

    # No se pueden generar más administradores que usuarios disponibles
    if numero_datos > len(user_ids):
        raise ValueError(
            f"Solicitaste {numero_datos} administradores, "
            f"pero solo hay {len(user_ids)} usuarios disponibles."
        )

    # Seleccionar usuarios sin repetir
    user_ids = user_ids.sample(
        n=numero_datos,
    ).tolist()

    filas = []

    for user_id in user_ids:
        filas.append({
            "user_id": user_id,
            "adminType": random.choice(ADMIN_TYPES)
        })

    return pd.DataFrame(filas)


# 6. Seleccionar una muestra de registros
def generar_muestra(datos, porcentaje):
    return datos.sample(
        frac=porcentaje,
        random_state=random.randint(0, 999)
    ).index


# 7. Escribir texto con variaciones
def escribir_mal(texto):
    variantes = [
        texto.lower(),
        texto.upper(),
        texto.title()
    ]
    return random.choice(variantes)


# 8. Ensuciar intencionalmente los datos
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # 10 %: espacios adicionales en adminType
    filas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas, "adminType"] = (
        " " + datos_df.loc[filas, "adminType"] + " "
    )

    # 15 %: cambiar mayúsculas y minúsculas
    filas = generar_muestra(datos_df, 0.15)
    datos_df.loc[filas, "adminType"] = (
        datos_df.loc[filas, "adminType"].apply(escribir_mal)
    )

    # Duplicar registros sin eliminar datos válidos de administradores.
    filas_duplicadas = datos_df.sample(frac=0.05)
    return pd.concat([datos_df, filas_duplicadas], ignore_index=True)


# 9. Ejecutar el programa
if __name__ == "__main__":
    df = generar_datos_limpios()

    print("Datos limpios:")
    print("Filas y columnas:", df.shape)
    print(df.head())

    # Ensuciar los datos después de generarlos
    df_sucio = ensuciar(df)

    CARPETA_CRUDOS.mkdir(parents=True, exist_ok=True)
    CARPETA_SUCIOS.mkdir(parents=True, exist_ok=True)
    ruta_exportada = CARPETA_CRUDOS / "administradores.csv"
    ruta_sucia = CARPETA_SUCIOS / "administradores_sucios.csv"
    df.to_csv(ruta_exportada, index=False, encoding="utf-8-sig")
    df_sucio.to_csv(ruta_sucia, index=False, encoding="utf-8-sig")

    print("\nDatos después de ensuciar:")
    print("Filas y columnas:", df_sucio.shape)
    print(df_sucio.head())
    print("\nArchivo exportado en:", ruta_exportada)
    print("Archivo sucio generado en:", ruta_sucia)
   
