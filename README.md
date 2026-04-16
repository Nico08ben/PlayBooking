# 🏟️ SportCore: PlayBooking

**PlayBooking** es la solución definitiva para la gestión y reserva de escenarios deportivos, desarrollada por la startup **SportCore**.  

Nuestra plataforma optimiza la interacción entre los complejos deportivos y los usuarios recreativos, eliminando la fricción de los procesos manuales.

---

## 🌟 Propuesta de Valor

En SportCore, entendemos que tu tiempo es valioso.  

PlayBooking ofrece una experiencia de reserva **rápida, fácil y organizada**. Nuestra solución simplifica la búsqueda de espacios, evitando confusiones de horarios y permitiéndote coordinar tus partidos sin inconvenientes.

Mejoramos la práctica deportiva brindando una herramienta **accesible y eficiente** que se adapta a las necesidades del deportista moderno.

---

## 🎯 Público Objetivo

Nuestra aplicación está dirigida a:

- Deportistas recreativos que buscan **inmediatez y orden**.
- Usuarios que valoran las **soluciones digitales** para gestionar su tiempo libre.
- Personas que desean evitar **complicaciones telefónicas o presenciales** al reservar una cancha.

---

## 🛑 El Problema que Resolvemos

La gestión manual de escenarios deportivos suele derivar en:

- Conflictos de horarios  
- Sobreventa de espacios  
- Falta de transparencia  

**PlayBooking soluciona esto mediante:**

- 🗓️ Administración de horarios diferenciados por día  
- ⚽ Gestión multi-deporte: Fútbol, Voleibol y Pádel  
- 🤖 Reservas inteligentes: sin cruces ni conflictos  
- 📊 Centralización de información: acceso inmediato a disponibilidad real  

---

## 🛠️ Aspectos Técnicos (Diseño OO)

Este proyecto ha sido desarrollado siguiendo los principios de la **Programación Orientada a Objetos en Python**, cumpliendo con los requerimientos académicos de la Universidad Autónoma de Occidente.

### 🔹 Arquitectura de Clases

- **Superclase:**
  - `Cancha`: Define la lógica de precios, horarios y estado  

- **Subclases (Herencia):**
  - `Futbol`: Tipos de superficie (Sintética, Sala, Natural)  
  - `Voley`: Modalidades (Normal y Playa)  
  - `Padel`: Gestión de jugadores y equipamiento  

- **Otras clases:**
  - `Usuario`: Encapsulamiento de datos y gestión de historial  
  - `Reserva`: Relación entre usuario, cancha y tiempo  

---

### 🔹 Características de Implementación

- 🔒 **Encapsulamiento:** Uso de atributos privados (`__atributo`)  
- 🔁 **Sobrescritura de métodos:**  
  - `mostrar_informacion`  
  - `to_dict`  
- 💾 **Persistencia:** Uso de `pickle` con `datos.pkl`  
- ✅ **Validaciones robustas:**  
  - Cédulas  
  - Teléfonos  
  - Correos electrónicos  

---

## 📂 Estructura del Proyecto

El sistema está modularizado en los siguientes archivos:
