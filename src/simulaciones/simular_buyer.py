import random
import uuid
import pandas as pd
from faker import Faker

# 1. Configurar Faker para Colombia
faker = Faker("es_CO")

# 2. Sembrar las semillas
Faker.seed(42)
random.seed(42)

#3. Identifico los datos que debo simular y los campos que necesito para USER + BUYER
# user_id (texto(UUID))
# password (texto)
# nombre (texto)    
# apellido (texto)
# telefono (texto)
# correo (texto)
# status (boolean)
# propiedad_de_interes (texto)
# balance (float)

# 4. Opciones controladas para los datos simulados
STATUS_OPCIONES = [True, False]

# 5. Defino mi DATASET
FILAS = 300

# 6. Funciones auxiliares
def generar_uuid():
    return str(uuid.UUID(int=random.getrandbits(128), version=4))

def generar_telefono():
    return "3" + "".join(str(random.randint(0, 9)) for _ in range(9))

# 7. Construyo una función para generar los datos limpios
def generar_datos_limpios(numero_datos=FILAS, df_propiedades=None):
    if df_propiedades is None:
        raise ValueError("Se requiere un DataFrame de propiedades para generar datos de compradores.")
    if"property_id" not in df_propiedades.columns:
        raise ValueError("El DataFrame de propiedades debe contener la columna 'property_id'.")

    propiedades_ids = df_propiedades["property_id"].dropna().drop_duplicates().tolist()

    filas = []
    for _ in range(numero_datos):
        filas.append({
            "user_id": generar_uuid(),
            "password": faker.password(length=12),
            "nombre": faker.first_name(),
            "apellido": faker.last_name(),
            "telefono": generar_telefono(),
            "correo": faker.email(),
            "status": random.choice(STATUS_OPCIONES),
            "propiedad_de_interes": random.choice(propiedades_ids),
            "balance": round(random.uniform(0, 500000000), 2)
        })
    return pd.DataFrame(filas)

# ------------ Ensuciar los datos ------------

#1. porcentaje de filas a ensuciar
def generar_muestra(datos, porcentaje):
    return datos.sample(
        frac=porcentaje,
        random_state=random.randint(0, 999)
    ).index

#2. Escribir mal el texto (cambiar mayúsculas y minúsculas, agregar espacios)
def escribir_mal(texto):
    variantes = [texto.lower(), f" {texto.title()} ", texto.capitalize()]
    return random.choice(variantes)

#3. Booleano a texto (Si/No o 1/0)
def convertir_booleano_en_texto(valor):
    if valor:
        return random.choice(["Si", "1"])
    else:
        return random.choice(["No", "0"])

#4. Ensuciar teléfono con datos de diferentes formatos
def ensuciar_telefono(telefono):
    formatos = [
        telefono,
        f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}",
        f"+57 {telefono[:3]}-{telefono[3:6]}-{telefono[6:]}"
    ]
    return random.choice(formatos)

#5. Función principal para ensuciar los datos de compradores
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # nombre: 10 % de filas con espacios adicionales, 15 % de filas con mayúsculas
    filas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas, "nombre"] = (
        " " + datos_df.loc[filas, "nombre"] + " "
    )

    filas = generar_muestra(datos_df, 0.15)
    datos_df.loc[filas, "nombre"] = (
        datos_df.loc[filas, "nombre"].str.upper()
    )

    # apellido: 7% con errores de escritura
    filas = generar_muestra(datos_df, 0.07)
    datos_df.loc[filas, "apellido"] = (
        datos_df.loc[filas, "apellido"].map(escribir_mal)
    )

    # telefono: 8 % de filas con diferentes formatos
    filas = generar_muestra(datos_df, 0.08)
    datos_df.loc[filas, "telefono"] = datos_df.loc[
        filas, "telefono"
    ].map(ensuciar_telefono)

    # correo: 6 % de filas con @ reemplazado por espacio
    filas = generar_muestra(datos_df, 0.06)
    datos_df.loc[filas, "correo"] = (
        datos_df.loc[filas, "correo"].str.replace("@", " ", regex=False)
    )

    # status: 10 % de filas con valores booleanos convertidos a texto
    datos_df["status"] = datos_df["status"].astype(object)
    filas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas, "status"] = (
        datos_df.loc[filas, "status"].map(convertir_booleano_en_texto)
    )

    # 5 % de filas duplicadas
    filas = generar_muestra(datos_df, 0.05)
    datos_df = pd.concat([datos_df, datos_df.loc[filas]], ignore_index=True)

    return datos_df


""" if __name__ == "__main__":
    df = generar_datos_limpios()
    df_sucio = ensuciar(df)

    CARPETA_EXPORTAR.mkdir(parents=True, exist_ok=True)
    CARPETA_ENSUCIAR.mkdir(parents=True, exist_ok=True)

    ruta_exportada = CARPETA_EXPORTAR / "compradores.csv"
    ruta_sucia = CARPETA_ENSUCIAR / "compradores_sucios.csv"
    df.to_csv(ruta_exportada, index=False, encoding="utf-8-sig")
    df_sucio.to_csv(ruta_sucia, index=False, encoding="utf-8-sig")

    print(f"Datos exportados ({df.shape[0]} filas): {ruta_exportada}")
    print(f"Datos sucios ({df_sucio.shape[0]} filas): {ruta_sucia}") """
