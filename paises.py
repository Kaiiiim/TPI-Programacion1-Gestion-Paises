"""Módulo con la lógica de gestión de países.

Contiene funciones para cargar/guardar el dataset, agregar, buscar, filtrar,
ordenar y calcular estadísticas sobre países. Cada función tiene una única
responsabilidad (modularización).
"""

import csv
import os
import unicodedata
from typing import List, Dict, Optional, Any


# ---------------------------------------------------------------------------
# Estructura de datos
# ---------------------------------------------------------------------------
# Un país se representa como un diccionario con las siguientes claves:
#   "nombre": str
#   "poblacion": int
#   "superficie": int   (en km²)
#   "continente": str
# El dataset completo es una lista de estos diccionarios.


CAMPOS_OBLIGATORIOS = ("nombre", "poblacion", "superficie", "continente")


# ---------------------------------------------------------------------------
# Normalización de texto
# ---------------------------------------------------------------------------

def normalizar_texto(texto: str) -> str:
    """Normaliza un texto: lo pasa a minúsculas y quita tildes/diacríticos.

    Útil para comparaciones insensibles a mayúsculas y acentos.
    """
    if texto is None:
        return ""
    texto = str(texto).lower()
    # Descompone caracteres acentuados (NFD) y elimina las marcas diacríticas
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto


# ---------------------------------------------------------------------------
# Validaciones
# ---------------------------------------------------------------------------

def validar_no_vacio(texto: str, campo: str = "valor") -> str:
    """Valida que un texto no esté vacío (ni solo espacios).

    Lanza ValueError si el texto es vacío.
    """
    if texto is None:
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    texto = texto.strip()
    if texto == "":
        raise ValueError(f"El campo '{campo}' no puede estar vacío.")
    return texto


def validar_entero_positivo(valor: Any, campo: str = "valor") -> int:
    """Valida y convierte un valor a entero positivo.

    Acepta str o int. Lanza ValueError si no es un entero válido o no es positivo.
    """
    if isinstance(valor, bool):
        raise ValueError(f"El campo '{campo}' debe ser un número entero.")
    if isinstance(valor, int):
        numero = valor
    else:
        texto = str(valor).strip()
        if texto == "":
            raise ValueError(f"El campo '{campo}' no puede estar vacío.")
        try:
            numero = int(texto)
        except (ValueError, TypeError):
            raise ValueError(f"El campo '{campo}' debe ser un número entero.")
    if numero <= 0:
        raise ValueError(f"El campo '{campo}' debe ser mayor que cero.")
    return numero


# ---------------------------------------------------------------------------
# Persistencia (CSV)
# ---------------------------------------------------------------------------

def cargar_paises(ruta: str) -> List[Dict]:
    """Carga el dataset de países desde un archivo CSV.

    Devuelve una lista de diccionarios. Si el archivo no existe o tiene
    errores de formato, se manejan de forma controlada y se devuelve la
    lista (posiblemente vacía) junto con un mensaje de advertencia.
    """
    paises: List[Dict] = []
    if not os.path.exists(ruta):
        print(f"Advertencia: el archivo '{ruta}' no existe. Se inicia con dataset vacío.")
        return paises

    try:
        with open(ruta, mode="r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)
            if lector.fieldnames is None:
                print("Advertencia: el CSV no tiene encabezado. Se inicia con dataset vacío.")
                return paises

            # Normalizar nombres de columnas (minúsculas y sin espacios)
            campos = [c.strip().lower() for c in lector.fieldnames]
            for campo in CAMPOS_OBLIGATORIOS:
                if campo not in campos:
                    print(f"Advertencia: falta la columna '{campo}' en el CSV. Se inicia con dataset vacío.")
                    return paises

            for numero_fila, fila in enumerate(lector, start=2):
                try:
                    nombre = validar_no_vacio(fila.get("nombre", ""), "nombre")
                    poblacion = validar_entero_positivo(fila.get("poblacion", ""), "poblacion")
                    superficie = validar_entero_positivo(fila.get("superficie", ""), "superficie")
                    continente = validar_no_vacio(fila.get("continente", ""), "continente")
                except ValueError as e:
                    print(f"Fila {numero_fila} ignorada por error de formato: {e}")
                    continue
                paises.append({
                    "nombre": nombre,
                    "poblacion": poblacion,
                    "superficie": superficie,
                    "continente": continente,
                })
    except (OSError, csv.Error) as e:
        print(f"Error al leer el archivo CSV: {e}")

    return paises


def guardar_paises(ruta: str, paises: List[Dict]) -> bool:
    """Guarda la lista de países en un archivo CSV.

    Devuelve True si se guardó correctamente, False en caso de error.
    """
    try:
        os.makedirs(os.path.dirname(ruta) or ".", exist_ok=True)
        with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=list(CAMPOS_OBLIGATORIOS))
            escritor.writeheader()
            for pais in paises:
                escritor.writerow(pais)
        return True
    except (OSError, csv.Error) as e:
        print(f"Error al guardar el archivo CSV: {e}")
        return False


