# 🏟️ SportCore: PlayBooking

**PlayBooking** es la solución definitiva para la gestión y reserva de escenarios deportivos, desarrollada por la startup **SportCore**.  
Nuestra plataforma optimiza la interacción entre los complejos deportivos y los usuarios recreativos, eliminando la fricción de los procesos manuales.

---

## 🌟 Propuesta de Valor

En SportCore entendemos que tu tiempo es valioso. **PlayBooking** ofrece una experiencia de reserva rápida, fácil y organizada.

Nuestra solución simplifica la búsqueda de espacios, evitando confusiones de horarios y permitiéndote coordinar tus partidos sin inconvenientes.  
Mejoramos la práctica deportiva brindando una herramienta accesible y eficiente que se adapta a las necesidades del deportista moderno.

---

## 🎯 Público Objetivo

Nuestra aplicación está dirigida a:

- Deportistas recreativos que buscan inmediatez y orden.
- Usuarios que valoran las soluciones digitales para gestionar su tiempo libre.
- Personas que desean evitar complicaciones telefónicas o presenciales al reservar una cancha.

---

## 🛑 El Problema que Resolvemos

La gestión manual de escenarios deportivos suele derivar en conflictos de horarios, sobreventa de espacios y falta de transparencia.  
**PlayBooking** resuelve esto mediante:

- Administración de horarios diferenciados por día.
- Gestión multi-deporte: fútbol, voleibol y pádel en una sola interfaz.
- Reservas inteligentes: sistema que garantiza reservas por hora sin cruces ni conflictos.
- Centralización de información: reducción del error humano y acceso inmediato a la disponibilidad real.

---

## 🛠️ Aspectos Técnicos (Diseño OO)

Este proyecto ha sido desarrollado siguiendo los más altos estándares de la Programación Orientada a Objetos en Python, cumpliendo con los requerimientos académicos de la Universidad Autónoma de Occidente.

### Arquitectura de Clases

- **Superclase:** `Cancha` (clase base que define la lógica de precios, horarios y estado).
- **Subclases (herencia):**
  - `Futbol`: especializada en tipos de superficie (sintética, sala, natural).
  - `Voley`: diferenciación entre vóley normal y playa.
  - `Padel`: gestión de jugadores y equipamiento incluido.
- **Clase `Usuario`:** maneja el encapsulamiento de datos sensibles y el historial de reservas.
- **Clase `Reserva`:** orquestador de la relación entre usuario, cancha y tiempo.

### Características de Implementación

- **Encapsulamiento:** uso de atributos privados (`__atributo`) para proteger la integridad de los datos.
- **Sobrescritura de métodos:** métodos como `mostrar_informacion` y `to_dict` han sido especializados en cada subclase.
- **Persistencia:** carga y guardado automático mediante `pickle` en el archivo `datos.pkl`.
- **Validaciones robustas:** control de entradas para cédulas, teléfonos y correos electrónicos.

---

## 📂 Estructura del Proyecto

El sistema está modularizado en los siguientes archivos:

- `ProgramaGestion.py`: interfaz de usuario y lógica del menú principal.
- `ClaseCancha.py`: definición de la clase base.
- `ClasesHijasCancha.py`: implementación de la jerarquía de herencia.
- `ClaseUsuario.py`: gestión de perfiles y validaciones.
- `ClaseReserva.py`: lógica de negocio y control de disponibilidad.
- `InfoMin.py`: módulo de persistencia y configuración inicial.

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone https://github.com/Nico08ben/playbooking.git
```

### 2. Navegar a la carpeta
```bash
cd playbooking
```

### 3. Ejecutar la aplicación
```bash
python ProgramaGestion.py
```

> **Nota:** Si es la primera vez que se usa y se desea regenerar la base de datos, ejecutar:
```bash
python InfoMin.py
```

---

## 👥 Equipo de Desarrollo (SportCore)

Este MVP fue desarrollado por:

| Nombre | GitHub |
|--------|--------|
| Nicolás Armero Rosero | [@Nico08ben](https://github.com/Nico08ben) |
| Sara Mesa Lenis | [@saramesal](https://github.com/saramesal)|
| Karen Juliana Dueñas Castro | [@karen11439](https://github.com/karen11439) |
| Santiago Garcia | [@Sant1833](https://github.com/Sant1833) |

**Asignatura:** Programación (G02)  
**Facultad de Ingeniería - Ingeniería de Datos e Inteligencia Artificial**  
**Universidad Autónoma de Occidente
