'''
El elemento central: la necesidad que publica la Inmobiliaria. Crea el script src/simular_propiedades.py. Con la libreria Faker genera 500 filas falsas de la tabla propiedades, con las MISMAS columnas que usa Backend II. Despues ensucia los datos a proposito: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa Faker("es_CO") y fija la semilla con Faker.seed(42) y random.seed(42) para que el resultado sea SIEMPRE el mismo y tu compañero pueda reproducirlo.
'''
from pathlib import Path
import random
import uuid
from faker import Faker

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

#5. Defino mi DATASET
FILAS = 500

#6. Construyo una función para generar los N datos pedidos (LIMPIOS)
def generar_datos_limpios(numero_datos=FILAS):
    filas = []
    for _ in range(numero_datos):

        filas.append({
            "id": str(uuid.uuid4()),
            "valorPropiedad": round(random.uniform(50000000, 1000000000), 2),
            "direccionPropiedad": faker.address().replace("\n", " "),
            "numeroHabitaciones": random.choice(NUMERO_HABITACIONES),
            "estrato": random.choice(ESTRATOS),
            "barrio": random.choice(BARRIOS)
        })
    return pd.DataFrame(filas)

#7 Interruptor if __name__ == "__main__": 

if __name__ == "__main__":
    df = generar_datos_limpios()

    print("Filas y columnas generadas:", df.shape)
    print(df.head())

    salida = Path("propiedades_simuladas.csv")
    salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(salida/"comprador.csv", index=False, encoding="utf-8-sig")

    print("Archivo generado en:", salida/"comprador.csv")

