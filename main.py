"""Punto de entrada de la aplicación de gestión de países.

Ofrece un menú interactivo en consola que permite agregar, actualizar,
buscar, filtrar, ordenar y analizar países a partir de un dataset CSV.
"""

import os
import sys

# Asegurar entrada/salida en UTF-8 (importante en Windows)
try:
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Permitir ejecutar desde cualquier directorio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cargar paises.py de forma robusta (independiente del directorio de trabajo)
import importlib.util as _ilu
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_paises_spec = _ilu.spec_from_file_location("paises", os.path.join(_BASE_DIR, "paises.py"))
_paises_mod = _ilu.module_from_spec(_paises_spec)
_paises_spec.loader.exec_module(_paises_mod)
for _name in dir(_paises_mod):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_paises_mod, _name)

RUTA_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "paises.csv")


def leer_texto(mensaje: str) -> str:
    """Lee un texto no vacío desde consola, validando la entrada."""
    while True:
        try:
            valor = input(mensaje)
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada.")
            return ""
        try:
            return validar_no_vacio(valor, "entrada")
        except ValueError as e:
            print(f"  Error: {e}")


def leer_entero(mensaje: str) -> int:
    """Lee un entero positivo desde consola, validando la entrada."""
    while True:
        try:
            valor = input(mensaje)
        except (EOFError, KeyboardInterrupt):
            print("\nOperación cancelada.")
            return 0
        try:
            return validar_entero_positivo(valor, "entrada")
        except ValueError as e:
            print(f"  Error: {e}")


def opcion_agregar(paises: list) -> None:
    print("\n--- Agregar país ---")
    nombre = leer_texto("Nombre del país: ")
    if not nombre:
        return
    try:
        poblacion = leer_entero("Población (entero positivo): ")
        if poblacion == 0:
            return
        superficie = leer_entero("Superficie en km² (entero positivo): ")
        if superficie == 0:
            return
        continente = leer_texto("Continente: ")
        if not continente:
            return
        pais = crear_pais(nombre, poblacion, superficie, continente)
    except ValueError as e:
        print(f"  Error al crear el país: {e}")
        return

    if agregar_pais(paises, pais):
        print(f"  País '{pais['nombre']}' agregado correctamente.")
        if guardar_paises(RUTA_CSV, paises):
            print("  Cambios guardados en el CSV.")
    else:
        print("  No se agregó el país.")


def opcion_actualizar(paises: list) -> None:
    print("\n--- Actualizar país ---")
    nombre = leer_texto("Nombre del país a actualizar: ")
    if not nombre:
        return
    resultados = buscar_pais_por_nombre(paises, nombre, exacto=True)
    if not resultados:
        # Intentar búsqueda parcial
        resultados = buscar_pais_por_nombre(paises, nombre, exacto=False)
        if not resultados:
            print(f"  No se encontró ningún país con el nombre '{nombre}'.")
            return
        if len(resultados) > 1:
            print("  Se encontraron varios países:")
            for p in resultados:
                print(f"    - {p['nombre']}")
            nombre = leer_texto("Indique el nombre exacto del país: ")
            if not nombre:
                return
            resultados = buscar_pais_por_nombre(paises, nombre, exacto=True)
            if not resultados:
                print("  No se encontró el país indicado.")
                return

    pais = resultados[0]
    print(f"  País seleccionado: {pais['nombre']} "
          f"(población={pais['poblacion']}, superficie={pais['superficie']})")

    actualizar_poblacion = leer_texto("¿Actualizar población? (s/n): ").lower()
    nueva_poblacion = None
    if actualizar_poblacion == "s":
        nueva_poblacion = leer_entero("Nueva población: ")
        if nueva_poblacion == 0:
            nueva_poblacion = None

    actualizar_superficie = leer_texto("¿Actualizar superficie? (s/n): ").lower()
    nueva_superficie = None
    if actualizar_superficie == "s":
        nueva_superficie = leer_entero("Nueva superficie en km²: ")
        if nueva_superficie == 0:
            nueva_superficie = None

    if nueva_poblacion is None and nueva_superficie is None:
        print("  No se realizaron cambios.")
        return

    try:
        if actualizar_pais(paises, pais["nombre"], nueva_poblacion, nueva_superficie):
            print("  País actualizado correctamente.")
            if guardar_paises(RUTA_CSV, paises):
                print("  Cambios guardados en el CSV.")
    except ValueError as e:
        print(f"  Error al actualizar: {e}")


def opcion_buscar(paises: list) -> None:
    print("\n--- Buscar país ---")
    nombre = leer_texto("Nombre (o parte del nombre) del país: ")
    if not nombre:
        return
    tipo = leer_texto("¿Coincidencia exacta? (s/n): ").lower()
    exacto = (tipo == "s")
    resultados = buscar_pais_por_nombre(paises, nombre, exacto=exacto)
    if resultados:
        mostrar_lista(resultados, "Resultados de búsqueda")
    else:
        print(f"  No se encontraron países que coincidan con '{nombre}'.")


