"""
Sistema de Gestión de Canchas Deportivas
Clase: Reserva
Autores: Nicolás Armero Rosero, Santiago Andres Garcia Sanchez,
         Karen Juliana Dueñas, Sara Mesa Lenis
"""
from datetime import datetime, date

HORAS_MIN_CANCELACION = 2


class Reserva:
    contador_id = 1

    def __init__(self, usuario, cancha, fecha, hora_inicio, duracion):
        if not isinstance(hora_inicio, int) or not (6 <= hora_inicio <= 22):
            raise ValueError("La hora de inicio debe estar entre 6 y 22.")
        if not isinstance(duracion, int) or not (1 <= duracion <= 8):
            raise ValueError("La duración debe ser entre 1 y 8 horas.")
        if hora_inicio + duracion > 23:
            raise ValueError("La reserva no puede terminar después de las 23:00.")

        self.__id          = Reserva.contador_id
        Reserva.contador_id += 1

        self.__usuario      = usuario
        self.__cancha       = cancha
        self.__fecha        = fecha
        self.__hora_inicio  = hora_inicio
        self.__duracion     = duracion
        self.__activa       = True
        self.__creada_en    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__cancelada_en = None

    def get_id(self):           return self.__id
    def get_usuario(self):      return self.__usuario
    def get_cancha(self):       return self.__cancha
    def get_fecha(self):        return self.__fecha
    def get_hora_inicio(self):  return self.__hora_inicio
    def get_hora_fin(self):     return self.__hora_inicio + self.__duracion
    def get_duracion(self):     return self.__duracion
    def get_activa(self):       return self.__activa
    def get_creada_en(self):    return self.__creada_en
    def get_cancelada_en(self): return self.__cancelada_en

    def get_costo_total(self):
        return self.__cancha.calcular_costo(
            self.__hora_inicio, self.__duracion, self.__fecha
        )

    def es_futura(self):
        try:
            return datetime.strptime(self.__fecha, "%Y-%m-%d").date() >= date.today()
        except ValueError:
            return False

    def puede_cancelarse(self):
        if not self.__activa:
            return False, "La reserva ya está cancelada."
        try:
            inicio_dt = datetime.strptime(
                f"{self.__fecha} {self.__hora_inicio:02d}:00", "%Y-%m-%d %H:%M"
            )
        except ValueError:
            return False, "Fecha inválida en la reserva."

        horas_restantes = (inicio_dt - datetime.now()).total_seconds() / 3600

        if horas_restantes < 0:
            return False, "No se puede cancelar una reserva que ya transcurrió."
        if horas_restantes < HORAS_MIN_CANCELACION:
            return (
                False,
                f"Solo se puede cancelar con al menos {HORAS_MIN_CANCELACION}h de anticipación "
                f"(quedan {horas_restantes:.1f}h)."
            )
        return True, ""

    def cancelar(self):
        puede, motivo = self.puede_cancelarse()
        if not puede:
            raise ValueError(motivo)
        self.__activa       = False
        self.__cancelada_en = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__usuario.decrementar_reservas()

    def choca_con(self, otra):
        if self.__cancha.get_id() != otra.get_cancha().get_id():
            return False
        if self.__fecha != otra.get_fecha():
            return False
        return (self.__hora_inicio < otra.get_hora_fin() and
                otra.get_hora_inicio() < self.get_hora_fin())

    def mostrar_informacion(self):
        estado = "✅ ACTIVA" if self.__activa else "❌ CANCELADA"
        futuro = "📅 (próxima)" if self.es_futura() else "📆 (pasada)"
        lineas = [
            f"Reserva #{self.__id:03d}  [{estado}]  {futuro}",
            f"  Cancha  : {self.__cancha.get_nombre()}",
            f"  Usuario : {self.__usuario.get_nombre()} ({self.__usuario.get_numero()})",
            f"  Fecha   : {self.__fecha}",
            f"  Horario : {self.__hora_inicio:02d}:00 — {self.get_hora_fin():02d}:00  ({self.__duracion}h)",
            f"  Costo   : ${self.get_costo_total():,}",
            f"  Creada  : {self.__creada_en}",
        ]
        if self.__cancelada_en:
            lineas.append(f"  Cancelada: {self.__cancelada_en}")
        return "\n".join(lineas)

    def mostrar_resumen(self):
        estado = "✅" if self.__activa else "❌"
        return (f"{estado} #{self.__id:03d} | {self.__cancha.get_nombre():<22} | "
                f"{self.__usuario.get_nombre():<25} | {self.__fecha} "
                f"{self.__hora_inicio:02d}:00-{self.get_hora_fin():02d}:00 | "
                f"${self.get_costo_total():>10,}")