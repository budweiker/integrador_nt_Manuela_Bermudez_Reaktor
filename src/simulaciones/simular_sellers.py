import random
import uuid
import pandas as pd
from faker import Faker

# 1. Configurar el faker a la región que necesito
faker = Faker("es_CO")
""" CARPETA_PROYECTO = Path(
    os.environ.get(
        "PROYECTO_INTEGRADOR_DIR",
        Path(__file__).resolve().parents[1],
    )
).resolve()
CARPETA_EXPORTAR = CARPETA_PROYECTO / "data" / "exportar" / "vendedores"
CARPETA_ENSUCIAR = CARPETA_PROYECTO / "data" / "ensuciar" / "vendedores" """
#2. Sembrar las semillas
Faker.seed(42)
random.seed(42)


# 3. Identifico los datos que debo simular y los campos que necesito para USER + SELLER
# user_id (texto(UUID))
# password (texto)
# nombre (texto)
# apellido (texto)
# telefono (texto)
# correo (texto)
# status (boolean)
# propiedadesVendidas (int)
# balance (float)

# 4. Identifico los datos o el dato que sea un selector de opciones, para generar datos aleatorios de manera controlada
PROPIEDADES_VENDIDAS = [0, 1, 2, 3, 4, 5, 8, 10, 12, 15]
STATUS_OPCIONES = [True, False]

# 5. Defino mi DATASET
FILAS = 300

# 6. Funciones auxiliares

#Reproducibilidad del UUID
def generar_uuid():
       return str(uuid.UUID(int=random.getrandbits(128), version=4))

def generar_telefono():
    return "3" + "".join(str(random.randint(0,9)) for _ in range(9))

# 7. Construyo una función para generar los N datos pedidos (LIMPIOS)
def generar_datos_limpios(numero_datos=FILAS):
    filas = []
    for _ in range(numero_datos):
        filas.append({
            "user_id": generar_uuid(),
            "password": faker.password(length=12),
            "nombre": faker.name(),
            "apellido": faker.last_name(),
            "telefono": generar_telefono(),
            "correo": faker.email(),
            "status": random.choice(STATUS_OPCIONES),
            "propiedadesVendidas": random.choice(PROPIEDADES_VENDIDAS),
            "balance": round(random.uniform(0, 500000000), 2)
        })
    return pd.DataFrame(filas)

# ------------ Ensuciar los datos ------------

#1. Porcentaje de filas afectadas
def generar_muestra(datos,porcentaje):
    return datos.sample(frac=porcentaje,random_state=random.randint(0,999)).index

#2. Función para escribir mal un texto
def escribir_mal(texto):
    variantes =[texto.lower(),f" {texto.title()} ", texto.capitalize()]
    return random.choice(variantes)

#3. Función para convertir un booleano en texto
def convertir_booleano_en_texto(valor):
    if valor:
        return random.choice(["Si", "1"])
    else:
        return random.choice(["No", "0"])

#4. Función para ensuciar el teléfono
def ensuciar_telefono(telefono):
    formatos = [
        telefono,
        f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}",
        f"+57 {telefono[:3]}-{telefono[3:6]}-{telefono[6:]}"
    ]
    return random.choice(formatos)


#5. Función principal para ensuciar los datos de vendedores
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # nombre: 10 % de filas con espacios adicionales, 15 % de filas con mayúsculas  
    filas_elegidas = generar_muestra(datos_df, 0.1)
    datos_df.loc[filas_elegidas, "nombre"] = (
        " " + datos_df.loc[filas_elegidas, "nombre"] + " "
    )

    filas_elegidas = generar_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "nombre"] = (
        datos_df.loc[filas_elegidas, "nombre"].str.upper()
    )
    # apellido: 10 % de filas con espacios adicionales, 15 % de filas con mayúsculas 
    filas_elegidas = generar_muestra(datos_df, 0.1)
    datos_df.loc[filas_elegidas, "apellido"] = (
        " " + datos_df.loc[filas_elegidas, "apellido"] + " "
    )   

    filas_elegidas = generar_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "apellido"] = (
        datos_df.loc[filas_elegidas, "apellido"].str.upper()
    )

    # correo: 6 % de filas con @ reemplazado por espacio
    filas_elegidas = generar_muestra(datos_df, 0.06)
    datos_df.loc[filas_elegidas, "correo"] = (
        datos_df.loc[filas_elegidas, "correo"].str.replace(
            "@", " ", regex=False
        )
    )
    # telefono: 100 % de filas con diferentes formatos
    filas_elegidas = generar_muestra(datos_df, 1)
    datos_df.loc[filas_elegidas, "telefono"] = datos_df.loc[filas_elegidas, "telefono"].apply(ensuciar_telefono)

    # status: 10 % de filas con booleanos convertidos a texto, 5 % de filas duplicadas
    datos_df["status"] = datos_df["status"].astype(object)
    filas_elegidas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "status"] = datos_df.loc[filas_elegidas, "status"].map(convertir_booleano_en_texto)
    
    # 5 % de filas duplicadas
    filas_duplicadas_indices = generar_muestra(datos_df, 0.05)
    filas_duplicadas = datos_df.loc[filas_duplicadas_indices]
    datos_df = pd.concat([datos_df, filas_duplicadas], ignore_index=True)

    return datos_df

""" if __name__ == "__main__":
    df = generar_datos_limpios()

    print("Filas y columnas generadas:", df.shape)
    print(df.head())

    CARPETA_EXPORTAR.mkdir(parents=True, exist_ok=True)
    CARPETA_ENSUCIAR.mkdir(parents=True, exist_ok=True)

    archivo_exportado = CARPETA_EXPORTAR / "vendedores.csv"
    df.to_csv(archivo_exportado, index=False, encoding="utf-8-sig")

    df_ensuciado = ensuciar(df)
    archivo_sucio = CARPETA_ENSUCIAR / "vendedores_sucios.csv"
    df_ensuciado.to_csv(archivo_sucio, index=False, encoding="utf-8-sig")

    print("Archivo exportado generado en:", archivo_exportado)
    print("Archivo sucio generado en:", archivo_sucio) """
