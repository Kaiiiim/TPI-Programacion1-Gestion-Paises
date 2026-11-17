# Trabajo Práctico Integrador (TPI) - Tecnicatura Universitaria en Programación a Distancia.

Aplicación en consola que permite gestionar información sobre países a partir de un
dataset en formato CSV, aplicando listas, diccionarios, funciones, estructuras
condicionales y repetitivas, ordenamientos, filtros y estadísticas.

## Integrantes

- Kevin Ibáñez
- Selene Carrascosa

## Estructura del proyecto

```
.
├── main.py               # Punto de entrada: menú interactivo
├── paises.py             # Lógica de gestión de países (funciones)
├── data/
│   └── paises.csv        # Dataset base de países
├── informe.pdf           # Documentación académica y técnica
└── README.md
```

## Requisitos

- Python 3.x

No se requieren librerías externas.

## Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

En Windows también puede usarse:

```bash
py main.py
```

## Funcionalidades

El menú ofrece las siguientes opciones:

1. **Agregar país**: solicita nombre, población, superficie (km²) y continente.
   No se permiten campos vacíos ni valores no positivos.
2. **Actualizar país**: permite modificar la población y/o la superficie de un país
   existente.
3. **Buscar país por nombre**: coincidencia exacta o parcial (contiene).
4. **Filtrar países**: por continente, por rango de población o por rango de superficie.
5. **Ordenar países**: por nombre, población, superficie o continente, en orden
   ascendente o descendente.
6. **Mostrar estadísticas**: país con mayor y menor población, promedio de población,
   promedio de superficie y cantidad de países por continente.
7. **Listar todos los países**.
8. **Guardar y salir**: persiste los cambios en `data/paises.csv`.

## Dataset (CSV)

Archivo `data/paises.csv` con las columnas:

| Columna    | Tipo   | Descripción              |
|------------|--------|--------------------------|
| nombre     | string | Nombre del país          |
| poblacion  | int    | Población (habitantes)   |
| superficie | int    | Superficie (km²)         |
| continente | string | Continente               |

Ejemplo de registro:

```
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
```

## Ejemplos de uso

### Agregar un país

```
Seleccione una opción: 1
Nombre del país: Chile
Población (entero positivo): 19116201
Superficie en km² (entero positivo): 756102
Continente: América
  País 'Chile' agregado correctamente.
  Cambios guardados en el CSV.
```

### Buscar un país

```
Seleccione una opción: 3
Nombre (o parte del nombre) del país: arg
¿Coincidencia exacta? (s/n): n
--- Resultados de búsqueda (1) ---
  - Argentina: población=45.376.763, superficie=2.780.400 km², continente=América
```

### Estadísticas

```
Seleccione una opción: 6
--- Estadísticas ---
  País con mayor población: India (1.380.004.385 habitantes)
  País con menor población: Australia (25.687.041 habitantes)
  Promedio de población: 223.289.732,00
  Promedio de superficie: 3.497.657,60 km²
  Cantidad de países por continente:
    - América: 3
    - Asia: 2
    - Europa: 3
    - Oceanía: 1
    - África: 1
```

## Validaciones y manejo de errores

- Campos vacíos no se aceptan.
- Población y superficie deben ser enteros positivos.
- Filtrar por continente inexistente devuelve lista vacía con mensaje claro.
- Búsquedas sin resultados muestran mensaje informativo.
- Errores de formato en el CSV se reportan fila por fila sin detener la carga.
- El programa no falla ante entradas inválidas; vuelve a solicitar el dato.

## Documentación

La documentación académica y técnica se encuentra en `informe.pdf` (raíz del proyecto).

## Enlaces

- Repositorio en GitHub: https://github.com/Kaiiiim/TPI-Programacion1-Gestion-Paises
- Documentación en PDF: `./informe.pdf`
- Video demostrativo: [COMPLETAR: Link público de YouTube/Drive]

## Licencia

Proyecto académico - uso educativo.
