# Informe Académico y Técnico

## Trabajo Práctico Integrador (TPI)

### Gestión de Datos de Países en Python: filtros, ordenamientos y estadísticas

---

## Carátula

- Institución: Universidad Tecnológica Nacional (UTN) - Facultad Regional Mendoza
- Carrera: Tecnicatura Universitaria en Programación a Distancia
- Materia: Programación 1
- Título: Gestión de Datos de Países en Python: filtros, ordenamientos y estadísticas
- Integrantes: Kevin Ibáñez - Selene Carrascosa
- Fecha de entrega: 17 de noviembre de 2026

---

## Índice

1. Objetivo
2. Dominio del problema
3. Marco Teórico
   3.1 Listas
   3.2 Diccionarios
   3.3 Funciones
   3.4 Estructuras condicionales y repetitivas
   3.5 Archivos CSV con codificación UTF-8
   3.6 Ordenamientos sin modificar la lista original
   3.7 Estadísticas básicas
4. Requerimientos técnicos
5. Diseño y arquitectura
6. Decisiones técnicas
7. Validaciones y manejo de errores
8. Funcionalidades implementadas
9. Dificultades y conclusiones
10. Bibliografía / Webgrafía
11. Enlaces del Proyecto

---

## 1. Objetivo

El objetivo de este trabajo es desarrollar una aplicación en Python que permita gestionar
información sobre países, aplicando listas, diccionarios, funciones, estructuras
condicionales y repetitivas, ordenamientos y estadísticas. El sistema debe ser capaz de
leer datos desde un archivo CSV, realizar consultas sobre esos datos y generar
indicadores clave a partir del dataset. Más allá de cumplir con las funcionalidades
pedidas, el objetivo principal es afianzar el uso de las estructuras de datos, la
modularización del código mediante funciones y las técnicas de filtrado y
ordenamiento, poniendo en práctica los conceptos aprendidos a lo largo de la materia
Programación 1.

## 2. Dominio del problema

El dominio de nuestro proyecto es la gestión de datos de países. Cada país se describe
mediante cuatro atributos: el nombre (texto), la población (número entero), la
superficie en kilómetros cuadrados (número entero) y el continente al que pertenece
(texto). El dataset base se guarda en un archivo CSV con las columnas
nombre,poblacion,superficie,continente, y la aplicación permite agregar, actualizar,
buscar, filtrar y ordenar países, además de calcular estadísticas generales sobre el
conjunto de datos.

## 3. Marco Teórico

### 3.1 Listas

Una lista en Python es una estructura de datos ordenada y mutable que permite
almacenar una colección de elementos. En nuestro proyecto utilizamos una lista
principal llamada paises, donde cada elemento es un diccionario que representa un
país. Las listas nos permiten agregar nuevos países, recorrerlos para mostrarlos,
filtrarlos y ordenarlos. Trabajamos siempre sobre copias de la lista cuando queremos
ordenar, para no perder el orden original de los datos.

### 3.2 Diccionarios

Un diccionario es una estructura de datos que almacena información en pares
clave-valor. En nuestro proyecto cada país se representa como un diccionario con las
claves nombre, poblacion, superficie y continente. Esta forma de representar
los datos nos resulta muy cómoda porque nos permite acceder a cada atributo por su
nombre en lugar de usar índices numéricos, y además facilita la lectura y escritura
del archivo CSV, ya que las claves coinciden con los nombres de las columnas.

### 3.3 Funciones

Las funciones son bloques de código reutilizables que realizan una tarea específica.
En nuestro proyecto aplicamos el principio de que cada función tenga una única
responsabilidad: hay funciones para validar entradas, para cargar y guardar el CSV,
para agregar y actualizar países, para buscar, filtrar y ordenar, y para calcular
estadísticas. Dividimos el código en dos módulos: paises.py, donde vive toda la
lógica del negocio, y main.py, que se encarga únicamente de la interacción con el
usuario a través del menú. Esta separación hace que el código sea más fácil de leer,
modificar y probar.

### 3.4 Estructuras condicionales y repetitivas

Las estructuras condicionales (if, elif, else) las usamos para validar las
opciones del menú, comprobar que los datos ingresados sean correctos y decidir qué
mensaje mostrar al usuario. Las estructuras repetitivas (while y for) las usamos
para el bucle principal del menú, que se repite hasta que el usuario elige salir, y
para recorrer la lista de países en las búsquedas, filtros y estadísticas. Juntas
permiten que el programa sea interactivo y procese todos los registros del dataset.

### 3.5 Archivos CSV con codificación UTF-8

El formato CSV (valores separados por comas) es el que usamos para persistir el
dataset. Python ofrece el módulo csv, que nos permite leer y escribir estos archivos
de forma segura. Para la lectura usamos csv.DictReader, que convierte cada fila en
un diccionario usando el encabezado como claves, y para la escritura usamos
csv.DictWriter. Elegimos la codificación UTF-8 para que los nombres de países y
continentes con tildes o caracteres especiales (como "América" o "Japón") se guarden
y lean correctamente sin perder información.

### 3.6 Ordenamientos sin modificar la lista original

Para ordenar los países utilizamos el método sort() con un parámetro key que
indica por qué atributo ordenar (nombre, población, superficie o continente) y
reverse para definir si el orden es ascendente o descendente. Una decisión
importante que tomamos fue trabajar sobre una copia de la lista (list(paises))
antes de ordenar, de manera que el orden original del dataset no se vea alterado.
Además, al ordenar texto lo hacemos convirtiendo a minúsculas, para que las
mayúsculas no afecten el resultado.

