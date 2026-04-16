"""
╔══════════════════════════════════════════════════════════════╗
║          SISTEMA DE RESERVAS DE CANCHAS DEPORTIVAS           ║
║                     SportField Manager                       ║
╚══════════════════════════════════════════════════════════════╝
Autores: Nicolás Armero Rosero, Santiago Andres Garcia Sanchez,
         Karen Juliana Dueñas, Sara Mesa Lenis
"""

import os
from datetime import datetime, date

from ClaseUsuario import Usuario, cedula_valida, valida_tel, email_valido
from ClaseReserva import Reserva
from InfoMin      import guardar, cargar

canchas, usuarios, reservas = cargar()


# ════════════════════════════════════════════════════════════════════════════════
#  HELPERS DE UI
# ════════════════════════════════════════════════════════════════════════════════

LINEA       = "═" * 64
LINEA_CORTA = "─" * 64


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def encabezado(titulo):
    limpiar()
    print(f"\n{LINEA}")
    print(f"  🏟️  {titulo}")
    print(f"  {datetime.now().strftime('%d/%m/%Y  %H:%M')}")
    print(LINEA)


def pausa():
    input("\n  Presiona ENTER para continuar...")


def separador():
    print(LINEA_CORTA)


def pedir_entero(mensaje, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"  ⚠ El valor mínimo es {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠ El valor máximo es {maximo}.")
                continue
            return valor
        except ValueError:
            print("  ⚠ Ingresa un número entero válido.")


def pedir_fecha(mensaje, solo_futuras=True):
    while True:
        texto = input(mensaje).strip()
        try:
            fecha_dt = datetime.strptime(texto, "%Y-%m-%d").date()
        except ValueError:
            print("  ⚠ Formato inválido. Usa AAAA-MM-DD (ej: 2025-07-20).")
            continue

        if solo_futuras:
            hoy = date.today()
            if fecha_dt < hoy:
                print("  ⚠ La fecha no puede ser en el pasado.")
                continue
            if (fecha_dt - hoy).days > 90:
                print("  ⚠ Solo se permiten reservas con hasta 90 días de anticipación.")
                continue
        return texto


def pedir_opcion(opciones_validas):
    while True:
        op = input("\n  Opción: ").strip()
        if op in opciones_validas:
            return op
        print(f"  ⚠ Opción inválida. Elige entre: {', '.join(sorted(opciones_validas))}")


def confirmar(mensaje="  ¿Confirmar? (s/n): "):
    return input(mensaje).strip().lower() == "s"


# ════════════════════════════════════════════════════════════════════════════════
#  MÓDULO: CANCHAS
# ════════════════════════════════════════════════════════════════════════════════

def mostrar_canchas(solo_activas=True):
    lista = [c for c in canchas.values() if not solo_activas or c.get_activa()]
    if not lista:
        print("  No hay canchas registradas.")
        return
    for c in lista:
        print()
        for linea in c.mostrar_informacion().split("\n"):
            print(f"  {linea}")
        separador()


# ════════════════════════════════════════════════════════════════════════════════
#  MÓDULO: USUARIOS
# ════════════════════════════════════════════════════════════════════════════════

def mostrar_usuarios():
    if not usuarios:
        print("  No hay usuarios registrados.")
        return
    print(f"\n  {'NOMBRE':<32} {'CÉDULA':<14} {'TELÉFONO':<14} {'RESERVAS'}")
    separador()
    for u in usuarios.values():
        print(f"  {u.mostrar_informacion()}")
    separador()
    print(f"  Total: {len(usuarios)} usuario(s) registrado(s).")


