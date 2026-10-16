# 🏥 MediNova - Sistema de Gestión de Citas Médicas
> **Asignatura:** Componentes de Lógica de Negocio — Unidad 3: Diseño Arquitectural del Sistema con IA 
> **Institución:** Universidad Autónoma de Nuevo León (UANL) — Facultad de Ingeniería Mecánica y Eléctrica (FIME)  
> **Semestre:** Agosto - Diciembre 2026  

---

## 👥 Integrantes del Equipo
* **Hernández  Roberto** | ITS |
* **Rodríguez  Danna** | ITS | 
* **Martínez Álvarez** | ITS |


---

##  Alcance del Proyecto
MediNova es una clínica privada con tres sucursales que gestiona consultas de medicina general, especialidades, estudios básicos y procedimientos menores. Este proyecto transforma el análisis de requerimientos de la Unidad 2 en una propuesta de arquitectura de software basada en **Domain-Driven Design (DDD)**.

El alcance del diseño arquitectónico cubre los 5 Casos de Uso principales:
1. **`CU-01`**: Consulta de disponibilidad por especialidad, sucursal, fecha y horario.
2. **`CU-02`**: Prevención y bloqueo de citas duplicadas en tiempo real.
3. **`CU-03`**: Cancelación de citas con registro obligatorio de evidencia.
4. **`CU-04`**: Detección y cambio automático a *No-Show* (20 minutos de tolerancia).
5. **`CU-05`**: Control y validación de sobrecupos configurables por médico (máx. 2 por turno).

---

##  Patrón de Lógica de Negocio Elegido: Domain Model
Tras evaluar *Transaction Script*, *Table Module* y *Domain Model*, el equipo seleccionó **Domain Model**. 

### **Justificación Principal**
El negocio de MediNova presenta reglas interconectadas e invariantes complejas (como la penalización por reincidencia de 3 *no-shows*, la gestión de concurrencia de 3 minutos y los límites de sobrecupos). Domain Model permite encapsular estas reglas directamente en los **Aggregates** (`Cita`, `Paciente`, `JornadaMedica`), protegiendo la consistencia de los datos y evitando duplicar validaciones en procedimientos sueltos.

---

##  Estructura del Repositorio

```text
├── diagramas/                    
│   ├── clases                             
│   ├── dominio                            
│   └── secuancia                   
│
├── docs/                       
│   ├── ADR               
│   ├── Bitacora IA/
│   ├── Informe/ 
│   ├── Trazabilida/
│   └── Unidad 2/
│
├── src/                                   
│   ├── aplication/                 
│   ├── domain                  
│   └── infrastructure/                   
│
└── README.md                             