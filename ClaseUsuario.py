"""
Sistema de Gestión de Canchas Deportivas
Clase: Usuario
Autores: Nicolás Armero Rosero, Santiago Andres Garcia Sanchez,
         Karen Juliana Dueñas, Sara Mesa Lenis
"""
import re
from datetime import datetime


class Usuario:
    def __init__(self, cedula, nombre, apellido, numero, email=""):
        self.__cedula         = cedula.strip()
        self.__nombre         = nombre.strip().title()
        self.__apellido       = apellido.strip().title()
        self.__numero         = numero.strip()
        self.__email          = email.strip().lower()
        self.__registrado     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__total_reservas = 0

    def get_cedula(self):          return self.__cedula
    def get_nombre(self):          return f"{self.__nombre} {self.__apellido}"
    def get_nombre_solo(self):     return self.__nombre
    def get_apellido(self):        return self.__apellido
    def get_numero(self):          return self.__numero
    def get_email(self):           return self.__email
    def get_registrado(self):      return self.__registrado
    def get_total_reservas(self):  return self.__total_reservas

    def incrementar_reservas(self):
        self.__total_reservas += 1

    def decrementar_reservas(self):
        if self.__total_reservas > 0:
            self.__total_reservas -= 1

    def mostrar_informacion(self):
        email_str = f"  | 📧 {self.__email}" if self.__email else ""
        return (f"👤 {self.get_nombre():<30}"
                f"  | 🪪 {self.__cedula}"
                f"  | 📱 {self.__numero}"
                f"{email_str}"
                f"  | 🎫 Reservas: {self.__total_reservas}")

    def to_dict(self):
        return {
            "cedula":         self.__cedula,
            "nombre":         self.__nombre,
            "apellido":       self.__apellido,
            "numero":         self.__numero,
            "email":          self.__email,
            "registrado":     self.__registrado,
            "total_reservas": self.__total_reservas,
        }

    def __eq__(self, other):
        return isinstance(other, Usuario) and self.__cedula == other.get_cedula()


# ── Validaciones como funciones del módulo ────────────────────────────────────

def cedula_valida(cedula):
    """Cédula colombiana: solo dígitos, entre 8 y 10 caracteres."""
    c = cedula.strip()
    return c.isdigit() and 8 <= len(c) <= 10


def valida_tel(tel):
    """
    Teléfono colombiano de 10 dígitos.
    Acepta prefijo +57 o 57. Debe comenzar en 3 (celular) o 6 (fijo).
    """
    limpio = re.sub(r"\D", "", tel.strip().replace("+", ""))
    if limpio.startswith("57") and len(limpio) == 12:
        limpio = limpio[2:]
    return len(limpio) == 10 and limpio[0] in ("3", "6")


def email_valido(email):
    """Vacío se permite. Si tiene valor, valida el formato."""
    if email.strip() == "":
        return True
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()) is not None