def registrar_o_buscar_usuario():
    cedula = input("  Cédula del usuario : ").strip()

    if not cedula:
        print("  ⚠ Cédula vacía. Operación cancelada.")
        return None

    if not cedula_valida(cedula):
        print("  ⚠ Cédula inválida (solo dígitos, 8-10 caracteres).")
        return None

    if cedula in usuarios:
        u = usuarios[cedula]
        print(f"  ✅ Bienvenido de nuevo, {u.get_nombre()}!")
        return u

    print("  🆕 Usuario no encontrado. Complete el registro:")
    separador()

    nombre = input("  Nombre    : ").strip()
    if not nombre:
        print("  ⚠ Nombre vacío. Operación cancelada.")
        return None

    apellido = input("  Apellido  : ").strip()
    if not apellido:
        print("  ⚠ Apellido vacío. Operación cancelada.")
        return None

    while True:
        tel = input("  Teléfono  : ").strip()
        if valida_tel(tel):
            break
        print("  ⚠ Teléfono inválido. Ingresa un número colombiano de 10 dígitos (ej: 3001234567).")

    email = input("  Email (opcional, ENTER para omitir): ").strip()
    if email and not email_valido(email):
        print("  ⚠ Email con formato inválido. Se omitirá.")
        email = ""

    print(f"\n  Nuevo usuario:")
    print(f"     Nombre   : {nombre.title()} {apellido.title()}")
    print(f"     Cédula   : {cedula}")
    print(f"     Teléfono : {tel}")
    if email:
        print(f"     Email    : {email}")

    if not confirmar("  ¿Confirmar registro? (s/n): "):
        print("  Registro cancelado.")
        return None

    nuevo = Usuario(cedula, nombre, apellido, tel, email)
    usuarios[cedula] = nuevo
    guardar(canchas, usuarios, reservas)
    print(f"  ✅ Usuario '{nuevo.get_nombre()}' registrado correctamente.")
    return nuevo

# ════════════════════════════════════════════════════════════════════════════════
#  MÓDULO: RESERVAS
# ════════════════════════════════════════════════════════════════════════════════

def listar_reservas(filtro="activas"):
    mapa = {
        "activas":    lambda r: r.get_activa(),
        "canceladas": lambda r: not r.get_activa(),
        "futuras":    lambda r: r.get_activa() and r.es_futura(),
        "todas":      lambda r: True,
    }
    lista = [r for r in reservas if mapa.get(filtro, lambda r: True)(r)]

    if not lista:
        print(f"  No hay reservas ({filtro}).")
        return

    for r in lista:
        print(f"  {r.mostrar_resumen()}")

    if filtro in ("activas", "futuras", "todas"):
        total = sum(r.get_costo_total() for r in lista if r.get_activa())
        separador()
        print(f"  {len(lista)} reserva(s)  |  💰 Total activas: ${total:,}")


