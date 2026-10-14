
from pathlib import Path
import random
import pandas as pd
from faker import Faker

# 1. Configurar Faker para Colombia
faker = Faker("es_CO")

# 2. Semillas para reproducir los datos
Faker.seed(42)
random.seed(42)

# 3. Definir los datos de ADMIN
# user_id: clave foránea hacia USER.id
# adminType: tipo de administrador

ADMIN_TYPES = ["superadmin", "admin"]
FILAS = 300

# 4. Rutas de los archivos
RUTA_USER = Path("users_simulados") / "user.csv"
RUTA_SALIDA = Path("admins_simulados") / "admin.csv"


# 5. Generar los datos iniciales de administradores
def generar_datos_limpios(numero_datos=FILAS):
    # Leer los usuarios existentes
    df_user = pd.read_csv(RUTA_USER, dtype={"id": str})

    # Comprobar que existe la columna id
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
        random_state=42
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

    # 8 %: valores nulos en adminType
    filas = generar_muestra(datos_df, 0.08)
    datos_df.loc[filas, "adminType"] = None

    # 2 %: duplicar algunos user_id para practicar limpieza
    # Esto introduce una inconsistencia intencional.
    cantidad = max(1, int(len(datos_df) * 0.02))
    if len(datos_df) > 1:
        indices = datos_df.index.tolist()
        indices_destino = indices[:cantidad]
        indices_origen = indices[cantidad:cantidad * 2]

        if len(indices_origen) == len(indices_destino):
            datos_df.loc[indices_destino, "user_id"] = (
                datos_df.loc[indices_origen, "user_id"].to_numpy()
            )

    return datos_df


# 9. Ejecutar el programa
if __name__ == "__main__":
    df = generar_datos_limpios()

    print("Datos limpios:")
    print("Filas y columnas:", df.shape)
    print(df.head())

    # Ensuciar los datos después de generarlos
    df_sucio = ensuciar(df)

    # Crear la carpeta de salida
    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)

    # Guardar el archivo sucio
    df_sucio.to_csv(
        RUTA_SALIDA,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nDatos después de ensuciar:")
    print("Filas y columnas:", df_sucio.shape)
    print(df_sucio.head())
    print("\nArchivo generado en:", RUTA_SALIDA)
   

