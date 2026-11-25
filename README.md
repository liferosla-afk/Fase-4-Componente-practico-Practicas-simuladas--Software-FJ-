# Sistema de Gestión y Reservas - Software FJ

**Curso:** Programación (213023) - UNAD  
**Actividad:** Fase 4 – Componente práctico: Prácticas simuladas  
**Estudiante:** Lizeth Fernanda Ospitia Ladino
**Grupo:** 213023_641

## Descripción del proyecto
Aplicación modular desarrollada en Python bajo el paradigma de Programación Orientada a Objetos (POO) para gestionar clientes, servicios especializados (salas, equipos y asesorías) y reservas en memoria, garantizando ejecución continua mediante manejo avanzado de excepciones y auditoría en archivos de log.

## Estructura del código
* `excepciones.py`: Jerarquía de excepciones personalizadas y configuración del sistema de logs (`logs/eventos_sistema.log`).
* `modelos.py`: Clases abstractas (`Entidad`, `Servicio`), encapsulación (`Cliente`) y herencia/polimorfismo (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`).
* `gestor.py`: Lógica de reservas (`Reserva`) y administración en listas internas (`GestorSoftwareFJ`) con encadenamiento de excepciones.
* `main.py`: Simulación de 12 operaciones (válidas y con errores controlados) sin interrupciones.

## Ejecución
Desde la terminal ubicada en la carpeta del proyecto, ejecutar:
```bash
python main.py
```