def crear_reserva():
    encabezado("NUEVA RESERVA")

    print("\n  ── Canchas disponibles ──────────────────────────────────")
    mostrar_canchas(solo_activas=True)

    print("\n  ── Datos del usuario ────────────────────────────────────")
    usuario = registrar_o_buscar_usuario()
    if usuario is None:
        return

    print("\n  ── Datos de la reserva ──────────────────────────────────")

    id_c = input("  ID de la cancha    : ").strip().upper()
    if id_c not in canchas:
        print(f"  ⚠ Cancha '{id_c}' no encontrada.")
        return
    if not canchas[id_c].get_activa():
        print("  ⚠ Esa cancha no está disponible actualmente.")
        return

    fecha    = pedir_fecha("  Fecha (AAAA-MM-DD) : ")

    hora     = pedir_entero("  Hora inicio (6-22) : ", minimo=6, maximo=22)
    if fecha == date.today().strftime("%Y-%m-%d") and hora <= datetime.now().hour:
        print(f"  ⚠ La hora {hora:02d}:00 ya pasó. Hora actual: {datetime.now().hour:02d}:{datetime.now().minute:02d}.")
        return
    
    duracion = pedir_entero("  Duración (1-8 hrs) : ", minimo=1, maximo=8)
    if hora + duracion > 23:
        print(f"  ⚠ La reserva terminaría a las {hora + duracion:02d}:00, pero el cierre es a las 23:00.")
        return

    cancha_obj = canchas[id_c]

    # Verificar disponibilidad comparando directamente con cada reserva activa
    conflicto = None
    for r in reservas:
        if (r.get_activa()
                and r.get_cancha().get_id() == id_c
                and r.get_fecha() == fecha
                and hora < r.get_hora_fin()
                and r.get_hora_inicio() < hora + duracion):
            conflicto = r
            break

    if conflicto:
        print(f"\n  ⚠ CONFLICTO: La cancha ya está reservada en ese horario.")
        print(f"  Reserva existente: {conflicto.mostrar_resumen()}")
        return

    costo_prev = cancha_obj.calcular_costo(hora, duracion, fecha)
    print(f"\n  ┌{'─'*44}")
    print(f"  │  📋 RESUMEN DE LA RESERVA")
    print(f"  ├{'─'*44}")
    print(f"  │  Cancha  : {cancha_obj.get_nombre()}")
    print(f"  │  Usuario : {usuario.get_nombre()}")
    print(f"  │  Fecha   : {fecha}")
    print(f"  │  Horario : {hora:02d}:00 — {hora+duracion:02d}:00  ({duracion}h)")
    print(f"  │  Costo   : ${costo_prev:,}")
    print(f"  └{'─'*44}")

    if not confirmar("\n  ¿Confirmar reserva? (s/n): "):
        print("  Reserva cancelada por el usuario.")
        return

    try:
        nueva = Reserva(usuario, cancha_obj, fecha, hora, duracion)
    except ValueError as e:
        print(f"  ⚠ No se pudo crear la reserva: {e}")
        return

    usuario.incrementar_reservas()
    reservas.append(nueva)
    guardar(canchas, usuarios, reservas)
    print(f"\n  ✅ ¡Reserva #{nueva.get_id():03d} creada con éxito!")
    print(f"     {cancha_obj.get_nombre()}  |  {fecha}  {hora:02d}:00-{hora+duracion:02d}:00")


def cancelar_reserva():
    encabezado("CANCELAR RESERVA")

    print("\n  Reservas activas:")
    listar_reservas("activas")

    if not any(r.get_activa() for r in reservas):
        return

    id_r = pedir_entero("\n  ID de la reserva a cancelar (0 para volver): ", minimo=0)
    if id_r == 0:
        return

    reserva_obj = next((r for r in reservas if r.get_id() == id_r), None)
    if reserva_obj is None:
        print(f"  ⚠ No se encontró la reserva #{id_r}.")
        return

    puede, motivo = reserva_obj.puede_cancelarse()
    if not puede:
        print(f"  ⚠ {motivo}")
        return

    print(f"\n  Vas a cancelar:")
    print(f"  {reserva_obj.mostrar_resumen()}")

    if not confirmar("  ¿Confirmar cancelación? (s/n): "):
        print("  Operación abortada.")
        return

    try:
        reserva_obj.cancelar()
        guardar(canchas, usuarios, reservas)
        print("  ✅ Reserva cancelada correctamente.")
    except ValueError as e:
        print(f"  ⚠ {e}")


def buscar_reservas():
    encabezado("BUSCAR RESERVAS")
    print("  1. Por cédula de usuario")
    print("  2. Por ID de cancha")
    print("  3. Por fecha")
    print("  0. Volver")

    op = pedir_opcion({"1", "2", "3", "0"})
    if op == "0":
        return

    resultados = []

    if op == "1":
        cedula = input("  Cédula: ").strip()
        resultados = [r for r in reservas if r.get_usuario().get_cedula() == cedula]
        if not resultados and cedula not in usuarios:
            print("  ⚠ No existe ningún usuario con esa cédula.")
            return

    elif op == "2":
        id_c = input("  ID de cancha (ej: F1, V2, P1): ").strip().upper()
        if id_c not in canchas:
            print(f"  ⚠ Cancha '{id_c}' no encontrada.")
            return
        resultados = [r for r in reservas if r.get_cancha().get_id() == id_c]

    elif op == "3":
        fecha = input("  Fecha (AAAA-MM-DD): ").strip()
        resultados = [r for r in reservas if r.get_fecha() == fecha]

    separador()
    if not resultados:
        print("  Sin resultados para esa búsqueda.")
    else:
        activas = sum(1 for r in resultados if r.get_activa())
        print(f"  {len(resultados)} resultado(s) — {activas} activa(s):\n")
        for r in resultados:
            print(f"  {r.mostrar_resumen()}")


