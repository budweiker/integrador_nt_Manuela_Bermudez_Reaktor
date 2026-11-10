
import random
import uuid
import pandas as pd
from faker import Faker

# 1. Configurar Faker para Colombia
faker = Faker("es_CO")

# 2. Sembrar las semillas
Faker.seed(42)
random.seed(42)

#3. Identifico los datos que debo simular y los campos que necesito para Admin
# admin_id (texto(UUID))
# password (texto)
# nombre (texto)    
# apellido (texto)
# telefono (texto)
# correo (texto)
# status (boolean)
# adminType (texto) - opciones: "admin", "developer"

# 4. Opciones controladas para los datos simulados
ADMIN_TYPES = ["developer", "admin"]
STATUS_OPCIONES = [True, False]

# 5. Defino mi DATASET
FILAS = 10

# 6. Funciones auxiliares
def generar_uuid():
    return str(uuid.UUID(int=random.getrandbits(128), version=4))

def generar_telefono():
    return "3" + "".join(str(random.randint(0, 9)) for _ in range(9))

# 7. Generar los datos iniciales de administradores
def generar_datos_limpios(numero_datos=FILAS, df_user=None):
        filas = []
        for _ in range(numero_datos):
            filas.append({
                "user_id": generar_uuid(),
                "password": faker.password(),
                "nombre": faker.first_name(),
                "apellido": faker.last_name(),
                "telefono": generar_telefono(),
                "correo": faker.email(),
                "status": random.choice(STATUS_OPCIONES),
                "adminType": random.choice(ADMIN_TYPES)
            })
        return pd.DataFrame(filas)
        
# ----------- Ensuciar los datos de administradores ---------------

# 1. porcentaje de filas afectadas
def generar_muestra(datos, porcentaje):
    return datos.sample(
        frac=porcentaje,
        random_state=random.randint(0, 999)
    ).index


# 2. Escribir texto con variaciones
def escribir_mal(texto):
    variantes = [
        texto.lower(),
        texto.upper(),
        texto.title(),
        f" {texto} ",
        texto.capitalize()
    ]
    return random.choice(variantes)

# 3. Convertir booleano a texto
def convertir_booleano_en_texto(valor):
    if valor:
        return random.choice(["Si", "1"])
    else:
        return random.choice(["No", "0"])

# 4. Ensuciar teléfono con diferentes formatos
def ensuciar_telefono(telefono):
    formatos = [
        telefono,
        f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}",
        f"+57 {telefono[:3]}-{telefono[3:6]}-{telefono[6:]}"
    ]
    return random.choice(formatos)    

# 5. Ensuciar intencionalmente los datos
def ensuciar(datos_df):
    datos_df = datos_df.copy()

    # nombre: 10 % de filas con espacios adicionales, 20 % de filas con mayúsculas
    filas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas, "nombre"] = (
        " " + datos_df.loc[filas, "nombre"] + " "
    )

    filas = generar_muestra(datos_df, 0.20)
    datos_df.loc[filas, "nombre"] = (
        datos_df.loc[filas, "nombre"].str.upper()
    ) 

    # apellido: 20% con errores de escritura  
    filas = generar_muestra(datos_df, 0.20)
    datos_df.loc[filas, "apellido"] = (
        datos_df.loc[filas, "apellido"].map(escribir_mal)
    )

    # telefono: 10 % de filas con diferentes formatos
    filas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas, "telefono"] = (
        datos_df.loc[filas, "telefono"].apply(ensuciar_telefono)
    )

    # correo: 10 % de filas con @ reemplazado por espacio
    filas = generar_muestra(datos_df, 0.10)
    datos_df.loc[filas, "correo"] = (
        datos_df.loc[filas, "correo"].str.replace("@", " ", regex=False)
    )

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

    # 20 %: cambiar booleanos a texto
    filas = generar_muestra(datos_df, 0.20)
    datos_df.loc[filas, "adminType"] = (
        datos_df.loc[filas, "adminType"].map(convertir_booleano_en_texto)
    )

    # Duplicar 10% de registros sin eliminar datos válidos de administradores.
    filas = generar_muestra(datos_df, 0.10)
    datos_df = pd.concat([datos_df, datos_df.loc[filas]], ignore_index=True)   

    return datos_df
    



   
