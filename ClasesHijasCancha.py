"""
Sistema de Gestión de Canchas Deportivas
Subclases de Cancha: Futbol, Voley, Padel
Autores: Nicolás Armero Rosero, Santiago Andres Garcia Sanchez,
         Karen Juliana Dueñas, Sara Mesa Lenis
"""
from ClaseCancha import Cancha


class Futbol(Cancha):
    TIPOS_VALIDOS = ("Sintético", "Sala", "Natural")

    def __init__(self, nombre, id_cancha, tipo_cancha, jugadores, precio_hora, descripcion=""):
        if tipo_cancha not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de cancha inválido. Opciones: {self.TIPOS_VALIDOS}")
        if jugadores not in (5, 7, 9, 11):
            raise ValueError("Número de jugadores inválido. Opciones: 5, 7, 9 u 11.")
        super().__init__(nombre, id_cancha, precio_hora, descripcion)
        self.tipo_cancha = tipo_cancha
        self.jugadores   = jugadores

    def get_tipo(self):      return self.tipo_cancha
    def get_jugadores(self): return self.jugadores

    def mostrar_informacion(self):
        base = super().mostrar_informacion()
        return (f"{base}\n"
                f"       ⚽ Fútbol {self.tipo_cancha} — {self.jugadores}v{self.jugadores}\n"
                f"       Incluye: cancha y balón")

    def to_dict(self):
        d = super().to_dict()
        d.update({"tipo_cancha": self.tipo_cancha, "jugadores": self.jugadores})
        return d


class Voley(Cancha):
    TIPOS_VALIDOS = ("Normal", "Playa")

    def __init__(self, nombre, id_cancha, tipo_cancha, precio_hora, descripcion=""):
        if tipo_cancha not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo inválido. Opciones: {self.TIPOS_VALIDOS}")
        super().__init__(nombre, id_cancha, precio_hora, descripcion)
        self.tipo_cancha = tipo_cancha

    def get_tipo(self): return self.tipo_cancha

    def mostrar_informacion(self):
        base = super().mostrar_informacion()
        return (f"{base}\n"
                f"       🏐 Vóley {self.tipo_cancha}\n"
                f"       Incluye: cancha y balón")

    def to_dict(self):
        d = super().to_dict()
        d["tipo_cancha"] = self.tipo_cancha
        return d


class Padel(Cancha):
    JUGADORES_VALIDOS = (2, 4)

    def __init__(self, nombre, id_cancha, jugadores, precio_hora, descripcion=""):
        if jugadores not in self.JUGADORES_VALIDOS:
            raise ValueError(f"Número de jugadores inválido. Opciones: {self.JUGADORES_VALIDOS}")
        super().__init__(nombre, id_cancha, precio_hora, descripcion)
        self.jugadores = jugadores

    def get_jugadores(self): return self.jugadores

    def mostrar_informacion(self):
        base = super().mostrar_informacion()
        return (f"{base}\n"
                f"       🎾 Pádel — {self.jugadores} jugadores\n"
                f"       Incluye: cancha, raquetas y pelota")

    def to_dict(self):
        d = super().to_dict()
        d["jugadores"] = self.jugadores
        return d