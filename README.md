# Proyecto integrador

Proyecto de simulación de datos para compradores, vendedores y administradores.

## Estructura

```text
.
├── src/
│   ├── simular_datos.py
│   ├── exportar_datos.py
│   ├── limpiar_datos.py
│   ├── consultas_datos.py
│   ├── reporte_datos.py
│   ├── simular_buyers.py
│   ├── simular_sellers.py
│   └── simular_Admin.py
├── data/
│   ├── exportar/
│   │   ├── compradores/compradores.csv
│   │   ├── vendedores/vendedores.csv
│   │   └── administradores/administradores.csv
│   ├── ensuciar/
│   │   ├── compradores/compradores_sucios.csv
│   │   ├── vendedores/vendedores_sucios.csv
│   │   └── administradores/administradores_sucios.csv
│   └── limpiar/
│       ├── compradores/compradores_limpios.csv
│       ├── vendedores/vendedores_limpios.csv
│       └── administradores/administradores_limpios.csv
├── reportes/
│   ├── compradores/
│   ├── vendedores/
│   └── administradores/
├── requirements.txt
└── README.md
```

Compradores, vendedores y administradores permanecen como datasets separados.
Los archivos de propiedades se conservan sin cambios en sus ubicaciones
originales.

## Preparación

Desde la carpeta del proyecto, crear y activar un entorno virtual e instalar las
dependencias:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Uso

Los scripts se pueden ejecutar desde la carpeta raíz del proyecto; las rutas de
entrada y salida se resuelven desde su ubicación y no dependen del directorio
actual de la terminal.

Para ejecutar todo el proceso con un solo comando desde la carpeta raíz:

```powershell
python src\main.py
```

`main.py` corre las seis etapas una después de otra y se detiene si alguna
falla. También podés ejecutar las etapas por separado:

```powershell
python src\simular_datos.py
python src\ensuciar_datos.py
python src\limpiar_datos.py
python src\consultas_datos.py
python src\reporte_datos.py
```

El paso de simulación crea los datos Faker base y los exporta a
`data/exportar/<entidad>/`. `ensuciar_datos.py` lee esos CSV y guarda los datos
con errores intencionales y duplicados en `data/ensuciar/<entidad>/`.
`limpiar_datos.py` escribe los resultados depurados en
`data/limpiar/<entidad>/`. Cada ejecución reemplaza los CSV generados en esas
rutas. Los datos sucios tienen 315 filas (300 originales y 15 duplicados); los
limpios conservan 300 IDs únicos por entidad. Los CSV previos en `data/crudo/`
y `data/limpio/`, si existen, no son usados por el nuevo pipeline.

Los reportes se separan por entidad y se vuelven a generar en cada ejecución:

- `reportes/compradores/balance.png`
- `reportes/compradores/estado_cuentas.png`
- `reportes/compradores/intereses.png`
- `reportes/vendedores/balance.png`
- `reportes/vendedores/estado_cuentas.png`
- `reportes/vendedores/propiedades_vendidas.png`
- `reportes/administradores/tipos_cantidad.png`
- `reportes/administradores/tipos_proporcion.png`
- `reportes/administradores/calidad_datos.png`

En total se generan tres gráficos por entidad. Cada ejecución de `main.py`
simula datos aleatorios nuevos; no hay una semilla fija. Los rangos, categorías
y cantidades de las gráficas se calculan desde los CSV limpios recién generados.

Los simuladores individuales `simular_buyers.py` y `simular_sellers.py` siguen
disponibles para generar/exportar y ensuciar solo su respectiva entidad. Sus
salidas se guardan en las mismas carpetas por función.

`simular_Admin.py` también se puede ejecutar por separado después de crear los
CSV exportados de compradores y vendedores; usa sus IDs para generar
administradores:

```powershell
python src\simular_Admin.py
```

## Datos de propiedades

El simulador, el exportador y los CSV relacionados con propiedades se dejaron
intactos, fuera de la reorganización solicitada.