def opcion_filtrar(paises: list) -> None:
    print("\n--- Filtrar países ---")
    print("  1. Por continente")
    print("  2. Por rango de población")
    print("  3. Por rango de superficie")
    opcion = leer_texto("Seleccione una opción: ")
    if opcion == "1":
        continente = leer_texto("Continente: ")
        if not continente:
            return
        try:
            resultados = filtrar_por_continente(paises, continente)
        except ValueError as e:
            print(f"  Error: {e}")
            return
        mostrar_lista(resultados, f"Países en {continente}")
    elif opcion == "2":
        minimo = leer_entero("Población mínima: ")
        if minimo == 0:
            return
        maximo = leer_entero("Población máxima: ")
        if maximo == 0:
            return
        try:
            resultados = filtrar_por_rango_poblacion(paises, minimo, maximo)
        except ValueError as e:
            print(f"  Error: {e}")
            return
        mostrar_lista(resultados, f"Países con población entre {minimo} y {maximo}")
    elif opcion == "3":
        minimo = leer_entero("Superficie mínima (km²): ")
        if minimo == 0:
            return
        maximo = leer_entero("Superficie máxima (km²): ")
        if maximo == 0:
            return
        try:
            resultados = filtrar_por_rango_superficie(paises, minimo, maximo)
        except ValueError as e:
            print(f"  Error: {e}")
            return
        mostrar_lista(resultados, f"Países con superficie entre {minimo} y {maximo} km²")
    else:
        print("  Opción inválida.")


def opcion_ordenar(paises: list) -> None:
    print("\n--- Ordenar países ---")
    print("  Claves disponibles: nombre, poblacion, superficie, continente")
    clave = leer_texto("Ordenar por: ")
    if not clave:
        return
    orden = leer_texto("¿Descendente? (s/n): ").lower()
    descendente = (orden == "s")
    try:
        resultados = ordenar_paises(paises, clave, descendente=descendente)
    except ValueError as e:
        print(f"  Error: {e}")
        return
    direccion = "descendente" if descendente else "ascendente"
    mostrar_lista(resultados, f"Países ordenados por {clave} ({direccion})")


def opcion_estadisticas(paises: list) -> None:
    print("\n--- Estadísticas ---")
    if not paises:
        print("  No hay países cargados.")
        return

    mayor = pais_mayor_poblacion(paises)
    menor = pais_menor_poblacion(paises)
    prom_pob = promedio_poblacion(paises)
    prom_sup = promedio_superficie(paises)
    por_continente = cantidad_por_continente(paises)

    print(f"  País con mayor población: {mayor['nombre']} "
          f"({mayor['poblacion']:,} habitantes)".replace(",", "."))
    print(f"  País con menor población: {menor['nombre']} "
          f"({menor['poblacion']:,} habitantes)".replace(",", "."))
    print(f"  Promedio de población: {prom_pob:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    print(f"  Promedio de superficie: {prom_sup:,.2f} km²".replace(",", "X").replace(".", ",").replace("X", "."))
    print("  Cantidad de países por continente:")
    for continente, cantidad in sorted(por_continente.items()):
        print(f"    - {continente}: {cantidad}")


def mostrar_menu() -> None:
    print("\n" + "=" * 50)
    print("  GESTIÓN DE PAÍSES - MENÚ PRINCIPAL")
    print("=" * 50)
    print("  1. Agregar país")
    print("  2. Actualizar país (población/superficie)")
    print("  3. Buscar país por nombre")
    print("  4. Filtrar países")
    print("  5. Ordenar países")
    print("  6. Mostrar estadísticas")
    print("  7. Listar todos los países")
    print("  8. Guardar y salir")
    print("=" * 50)


def main() -> None:
    print("Cargando dataset de países...")
    paises = cargar_paises(RUTA_CSV)
    print(f"Se cargaron {len(paises)} países desde '{RUTA_CSV}'.")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            opcion_agregar(paises)
        elif opcion == "2":
            opcion_actualizar(paises)
        elif opcion == "3":
            opcion_buscar(paises)
        elif opcion == "4":
            opcion_filtrar(paises)
        elif opcion == "5":
            opcion_ordenar(paises)
        elif opcion == "6":
            opcion_estadisticas(paises)
        elif opcion == "7":
            mostrar_lista(paises, "Todos los países")
        elif opcion == "8":
            if guardar_paises(RUTA_CSV, paises):
                print("Datos guardados. ¡Hasta luego!")
            else:
                print("No se pudieron guardar los datos.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
