from pathlib import Path
import random
import uuid
import pandas as pd
from faker import Faker

# 1. Configurar el faker a la región que necesito
faker = Faker("es_CO")

# 2. Sembrar semilla para tener coherencia en los datos generados
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
FILAS = 100

# 6. Construyo una función para generar los N datos pedidos (LIMPIOS)
def generar_datos_limpios(numero_datos=FILAS):
    filas = []
    for _ in range(numero_datos):
        first_name = faker.first_name()
        last_name = faker.last_name()
        
        filas.append({
            "user_id": str(uuid.uuid4()),
            "password": faker.password(length=12),
            "nombre": faker.name(),
            "telefono": generar_telefono(),
            "correo": faker.email(),
            "status": random.choice(STATUS_OPCIONES),
            "propiedadesVendidas": random.choice(PROPIEDADES_VENDIDAS),
            "balance": round(random.uniform(0, 500000000), 2)
        })
    return pd.DataFrame(filas)


def generar_telefono():
    return "3" + "".join(str(random.randint(0, 9)) for _ in range(9))
#Funcion para ensuciar datos
def generar_muestra(datos,porcentaje):
    return datos.sample(frac=porcentaje,random_state=random.randint(0,999)).index
#FUncion para generar "el tipo de ensuciar los datos"

def escribir_mal(texto):
    variantes =[texto.lower(),f" {texto.title()} ", texto.capitalize()]
    return random.choice(variantes)
def convertir_booleano_en_texto(valor):
    if valor:
        return random.choice(["Si", "1"])
    else:
        return random.choice(["No", "0"])

def ensuciar_telefono(telefono):
    formatos = [
        telefono,
        f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}",
        f"+57 {telefono[:3]}-{telefono[3:6]}-{telefono[6:]}"
    ]
    return random.choice(formatos)


#funcion para ensuciar los datos
def ensuciar(datos_df):
    datos_df=datos_df.copy();

#para nombre  10% con espacios sobrantes al inicio y al final; 15% en MAYUSCULAS.
# para contacto 8% en None (nulos).
#para correo 6% sin la arroba (correo invalido).
#Se ensucia `correo`: 6% sin la arroba (correo invalido).
#Se ensucia `telefono`: tres formatos mezclados: '3001234567', '300 123 4567', '+57 300-123-4567'.

#Se ensucia `estado`: a veces como texto: 'SI', 'No', '1', '0'.
#Repetir 5 registros

    filas_elegidas=generar_muestra(datos_df, 0.1)
    datos_df["status"] = datos_df["status"].astype(object)
    datos_df.loc[filas_elegidas, "nombre"] = " " + datos_df.loc[filas_elegidas, "nombre"] + " ";
    filas_elegidas=generar_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "nombre"] = datos_df.loc[filas_elegidas, "nombre"].str.upper();
    filas_elegidas=generar_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "password"] = None
    filas_elegidas=generar_muestra(datos_df, 0.06)
    datos_df.loc[filas_elegidas, "correo"] = datos_df.loc[filas_elegidas, "correo"].str.replace("@" , " ", regex=False );
    filas_elegidas=generar_muestra(datos_df,1)
    datos_df.loc[filas_elegidas, "telefono"] = datos_df.loc[filas_elegidas, "telefono"].apply(ensuciar_telefono)
    datos_df.loc[filas_elegidas, "status"] = datos_df.loc[filas_elegidas, "status"].map(convertir_booleano_en_texto)
    filas_elegidas=generar_muestra(datos_df,0.05)
    
   

    return datos_df

if __name__ == "__main__":
    df = generar_datos_limpios()

    print("Filas y columnas generadas:", df.shape)
    print(df.head())

    salida = Path("vendedores_simulados")
    salida.mkdir(parents=True, exist_ok=True)
    
    archivo_csv = salida / "vendedor.csv"
    df.to_csv(archivo_csv, index=False, encoding="utf-8-sig")

    print("Archivo generado en:", archivo_csv)
    df_ensuciado = ensuciar(df)
    salida = Path("vendedores_simulados_ensuciados")
    salida.mkdir(parents=True, exist_ok=True)
    archivo_csv = salida / "vendedor_ensuciado.csv"
    df_ensuciado.to_csv(archivo_csv, index=False, encoding="utf-8-sig")
    








