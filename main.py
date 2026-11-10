import pandas as pd
from src.exportaciones.exportar_seller import exportar_sellers_crudos
from src.simulaciones.simular_sellers import generar_datos_limpios, ensuciar
from src.simulaciones.simular_buyers import generar_datos_limpios, ensuciar
#from src.simulaciones.simular_admin import 
from src.simulaciones.simular_properties import generar_datos_limpios, ensuciar
from src.exportaciones.exportar_properties import exportar_properties_crudos
print ("************ SIMULACION DE VENDEDORES ************")
vendedores_df = generar_datos_limpios()
vendedores_sucios_df = ensuciar(vendedores_df)
print(vendedores_sucios_df)

print("************ EXPORTACION DE VENDEDORES ************")
rutas_crudas = exportar_sellers_crudos(vendedores_sucios_df)
for ruta in rutas_crudas:
    print(f"Archivo exportado: {ruta}")

print ("************ SIMULACION DE PROPIEDADES ************")
propiedades_df = generar_datos_limpios()
propiedades_sucias_df = ensuciar(propiedades_df)
print(propiedades_sucias_df)

print("************ EXPORTACION DE PROPIEDADES ************")
rutas_crudas = exportar_properties_crudos(propiedades_sucias_df)
for ruta in rutas_crudas:
    print(f"Archivo exportado: {ruta}")