# ---------------------------------------------------------------------------
# Creación y modificación
# ---------------------------------------------------------------------------

def crear_pais(nombre: str, poblacion: Any, superficie: Any, continente: str) -> Dict:
    """Crea y valida un diccionario que representa un país."""
    return {
        "nombre": validar_no_vacio(nombre, "nombre"),
        "poblacion": validar_entero_positivo(poblacion, "poblacion"),
        "superficie": validar_entero_positivo(superficie, "superficie"),
        "continente": validar_no_vacio(continente, "continente"),
    }


def agregar_pais(paises: List[Dict], pais: Dict) -> bool:
    """Agrega un país a la lista si no existe otro con el mismo nombre.

    La comparación de nombres es case-insensitive. Devuelve True si se agregó.
    """
    nombre_nuevo = pais["nombre"].lower()
    for existente in paises:
        if existente["nombre"].lower() == nombre_nuevo:
            print(f"Ya existe un país con el nombre '{pais['nombre']}'.")
            return False
    paises.append(pais)
    return True


def actualizar_pais(paises: List[Dict], nombre: str,
                    poblacion: Optional[Any] = None,
                    superficie: Optional[Any] = None) -> bool:
    """Actualiza la población y/o superficie de un país existente.

    Devuelve True si se actualizó, False si no se encontró el país.
    """
    nombre = validar_no_vacio(nombre, "nombre")
    for pais in paises:
        if pais["nombre"].lower() == nombre.lower():
            if poblacion is not None:
                pais["poblacion"] = validar_entero_positivo(poblacion, "poblacion")
            if superficie is not None:
                pais["superficie"] = validar_entero_positivo(superficie, "superficie")
            return True
    print(f"No se encontró el país '{nombre}'.")
    return False


# ---------------------------------------------------------------------------
# Búsquedas y filtros
# ---------------------------------------------------------------------------

def buscar_pais_por_nombre(paises: List[Dict], nombre: str,
                           exacto: bool = False) -> List[Dict]:
    """Busca países por nombre (ignorando tildes y mayúsculas).

    Si exacto=True, la coincidencia es exacta.
    Si exacto=False, se busca coincidencia parcial (contiene).
    """
    nombre_norm = normalizar_texto(validar_no_vacio(nombre, "nombre"))
    resultados = []
    for pais in paises:
        nombre_pais_norm = normalizar_texto(pais["nombre"])
        if exacto and nombre_pais_norm == nombre_norm:
            resultados.append(pais)
        elif (not exacto) and nombre_norm in nombre_pais_norm:
            resultados.append(pais)
    return resultados


def filtrar_por_continente(paises: List[Dict], continente: str) -> List[Dict]:
    """Filtra países por continente (ignorando tildes y mayúsculas).

    La coincidencia es parcial: "americ" encuentra "América".
    """
    continente_norm = normalizar_texto(validar_no_vacio(continente, "continente"))
    return [p for p in paises
            if continente_norm in normalizar_texto(p["continente"])]


