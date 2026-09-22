import random
import uuid
import pandas as pd
from faker import Faker

# 1. Configurar el Faker a la región que necesito
fake = Faker("es_CO")

# 2. Sembrar semillas para tener coherencia en los datos simulados
Faker.seed(42)
random.seed(42)

# 3. Identificar las columnas de la tabla que necesito simular
columnas_vendedores = ["id_vendedor", "nombre", "apellido", "telefono", "correo", "contacto", "status", "propiedadesVendidas", "balance"]

# 4. Identifico los datos o el dato que sea el selector
SECTORES = ["Residencial", "Comercial", "Industrial", "Rural", "Proyectos Nuevos"]

# 5. Defino mi DATASET
FILAS = 300

# 6. Construyo una función para generar los N datos pedidos (LIMPIOS)
def generar_datos_limpios(numero_datos=FILAS):
    filas = []
    for _ in range(numero_datos):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.company(),
            "apellido": fake.last_name(),
            "telefono": fake.numerify("3#########"),
            "correo": fake.company_email(),
            "contacto": fake.name(),
            "status": random.choice([True, False]),
            "propiedadesVendidas": str(random.randint(0, 50)),
            "balance": round(random.uniform(1000000.0, 500000000.0), 2)
        })
    return filas

