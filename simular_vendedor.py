# /*vendedores de inmobiliaria Manuela Bermudez. Crea el script src/simular_vendedores.
# py. Con la libreria Faker genera 300 filas falsas de la tabla vendedores, con las MISMAS 
# columnas que usa Backend II. Despues ensucia los datos a proposito: nulos, duplicados, espacios 
# sobrantes, mayusculas mezcladas y formatos distintos. Esos errores son los que vas a arreglar en 
# la etapa de limpieza, asi que tienen que quedar bien puestos.

# Usa Faker("es_CO") y fija la semilla con Faker.seed(42) y random.seed(42) para que el resultado
# sea SIEMPRE el mismo y tu compañero pueda reproducirlo.*/

#3. identifica las columnas de la tabla vendedores que necesito simular

#columnas_vendedores = ["id_vendedor", "nombre", "apellido", "telefono", "email"]
    
import random
import uuid
import pandas as pd
from faker import Faker

# 1. Configurar Faker a la región requerida
fake = Faker("es_CO")

# 2. Sembrar semillas globales
Faker.seed(42)
random.seed(42)

# 3. Columnas requeridas:
# id, nombre, apellido, telefono, correo, contacto, status, propiedadesVendidas, balance

# 4. Selector de tipos de propiedad / sectores
PROPIEDADES = ["Apartamento", "Casa", "Oficina", "Local", "Lote", "Bodega"]

# 5. Tamaño del dataset
FILAS = 300


# 6. Generar N datos limpios
def generar_datos_limpios(numero_datos=FILAS):
    filas = []
    for _ in range(numero_datos):
        # 'activa' mapea directamente al campo 'status'
        activa = random.choice([True, False])
        # 'propiedad' mapea al campo 'propiedadesVendidas'
        propiedad = random.choice(PROPIEDADES)

        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.company(),
            "apellido": fake.last_name(),
            "telefono": fake.numerify("3#########"),
            "correo": fake.company_email(),
            "contacto": fake.name(),
            "status": activa,
            "propiedadesVendidas": propiedad,
            "balance": round(random.uniform(1000000.0, 500000000.0), 2)
        })
    return filas


# 7. Ensuciar los datos a propósito
def ensuciar_datos(filas):
    for row in filas:
        # Ensuciar 'nombre': 10% espacios sobrantes, 15% MAYÚSCULAS
        rand_nombre = random.random()
        if rand_nombre < 0.10:
            row["nombre"] = f"   {row['nombre']}   "
        elif rand_nombre < 0.25:  # 15% siguiente
            row["nombre"] = row["nombre"].upper()

        # Ensuciar 'contacto': 8% en None (nulos)
        if random.random() < 0.08:
            row["contacto"] = None

        # Ensuciar 'correo': 6% sin arroba (correo inválido)
        if random.random() < 0.06:
            row["correo"] = row["correo"].replace("@", "")

        # Ensuciar 'telefono': tres formatos mezclados
        rand_tel = random.random()
        tel_base = row["telefono"]
        if rand_tel < 0.33:
            row["telefono"] = tel_base  # '3001234567'
        elif rand_tel < 0.66:
            row["telefono"] = f"{tel_base[:3]} {tel_base[3:6]} {tel_base[6:]}"  # '300 123 4567'
        else:
            row["telefono"] = f"+57 {tel_base[:3]}-{tel_base[3:6]}-{tel_base[6:]}"  # '+57 300-123-4567'

        # Ensuciar 'status' ('estado'): a veces como texto ('SI', 'No', '1', '0')
        if random.random() < 0.20:
            row["status"] = random.choice(["SI", "No", "1", "0"])

    return filas


# 8. Función unificada que devuelve el DataFrame
def generar_vendedores(n=FILAS):
    # Fijar semillas internamente para asegurar reproductibilidad si se importa
    Faker.seed(42)
    random.seed(42)

    datos_limpios = generar_datos_limpios(n)
    datos_sucios = ensuciar_datos(datos_limpios)

    df = pd.DataFrame(datos_sucios)

    # 5% de duplicados exactos
    n_duplicados = int(n * 0.05)
    duplicados = df.sample(n=n_duplicados, random_state=42)
    df = pd.concat([df, duplicados], ignore_index=True)

    # Mezclar las filas para distribuir los duplicados
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    return df


# 9. Bloque __main__ exclusivo para revisión
if __name__ == "__main__":
    df = generar_vendedores(FILAS)

    print("--- Shape ---")
    print(df.shape)

    print("\n--- Head ---")
    print(df.head())

    print("\n--- Conteo de Nulos ---")
    print(df.isna().sum())