def filtrar_por_rango_poblacion(paises: List[Dict], minimo: Any, maximo: Any) -> List[Dict]:
    """Filtra países cuya población esté dentro del rango [minimo, maximo]."""
    min_p = validar_entero_positivo(minimo, "poblacion mínima")
    max_p = validar_entero_positivo(maximo, "poblacion máxima")
    if min_p > max_p:
        min_p, max_p = max_p, min_p
    return [p for p in paises if min_p <= p["poblacion"] <= max_p]


def filtrar_por_rango_superficie(paises: List[Dict], minimo: Any, maximo: Any) -> List[Dict]:
    """Filtra países cuya superficie esté dentro del rango [minimo, maximo]."""
    min_s = validar_entero_positivo(minimo, "superficie mínima")
    max_s = validar_entero_positivo(maximo, "superficie máxima")
    if min_s > max_s:
        min_s, max_s = max_s, min_s
    return [p for p in paises if min_s <= p["superficie"] <= max_s]


# ---------------------------------------------------------------------------
# Ordenamientos
# ---------------------------------------------------------------------------

CLAVES_ORDEN_VALIDAS = ("nombre", "poblacion", "superficie", "continente")


def ordenar_paises(paises: List[Dict], clave: str = "nombre",
                   descendente: bool = False) -> List[Dict]:
    """Devuelve una nueva lista de países ordenada por la clave indicada.

    La lista original no se modifica. Claves válidas: nombre, poblacion,
    superficie, continente.
    """
    clave = clave.strip().lower()
    if clave not in CLAVES_ORDEN_VALIDAS:
        raise ValueError(f"Clave de ordenamiento inválida: '{clave}'. "
                         f"Opciones: {', '.join(CLAVES_ORDEN_VALIDAS)}.")
    # Copia para no mutar la lista original
    copia = list(paises)

    def clave_orden(pais):
        valor = pais[clave]
        # Si es texto, ordenar sin distinguir mayúsculas/minúsculas
        if isinstance(valor, str):
            return valor.lower()
        return valor

    copia.sort(key=clave_orden, reverse=descendente)
    return copia


# ---------------------------------------------------------------------------
# Estadísticas
# ---------------------------------------------------------------------------

def pais_mayor_poblacion(paises: List[Dict]) -> Optional[Dict]:
    """Devuelve el país con mayor población, o None si la lista está vacía."""
    if not paises:
        return None
    return max(paises, key=lambda p: p["poblacion"])


def pais_menor_poblacion(paises: List[Dict]) -> Optional[Dict]:
    """Devuelve el país con menor población, o None si la lista está vacía."""
    if not paises:
        return None
    return min(paises, key=lambda p: p["poblacion"])


def promedio_poblacion(paises: List[Dict]) -> float:
    """Calcula el promedio de población. Devuelve 0.0 si la lista está vacía."""
    if not paises:
        return 0.0
    return sum(p["poblacion"] for p in paises) / len(paises)


def promedio_superficie(paises: List[Dict]) -> float:
    """Calcula el promedio de superficie. Devuelve 0.0 si la lista está vacía."""
    if not paises:
        return 0.0
    return sum(p["superficie"] for p in paises) / len(paises)


def cantidad_por_continente(paises: List[Dict]) -> Dict[str, int]:
    """Devuelve un diccionario {continente: cantidad de países}."""
    resultado: Dict[str, int] = {}
    for pais in paises:
        cont = pais["continente"]
        resultado[cont] = resultado.get(cont, 0) + 1
    return resultado


# ---------------------------------------------------------------------------
# Presentación
# ---------------------------------------------------------------------------

def formatear_numero(numero: int) -> str:
    """Formatea un número con separador de miles."""
    return f"{numero:,}".replace(",", ".")


def mostrar_pais(pais: Dict) -> None:
    """Imprime los datos de un país de forma legible."""
    print(f"  - {pais['nombre']}: población={formatear_numero(pais['poblacion'])}, "
          f"superficie={formatear_numero(pais['superficie'])} km², "
          f"continente={pais['continente']}")


def mostrar_lista(paises: List[Dict], titulo: str = "Países") -> None:
    """Imprime una lista de países con un título."""
    print(f"\n--- {titulo} ({len(paises)}) ---")
    if not paises:
        print("  (sin resultados)")
        return
    for pais in paises:
        mostrar_pais(pais)
    print()
