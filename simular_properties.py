'''
El elemento central: la necesidad que publica la Inmobiliaria. Crea el script src/simular_propiedades.py. Con la libreria Faker genera 500 filas falsas de la tabla propiedades, con las MISMAS columnas que usa Backend II. Despues ensucia los datos a proposito: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa Faker("es_CO") y fija la semilla con Faker.seed(42) y random.seed(42) para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.
'''
from datetime import timedelta
from pathlib import Path
import random
import uuid
from faker import Faker
import pandas as pd

#1. configurar el faker a la region que necesito
faker = Faker("es_CO")

#2. Sembrar semilla parar tener coherencia en los datos generados
Faker.seed(42)
random.seed(42)

#3. identifico los datos que debo simular y los campos que necesito para la tabla propiedades
#id (texto(UUID))
#valorPropiedad (float) 
#direccionPropiedad (texto)
#numeroHabitaciones (int)
#estrato (int)
#barrio (texto)

#4. Identifico los datos o el dato que sea un selector de opciones, para generar datos aleatorios de manera controlada
ESTRATOS = [1, 2, 3, 4, 5, 6]
BARRIOS = ["Poblado", "Laureles", "Envigado", "Sabaneta", "Belen", "Itagui", "Caldas", "La Estrella"]
NUMERO_HABITACIONES = [1, 2, 3, 4, 5]
ESTADO = ["Disponible", "Vendido", "Alquilado", "Reservado", "En construcción"]
TIPOS_PROPIEDAD = ["Apartamento", "Casa", "Finca", "Local Comercial", "Oficina"]

#5. Defino mi DATASET
FILAS = 500

#6 creo una función para generar una descripción más realista de la propiedad
def generar_descripcion():
    tipo = random.choice(TIPOS_PROPIEDAD)
    habitaciones = random.choice(NUMERO_HABITACIONES)
    area = round(random.uniform(30.0, 300.0), 2)
    estrato = random.choice(ESTRATOS)
    barrio = random.choice(BARRIOS)
    descripcion = (
        f"Se vende {tipo} de {habitaciones} habitaciones, con un área de {area} m², "
        f"ubicada en el barrio {barrio}, estrato {estrato}. Ideal para familias o inversión."
    )
    return {
        "descripcion": descripcion,
        "tipo": tipo,
        "habitaciones": habitaciones,
        "area": area,
        "estrato": estrato,
        "barrio": barrio
    }


#7. Construyo una función para generar los N datos pedidos (LIMPIOS)
def generar_datos_limpios(numero_datos=FILAS):
    filas = []
    for _ in range(numero_datos):
        propiedad = generar_descripcion()
        fecha_inicio = faker.date_time_between(start_date="-2y", end_date="now")

        fecha_fin = fecha_inicio + timedelta(days=random.randint(30, 365))

        filas.append({
            "id": str(uuid.uuid4()),
            "valorPropiedad": round(random.uniform(50000000, 1000000000), 2),
            "direccionPropiedad": faker.address().replace("\n", " "),
            "descripcion": propiedad["descripcion"],
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "numeroHabitaciones": propiedad["habitaciones"],
            "area": propiedad["area"],
            "baños": random.randint(1, 5),
            "estrato": propiedad["estrato"],
            "barrio": propiedad["barrio"],
            "estado": random.choice(ESTADO),
            "tipo_propiedad": propiedad["tipo"]
        })
    return pd.DataFrame(filas)


    

#Ensuciar los datos
#1. Crear una función para definir porcentajes de error
def generar_muestra(datos,porcentaje):
        return datos.sample(
            frac=porcentaje,
            random_state=random.randint(0, 999)
            ).index

#2. Crear una funcion para escribir mal un texto
def escribir_mal(texto):

        variantes=[
            texto.lower(),
            texto.upper(),
            f" {texto} ",
            texto.capitalize(),
            texto.replace("a", "@").replace("e", "3").replace("i", "1").replace("o", "0").replace("u", "v"  )
            ]
        return random.choice(variantes)

#3. Crear una funcion para ensuciar la descripcion de la propiedad
def ensuciar_descripcion(texto):
        variantes = [
            texto.upper(),
            texto.lower(),
            texto.replace(" ", "  "),
            texto.replace("a", "@").replace("e", "3").replace("i", "1").replace("o", "0").replace("u", "v"),
            texto + "!!!",
            texto.replace("Se vende", "Vendo")
        ]
        return random.choice(variantes)

#4. Convertir booleanos en textos
def convertir_booleano_texto(valor):
        if valor:
            return random.choice(["SI", "1"])
        return random.choice(["NO", "0"])