# ════════════════════════════════════════════════════════════════════════════════
#  MÓDULO: DISPONIBILIDAD
# ════════════════════════════════════════════════════════════════════════════════

def consultar_disponibilidad():
    encabezado("DISPONIBILIDAD DE CANCHAS")
    mostrar_canchas(solo_activas=True)

    id_c  = input("  ID cancha         : ").strip().upper()
    fecha = pedir_fecha("  Fecha (AAAA-MM-DD): ", solo_futuras=False)

    if id_c not in canchas:
        print(f"  ⚠ Cancha '{id_c}' no encontrada.")
        return
    if not canchas[id_c].get_activa():
        print("  ⚠ Esa cancha está actualmente inactiva.")
        return

    ocupadas = {}
    for r in reservas:
        if r.get_activa() and r.get_cancha().get_id() == id_c and r.get_fecha() == fecha:
            for h in range(r.get_hora_inicio(), r.get_hora_fin()):
                ocupadas[h] = r

    cancha_obj  = canchas[id_c]
    
    # Obtener fecha y hora actuales para invalidar horas que ya pasaron
    hoy_str = date.today().strftime("%Y-%m-%d")
    hora_actual = datetime.now().hour

    libres_list = []
    for h in range(6, 23):
        es_pasado = (fecha == hoy_str and h <= hora_actual) or (fecha < hoy_str)
        if h not in ocupadas and not es_pasado:
            libres_list.append(h)

    print(f"\n  📅 {cancha_obj.get_nombre()}  —  {fecha}")
    separador()

    for hora in range(6, 23):
        es_pasado = (fecha == hoy_str and hora <= hora_actual) or (fecha < hoy_str)
        
        if hora in ocupadas:
            r = ocupadas[hora]
            if es_pasado:
                print(f"  {hora:02d}:00  ⚫ FINALIZADA  "
                      f"(Reserva #{r.get_id():03d} — {r.get_usuario().get_nombre()})")
            else:
                print(f"  {hora:02d}:00  🔴 OCUPADA     "
                      f"(Reserva #{r.get_id():03d} — {r.get_usuario().get_nombre()})")
        elif es_pasado:
            print(f"  {hora:02d}:00  ⚫ PASADA      ")
        else:
            precio = cancha_obj.get_precio_franja(hora)
            print(f"  {hora:02d}:00  🟢 LIBRE       ${precio:,}/hr")


    separador()
    print(f"  Horas libres (disponibles): {len(libres_list)}  |  Horas ocupadas: {len(ocupadas)}")

    if libres_list:
        bloques = []
        inicio_bloque = libres_list[0]
        anterior      = libres_list[0]
        for h in libres_list[1:]:
            if h != anterior + 1:
                bloques.append((inicio_bloque, anterior + 1))
                inicio_bloque = h
            anterior = h
        bloques.append((inicio_bloque, anterior + 1))
        desc = ", ".join(f"{a:02d}:00-{b:02d}:00" for a, b in bloques)
        print(f"  Bloques libres: {desc}")


# ════════════════════════════════════════════════════════════════════════════════
#  MÓDULO: REPORTES
# ════════════════════════════════════════════════════════════════════════════════