### 3.7 Estadísticas básicas

Las estadísticas se calculan recorriendo la lista de países. Usamos las funciones
integradas max y min con un key sobre la población para encontrar el país con
mayor y menor población. El promedio de población y de superficie se obtiene sumando
todos los valores y dividiendo por la cantidad de países. Para la cantidad de países
por continente usamos un diccionario acumulador: recorremos la lista y vamos
sumando uno por cada país según su continente. Estos indicadores dan un resumen
rápido del dataset.

## 4. Requerimientos técnicos

- Lenguaje: Python 3.x, utilizando únicamente la biblioteca estándar.
- Código claro, comentado y modularizado, con una función por responsabilidad.
- Validación de entradas y manejo básico de errores.
- Lectura y escritura de archivos CSV.
- Estructuras de datos principales: listas y diccionarios.

## 5. Diseño y arquitectura

El proyecto se organiza en dos módulos principales. paises.py contiene toda la
lógica de negocio: validaciones, carga y guardado del CSV, creación, actualización,
búsqueda, filtrado, ordenamiento y estadísticas. main.py contiene el menú
interactivo y se encarga de pedir datos al usuario, mostrar resultados y llamar a las
funciones del módulo de lógica. Esta separación nos permite mantener el código ordenado
y facilita futuras modificaciones.

[INSERTAR IMAGEN: diagrama_flujo.png]

El flujo general del programa es: al iniciar se carga el CSV en una lista de países,
luego se muestra un menú con las opciones disponibles y, según la elección del
usuario, se realizan las operaciones correspondientes. Los cambios se guardan en el
CSV cada vez que se agrega o actualiza un país.

[INSERTAR CAPTURAS DE CONSOLA]

## 6. Decisiones técnicas

- Separación en módulos: dividimos la lógica (paises.py) de la interfaz
  (main.py) para que el código sea más mantenible y fácil de probar.
- Validación centralizada: creamos funciones reutilizables para validar textos no
  vacíos y números enteros positivos, que se usan en todas las operaciones.
- Persistencia inmediata: guardamos el CSV tras cada alta o actualización para
  evitar pérdida de datos.
- No mutación en ordenamientos: ordenamos una copia de la lista para conservar el
  orden original del dataset.
- Búsqueda flexible: permitimos coincidencia exacta o parcial, ignorando tildes y
  mayúsculas para que el usuario no tenga que escribir el nombre perfecto.
- Manejo de errores de CSV: las filas con formato inválido se reportan y se
  omiten sin detener la carga del resto.
- Normalización de texto: usamos unicodedata para quitar acentos en las
  comparaciones, lo que hace la búsqueda y el filtrado más tolerantes.

## 7. Validaciones y manejo de errores

- Los campos vacíos no se aceptan; el programa vuelve a solicitar el dato.
- La población y la superficie deben ser números enteros positivos.
- Filtrar por un continente inexistente devuelve una lista vacía con un mensaje claro.
- Las búsquedas sin resultados muestran un mensaje informativo.
- Los errores de formato en el CSV se reportan fila por fila sin detener la carga.
- El programa no se rompe ante entradas inválidas; vuelve a pedir el dato.

## 8. Funcionalidades implementadas

- Agregar un país con todos los datos necesarios (sin campos vacíos).
- Actualizar los datos de población y superficie de un país existente.
- Buscar un país por nombre con coincidencia parcial o exacta.
- Filtrar países por continente, por rango de población y por rango de superficie.
- Ordenar países por nombre, población, superficie o continente, en orden ascendente
  o descendente.
- Mostrar estadísticas: país con mayor y menor población, promedio de población,
  promedio de superficie y cantidad de países por continente.
- Persistencia de los datos en el archivo CSV.

## 9. Dificultades y conclusiones

Durante el desarrollo nos encontramos con varios problemas que tuvimos que resolver.
El primero fue el manejo de la codificación en Windows: la consola utiliza cp1252 por
defecto, lo que provocaba caracteres extraños al mostrar tildes o nombres como
"América" o "Japón". Lo resolvimos reconfigurando la entrada y salida estándar a
UTF-8 al inicio del programa. El segundo problema fue la validación del CSV: algunas
filas podían tener formatos inválidos, así que implementamos un manejo fila por fila
que reporta el error y continúa con el resto, evitando que un solo dato malo impida
cargar todo el dataset. El tercer inconveniente fue la comparación de textos con
tildes: al buscar "japon" no encontraba "Japón", por lo que aplicamos una
normalización con unicodedata para quitar acentos en las comparaciones. Aprendimos
a estructurar mejor el código separando la lógica de la interfaz, a validar entradas
de forma robusta y a manejar archivos con distintas codificaciones. En conclusión,
este trabajo nos permitió afianzar el uso de listas y diccionarios, la modularización
mediante funciones y las técnicas de filtrado y ordenamiento, que son la base para
proyectos más complejos.

## 10. Bibliografía / Webgrafía

- Documentación oficial de Python: https://docs.python.org/3/
- Módulo csv: https://docs.python.org/3/library/csv.html
- Funciones integradas (max, min, sorted): https://docs.python.org/3/library/functions.html
- unicodedata: https://docs.python.org/3/library/unicodedata.html
- PEP 8 - Guía de estilo: https://peps.python.org/pep-0008/

## 11. Enlaces del Proyecto

- Repositorio en GitHub: https://github.com/Kaiiiim/TPI-Programacion1-Gestion-Paises
- Video demostrativo: [COMPLETAR: Link al video]
