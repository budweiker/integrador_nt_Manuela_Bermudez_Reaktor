import pandas as pd
from notebook.simulaciones.simular_properties import generar_datos_limpios, ensuciar
from notebook.exportaciones.exportar_properties import exportar_properties_crudos
print ("************ SIMULACION DE PROPIEDADES ************")
propiedades_df = generar_datos_limpios()
propiedades_sucias_df = ensuciar(propiedades_df)
print(propiedades_sucias_df)

print("************ EXPORTACION DE PROPIEDADES ************")
rutas_crudas = exportar_properties_crudos(propiedades_sucias_df)
for ruta in rutas_crudas:
    print(f"Archivo exportado: {ruta}")