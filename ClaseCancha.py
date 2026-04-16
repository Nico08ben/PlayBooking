"""
Sistema de Gestión de Canchas Deportivas
Clase base: Cancha
Autores: Nicolás Armero Rosero, Santiago Andres Garcia Sanchez,
         Karen Juliana Dueñas, Sara Mesa Lenis
"""
from datetime import datetime


class Cancha:
    HORA_APERTURA = 6
    HORA_CIERRE   = 23

    def __init__(self, nombre, id_cancha, precio_hora, descripcion=""):
        self.__nombre      = nombre
        self.__id          = id_cancha
        self.__precio_hora = precio_hora
        self.__descripcion = descripcion
        self.__activa      = True

    def get_id(self):          return self.__id
    def get_nombre(self):      return self.__nombre
    def get_precio_hora(self): return self.__precio_hora
    def get_descripcion(self): return self.__descripcion
    def get_activa(self):       return self.__activa

    def desactivar(self): self.__activa = False
    def activar(self):    self.__activa = True

    def get_precio_franja(self, hora):
        if 6 <= hora < 14:
            return self.__precio_hora.get("6-12", 0)
        elif 14 <= hora < 18:
            return self.__precio_hora.get("13-17", 0)
        else:
            return self.__precio_hora.get("18-22", 0)

    def calcular_costo(self, hora_inicio, duracion, fecha):
        try:
            dia_semana = datetime.strptime(fecha, "%Y-%m-%d").weekday()
            es_finde   = dia_semana >= 5
        except ValueError:
            es_finde = False

        costo_total = 0
        for h in range(hora_inicio, hora_inicio + duracion):
            if es_finde and "finde" in self.__precio_hora:
                costo_total += self.__precio_hora["finde"]
            else:
                costo_total += self.get_precio_franja(h % 24)
        return costo_total

    def precio_resumen(self):
        p = self.__precio_hora
        lineas = []
        if "6-12"  in p: lineas.append(f"Mañana (06-12h):  ${p['6-12']:>9,}")
        if "13-17" in p: lineas.append(f"Tarde  (13-17h):  ${p['13-17']:>9,}")
        if "18-22" in p: lineas.append(f"Noche  (18-22h):  ${p['18-22']:>9,}")
        if "finde"  in p: lineas.append(f"Fin de semana:    ${p['finde']:>9,}")
        return " | ".join(lineas)

    def mostrar_informacion(self):
        estado = "✅ ACTIVA" if self.__activa else "❌ INACTIVA"
        return (f"[{self.__id}] {self.__nombre}  [{estado}]\n"
                f"       {self.__descripcion}\n"
                f"       Precios/hr: {self.precio_resumen()}")

    def to_dict(self):
        return {
            "id":          self.__id,
            "nombre":      self.__nombre,
            "descripcion": self.__descripcion,
            "precio_hora": self.__precio_hora,
            "activa":      self.__activa,
            "tipo":        self.__class__.__name__,
        }