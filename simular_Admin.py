from pathlib import Path
import random
import pandas as pd
import Faker as faker

# 1. Sembrar semilla para tener coherencia en los datos generados
random.seed(42)

# 2. Identifico los datos que debo simular para ADMIN
# user_id (texto(UUID)) -> PK y FK hacia USER.id
# adminType (texto)

# 3. Selector de opciones
ADMIN_TYPES = ["superadmin", "admin" ]

# 4. Defino mi DATASET (cuántos usuarios serán admin)
FILAS = 300

# 5. Ruta del CSV de usuarios (de donde salen las FK)
RUTA_USER = Path("admin_simulados") / "admin.csv"

# 6. Función para generar los N datos pedidos (LIMPIOS)
def generar_datos_limpios(numero_datos=FILAS):
    df_admin = pd.read_csv(RUTA_USER)

    # Relación 1 a 0..1: un usuario solo puede ser admin una vez -> sin repetir
    user_ids = df_user["id"].sample(n=numero_datos, random_state=42).tolist()

    filas = []
    for user_id in user_ids:
        filas.append({
            "user_id": user_id,
            "adminType": random.choice(ADMIN_TYPES),
            "id": str(uuid.uuid4()),
            "password": faker.password(length=12),
            "nombre": faker.first_name(),
            "apellido": faker.last_name(),
            "telefono": faker.phone_number(),
            "correo": faker.email(),
            "status": random.choice(STATUS_OPCIONES),
                        
            
        })
    return pd.DataFrame(filas)

# 7. Interruptor
if __name__ == "__main__":
    df = generar_datos_limpios()

    print("Filas y columnas generadas:", df.shape)
    print(df.head())

    salida = Path("admins_simulados")
    salida.mkdir(parents=True, exist_ok=True)

    archivo_csv = salida / "admin.csv"
    df.to_csv(archivo_csv, index=False, encoding="utf-8-sig")

    print("Archivo generado en:", archivo_csv)

#1 funcion para definir porcentaje de error

    def generar_muestra(datos,porcentaje):
        return datos.sample(fraccion=porcentaje,
        random_state=random.randint(0,999)).index

#2 funcion para escribir mal texto 

def escribir_mal(texto):
    variantes =[texto.lower(),f"{texto.title()}", texto.capitalice()]
    return random.choice(variantes)

#3 funcion de convertir booleanos en texto

def convertir_booleanos_en_texto(valor):
    if valor:
       return random.choice(["si","1"])
    else:
       return random.choce(["no","0"])

def ensuciar_telefono(telefono):
    formato = [
        telefono,
        f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}",
        f"+57 {telefono[:3]}-{telefono[3:6]}-{telefono[6:]}"
    ]

#4 funcion para ensuciar los datos 

def ensuciar(datos_df):
    datos_df=datos_df.copy();
# para nombre 10% con espacios sobrantes al inicio y al final; 15% en MAYUSCULAS.
# para contacto 8% en None (nulos).
# para correo 6% sin la arrba (correo invalido).
# se ensucia 'correo':6% sin la arroba (correo invalido).
# se ensucia 'telefono': tres formatos mezclados:'3001234567','300123 4567','57 300 123 4567´.
    filas_elegidas=generar_muestra(datos_df, 0.1)
    datos_df.loc[filas_elegidas, "nombre"] = "" + datos_df.loc[filas_elegidas, "nombre"] + "";
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.lof[filas_elegidas, "nombre"].str.upper();
    filas_elegidas=generar_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "password"] = None
    filas_elegidas=generar_muestra(datos_df, 0.06)
    datos_df.loc[filas_elegidas, "correo"] = datos_df.loc[filas_elegidas,"correo"].str.replace("@","",regex=False );
    filas_elegidas=generar_muestra(datos_df,1)
    datos_df.loc[filas_elegidas, "telefono"] = datos_df.loc[filas_elegidas,"telefono"].apply(ensuciar_telefono)
    datos_df.loc[filas_elegidas, "status"] = datos_df.loc[filas_elegidas,"status"].map(convertir_booleanos_en_texto)
    return datos_df



   