#5. Funcion para ensuciar los datos
def ensuciar(datos_df):
            datos_df=datos_df.copy()

            #barrio: 10% con espacios sobrantes, 8% Mayuscula
            filas_elegidas=generar_muestra(datos_df,0.10)
            datos_df.loc[filas_elegidas,"barrio"] = " " + datos_df.loc[filas_elegidas,"barrio"] + " "

            filas_elegidas=generar_muestra(datos_df,0.08)
            datos_df.loc[filas_elegidas,"barrio"]=datos_df.loc[filas_elegidas,"barrio"].str.upper()

            #barrio con errores de escritura 5%
            filas_elegidas=generar_muestra(datos_df,0.05)
            datos_df.loc[filas_elegidas,"barrio"]=datos_df.loc[filas_elegidas,"barrio"].map(escribir_mal)

            """#correo: 12% Mayusculas 5% sin el arroba 4% en None
            filas_elegidas=generar_muestra(datos_df,0.12)
            datos_df.loc[filas_elegidas,"correo"]=datos_df.loc[filas_elegidas,"correo"].str.upper()

            filas_elegidas=generar_muestra(datos_df,0.05)
            datos_df.loc[filas_elegidas,"correo"]=datos_df.loc[filas_elegidas,"correo"].str.replace("@","",regex=False)

            filas_elegidas=generar_muestra(datos_df,0.04)
            datos_df.loc[filas_elegidas,"correo"]=None """

            #Estrato como texto (uno, dos, tres, cuatro, cinco, seis) 8%
            filas_elegidas=generar_muestra(datos_df,0.08)
            datos_df["estrato"]=datos_df["estrato"].astype(str)
            datos_df.loc[filas_elegidas,"estrato"]=datos_df.loc[filas_elegidas,"estrato"].map({
                "1": "uno",
                "2": "dos",
                "3": "tres",
                "4": "cuatro",
                "5": "cinco",
                "6": "seis"
            })

            #datos_df.loc[filas_elegidas,"estrato"]=("Estrato " + datos_df.loc[filas_elegidas,"estrato"].astype(str))

            """ #rol variantes de escritura (admin ADMIN Admin)
            filas_elegidas=generar_muestra(datos_df,0.07)
            datos_df.loc[filas_elegidas,"rol"]=datos_df.loc[filas_elegidas,"rol"].map(escribir_mal) """

            #Descripcion: 15% con errores de escritura, 5% con espacios sobrantes, 5% con mayusculas, 3% valores nulos
            filas_elegidas=generar_muestra(datos_df,0.15)
            datos_df.loc[filas_elegidas,"descripcion"]=datos_df.loc[filas_elegidas,"descripcion"].map(ensuciar_descripcion)
            datos_df.loc[filas_elegidas,"descripcion"]=datos_df.loc[filas_elegidas,"descripcion"] + " "
            filas_elegidas=generar_muestra(datos_df,0.05)
            datos_df.loc[filas_elegidas,"descripcion"]=datos_df.loc[filas_elegidas,"descripcion"].str.upper()
            filas_elegidas=generar_muestra(datos_df,0.03)
            datos_df.loc[filas_elegidas,"descripcion"]=None

            #fecha dos formatos mezclados (2026-03-15 14:30:00 y 15/03/2026 14:30) formato ISO y latin
            iso=pd.to_datetime(datos_df["fecha_inicio"]).dt.strftime("%Y-%m-%d %H:%M:%S")
            latino=pd.to_datetime(datos_df["fecha_inicio"]).dt.strftime("%d/%m/%Y %H:%M")
            datos_df["fecha_iso"]=iso
            filas_elegidas=generar_muestra(datos_df,0.4)
            datos_df.loc[filas_elegidas,"fecha_latin"]=latino.loc[filas_elegidas]

            """ #activo en ocasiones llega SI NO 1 o 0
            filas_elegidas=generar_muestra(datos_df,0.03)
            datos_df.loc[filas_elegidas,"activo"]=datos_df[filas_elegidas,"activo"].map(convertir_booleano_texto) """

            #Habitaciones fuera de rango
            filas_elegidas=generar_muestra(datos_df,0.02)
            datos_df.loc[filas_elegidas,"numeroHabitaciones"]=random.randint(10, 20)

            #Duplicados 2%
            duplicados=datos_df.loc[filas_elegidas]

            datos_df = pd.concat([datos_df, duplicados], ignore_index=True)

            return datos_df


#Interruptor if __name__ == "__main__": 

if __name__ == "__main__":
    df = generar_datos_limpios()

    print("Filas y columnas generadas:", df.shape)
    print(df.head())

    salida = Path("propiedades_simuladas")
    salida.mkdir(parents=True, exist_ok=True)

    archivo = salida/"propiedades_simuladas.csv"
    if archivo.exists():
        archivo.unlink()
    df.to_csv(archivo, index=False, encoding="utf-8-sig")


    print("Archivo generado en:", salida/"propiedades_simuladas.csv")

    df_ensuciado = ensuciar(df)
    salida = Path("propiedades_simuladas_ensuciadas")
    salida.mkdir(parents=True, exist_ok=True)
    archivo = salida/"propiedades_simuladas_ensuciadas.csv"
    if archivo.exists():
        archivo.unlink()
    df_ensuciado.to_csv(archivo, index=False, encoding="utf-8-sig") 
    print("Archivo generado en:", salida/"propiedades_simuladas_ensuciadas.csv")
