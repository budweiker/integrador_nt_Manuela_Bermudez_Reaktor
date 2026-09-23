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
FILAS = 500

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
            "telefono": faker.phone_number(),
            "correo": faker.email(),
            "status": random.choice(STATUS_OPCIONES),
            "propiedadesVendidas": random.choice(PROPIEDADES_VENDIDAS),
            "balance": round(random.uniform(0, 500000000), 2)
        })
    return pd.DataFrame(filas)

# 7. Interruptor if __name__ == "__main__": 

if __name__ == "__main__":
    df = generar_datos_limpios()

    print("Filas y columnas generadas:", df.shape)
    print(df.head())

    salida = Path("vendedores_simulados")
    salida.mkdir(parents=True, exist_ok=True)
    
    archivo_csv = salida / "vendedor.csv"
    df.to_csv(archivo_csv, index=False, encoding="utf-8-sig")

    print("Archivo generado en:", archivo_csv)