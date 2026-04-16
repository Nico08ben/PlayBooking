"""
Sistema de Gestión de Canchas Deportivas
Módulo de persistencia y datos iniciales.

Ejecutar directamente (python InfoMin.py) para regenerar datos.pkl desde cero.

Autores: Nicolás Armero Rosero, Santiago Andres Garcia Sanchez,
         Karen Juliana Dueñas, Sara Mesa Lenis
"""
import pickle
import os
from datetime import datetime

from ClasesHijasCancha import Futbol, Voley, Padel
from ClaseUsuario       import Usuario
from ClaseReserva       import Reserva

ARCHIVO = "datos.pkl"


def guardar(canchas, usuarios, reservas):
    datos = {
        "canchas":     canchas,
        "usuarios":    usuarios,
        "reservas":    reservas,
        "contador":    Reserva.contador_id,
        "guardado_en": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    try:
        with open(ARCHIVO, "wb") as f:
            pickle.dump(datos, f)
    except OSError as e:
        print(f"  ⚠ Error al guardar: {e}")


def cargar():
    if not os.path.exists(ARCHIVO):
        print("  ℹ️  No se encontró datos.pkl — cargando datos iniciales.")
        return _datos_iniciales()

    try:
        with open(ARCHIVO, "rb") as f:
            datos = pickle.load(f)
        Reserva.contador_id = datos.get("contador", 1)
        print(f"  ✅ Datos cargados (último guardado: {datos.get('guardado_en', 'desconocido')})")
        return datos["canchas"], datos["usuarios"], datos["reservas"]

    except (pickle.UnpicklingError, KeyError, EOFError) as e:
        print(f"  ⚠ Archivo corrupto ({e}). Cargando datos iniciales.")
        return _datos_iniciales()


def _datos_iniciales():
    Reserva.contador_id = 1 
    PRECIOS = {
        "Futbol11":    {"6-12":  80000, "13-17": 100000, "18-22": 130000, "finde": 140000},
        "Futbol5":     {"6-12":  90000, "13-17": 110000, "18-22": 140000, "finde": 150000},
        "Volleyball":  {"6-12":  50000, "13-17":  60000, "18-22":  80000, "finde":  90000},
        "Volleyplaya": {"6-12":  60000, "13-17":  70000, "18-22":  90000, "finde": 100000},
        "Padel":       {"6-12":  70000, "13-17":  90000, "18-22": 120000, "finde": 130000},
    }

    canchas = {
        "F1": Futbol("Cancha Sintético 1", "F1", "Sintético", 11, PRECIOS["Futbol11"],
                     "Cancha de césped sintético para fútbol 11"),
        "F2": Futbol("Cancha Sintético 2", "F2", "Sintético", 11, PRECIOS["Futbol11"],
                     "Cancha de césped sintético para fútbol 11"),
        "F3": Futbol("Cancha Sala 1",      "F3", "Sala",       5, PRECIOS["Futbol5"],
                     "Cancha techada de microfútbol (fútbol sala)"),
        "F4": Futbol("Cancha Sala 2",      "F4", "Sala",       5, PRECIOS["Futbol5"],
                     "Cancha techada de microfútbol (fútbol sala)"),
        "V1": Voley("Cancha Vóley Normal", "V1", "Normal",        PRECIOS["Volleyball"],
                    "Cancha de vóley sobre piso duro"),
        "V2": Voley("Cancha Vóley Playa",  "V2", "Playa",         PRECIOS["Volleyplaya"],
                    "Cancha de vóley playa sobre arena"),
        "P1": Padel("Cancha Pádel 1",      "P1", 4,               PRECIOS["Padel"],
                    "Cancha de pádel cerrada con muro de cristal"),
    }

    return canchas, {}, []


if __name__ == "__main__":
    respuesta = input("⚠  Esto borrará todos los datos existentes. ¿Continuar? (s/n): ").strip().lower()
    if respuesta != "s":
        print("Operación cancelada.")
    else:
        canchas, usuarios, reservas = _datos_iniciales()
        guardar(canchas, usuarios, reservas)
        print(f"✅ Base de datos inicial creada en '{ARCHIVO}'")
        print(f"   Canchas creadas: {len(canchas)}")