def ver_reportes():
    encabezado("REPORTES Y ESTADÍSTICAS")
    print("  1. Resumen general")
    print("  2. Reservas activas")
    print("  3. Reservas futuras")
    print("  4. Historial completo")
    print("  5. Reservas canceladas")
    print("  6. Cancha más rentable")
    print("  0. Volver")

    op = pedir_opcion({"1", "2", "3", "4", "5", "6", "0"})
    if op == "0":
        return

    if op == "1":
        activas    = sum(1 for r in reservas if r.get_activa())
        canceladas = sum(1 for r in reservas if not r.get_activa())
        futuras    = sum(1 for r in reservas if r.get_activa() and r.es_futura())
        ingresos   = sum(r.get_costo_total() for r in reservas if r.get_activa())

        print(f"\n  {'─── RESUMEN GENERAL ───':^44}")
        separador()
        print(f"  📋 Total reservas     : {len(reservas)}")
        print(f"  ✅ Activas            : {activas}")
        print(f"  📅 Futuras            : {futuras}")
        print(f"  ❌ Canceladas         : {canceladas}")
        print(f"  👤 Usuarios           : {len(usuarios)}")
        print(f"  🏟️  Canchas activas    : {sum(1 for c in canchas.values() if c.get_activa())}")
        separador()
        print(f"  💰 Ingresos (activas) : ${ingresos:,}")

    elif op in ("2", "3", "4", "5"):
        filtros = {"2": "activas", "3": "futuras", "4": "todas", "5": "canceladas"}
        print()
        listar_reservas(filtros[op])

    elif op == "6":
        if not reservas:
            print("  No hay reservas registradas aún.")
            return
        ingresos_por_cancha = {}
        for r in reservas:
            if r.get_activa():
                cid = r.get_cancha().get_id()
                ingresos_por_cancha[cid] = ingresos_por_cancha.get(cid, 0) + r.get_costo_total()
        if not ingresos_por_cancha:
            print("  No hay reservas activas.")
            return
        print(f"\n  {'─── INGRESOS POR CANCHA ───':^44}")
        separador()
        ranking = sorted(ingresos_por_cancha.items(), key=lambda x: x[1], reverse=True)
        for pos, (cid, total) in enumerate(ranking, 1):
            nombre = canchas[cid].get_nombre() if cid in canchas else cid
            print(f"  {pos}. {nombre:<28}  ${total:>12,}")
        separador()
        mejor_id     = ranking[0][0]
        mejor_nombre = canchas[mejor_id].get_nombre() if mejor_id in canchas else mejor_id
        print(f"  🏆 Más rentable: {mejor_nombre}  (${ranking[0][1]:,})")


# ════════════════════════════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════════

MENU_PRINCIPAL = """
  ┌──────────────────────────────────────────┐
  │          ¿Qué deseas hacer?              │
  ├──────────────────────────────────────────┤
  │  1  Ver canchas disponibles              │
  │  2  Ver usuarios registrados             │
  │  3  Crear nueva reserva                  │
  │  4  Ver disponibilidad de cancha         │
  │  5  Cancelar una reserva                 │
  │  6  Buscar reservas                      │
  │  7  Reportes y estadísticas              │
  │  0  Guardar y salir                      │
  └──────────────────────────────────────────┘"""


def main():
    while True:
        encabezado("SISTEMA DE RESERVAS — SportField Manager")
        print(MENU_PRINCIPAL)

        op = pedir_opcion({"1", "2", "3", "4", "5", "6", "7", "0"})

        if op == "1":
            encabezado("CANCHAS DISPONIBLES")
            mostrar_canchas()
            pausa()

        elif op == "2":
            encabezado("USUARIOS REGISTRADOS")
            mostrar_usuarios()
            pausa()

        elif op == "3":
            crear_reserva()
            pausa()

        elif op == "4":
            consultar_disponibilidad()
            pausa()

        elif op == "5":
            cancelar_reserva()
            pausa()

        elif op == "6":
            buscar_reservas()
            pausa()

        elif op == "7":
            ver_reportes()
            pausa()

        elif op == "0":
            guardar(canchas, usuarios, reservas)
            limpiar()
            print("\n  ✅ Datos guardados. ¡Hasta pronto!\n")
            break


if __name__ == "__main__":
    main()