import pandas as pd
from src.simulaciones import (
    simular_sellers,
    simular_properties,
    simular_buyer,
    simular_admin,
)
from src.exportaciones.exportar_seller import exportar_sellers_crudos
from src.exportaciones.exportar_properties import exportar_properties_crudos
from src.exportaciones.exportar_buyer import exportar_buyers_crudos
from src.exportaciones.exportar_admin import exportar_admin_crudos
print ("************ SIMULACION DE VENDEDORES ************")
vendedores_df = simular_sellers.generar_datos_limpios()
vendedores_sucios_df = simular_sellers.ensuciar(vendedores_df)
print(vendedores_sucios_df)

print("************ EXPORTACION DE VENDEDORES ************")
rutas_crudas = exportar_sellers_crudos(vendedores_sucios_df)
for ruta in rutas_crudas:
    print(f"Archivo exportado: {ruta}")

print ("************ SIMULACION DE PROPIEDADES ************")
propiedades_df = simular_properties.generar_datos_limpios()
propiedades_sucias_df = simular_properties.ensuciar(propiedades_df)
print(propiedades_sucias_df)

print("************ EXPORTACION DE PROPIEDADES ************")
rutas_crudas = exportar_properties_crudos(propiedades_sucias_df)
for ruta in rutas_crudas:
    print(f"Archivo exportado: {ruta}")

print ("************ SIMULACION DE COMPRADORES ************")
compradores_df = simular_buyer.generar_datos_limpios(df_propiedades=propiedades_df)
compradores_sucios_df = simular_buyer.ensuciar(compradores_df)
print(compradores_sucios_df)

print("************ EXPORTACION DE COMPRADORES ************")
rutas_crudas = exportar_buyers_crudos(compradores_sucios_df)
for ruta in rutas_crudas:
    print(f"Archivo exportado: {ruta}")

print ("************ SIMULACION DE ADMINISTRADORES ************")
administradores_df = simular_admin.generar_datos_limpios()
administradores_sucios_df = simular_admin.ensuciar(administradores_df)
print(administradores_sucios_df)

print("************ EXPORTACION DE ADMINISTRADORES ************")
rutas_crudas = exportar_admin_crudos(administradores_sucios_df)
for ruta in rutas_crudas:
    print(f"Archivo exportado: {ruta}")

