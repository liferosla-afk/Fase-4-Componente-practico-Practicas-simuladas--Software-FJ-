from modelos import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from gestor import GestorSoftwareFJ
from excepciones import ErrorBaseSoftwareFJ, registrar_evento

def ejecutar_operacion_segura(numero: int, descripcion: str, funcion):
    """Barrera protectora que ejecuta cada operación sin detener el sistema."""
    print(f"\n[Operación {numero:02d}] {descripcion}")
    try:
        resultado = funcion()
    except ErrorBaseSoftwareFJ as e:
        causa = f" (Causa original: {e.__cause__})" if e.__cause__ else ""
        print(f"   -> [ERROR CONTROLADO] {e}{causa}")
    except Exception as e:
        registrar_evento("CRITICAL", f"Error inesperado en operación {numero}: {type(e).__name__} - {e}")
        print(f"   -> [ERROR CRÍTICO RECUPERADO] {type(e).__name__}: {e}")
    else:
        print("   -> [ÉXITO] Operación completada correctamente.")
        return resultado
    finally:
        print("   -> Flujo verificado; el sistema continúa operando.")

def main():
    registrar_evento("INFO", "=== INICIO DE SIMULACIÓN SOFTWARE FJ ===")
    sistema = GestorSoftwareFJ()

    # 1. Registro válido de cliente 1
    cliente_1 = ejecutar_operacion_segura(
        1, "Registrar cliente válido (Laura Gómez)",
        lambda: sistema.registrar_cliente("Laura Gómez", "1098765432", "laura.gomez@correo.com")
    )

    # 2. Registro válido de cliente 2
    cliente_2 = ejecutar_operacion_segura(
        2, "Registrar cliente válido (Carlos Mendoza)",
        lambda: sistema.registrar_cliente("Carlos Mendoza", "80123456", "cmendoza@empresa.co")
    )

    # 3. Registro inválido de cliente (correo sin arroba y documento corto)
    ejecutar_operacion_segura(
        3, "Intentar registrar cliente con datos inválidos",
        lambda: sistema.registrar_cliente("Ana", "123", "ana_correo_invalido")
    )

    # 4. Registro inválido de cliente (documento duplicado)
    ejecutar_operacion_segura(
        4, "Intentar registrar cliente con documento duplicado",
        lambda: sistema.registrar_cliente("Laura Duplicada", "1098765432", "otra@correo.com")
    )

    # 5. Creación válida de 3 servicios especializados
    sala_juntas = ejecutar_operacion_segura(
        5, "Agregar servicio: Sala de Juntas Ejecutiva",
        lambda: sistema.agregar_servicio(ReservaSala("Sala Norte", 60000, capacidad=12, tiene_proyector=True))
    )

    equipo_mac = ejecutar_operacion_segura(
        6, "Agregar servicio: Alquiler MacBook Pro M3",
        lambda: sistema.agregar_servicio(AlquilerEquipo("MacBook Pro", 35000, "Computación", deposito_seguridad=50000))
    )

    asesoria_ia = ejecutar_operacion_segura(
        7, "Agregar servicio: Asesoría en Arquitectura Cloud",
        lambda: sistema.agregar_servicio(AsesoriaEspecializada("Consultoría Cloud", 120000, "Infraestructura", nivel_senior=True))
    )

    # 8. Creación incorrecta de servicio (tarifa negativa)
    ejecutar_operacion_segura(
        8, "Intentar crear sala con tarifa negativa",
        lambda: sistema.agregar_servicio(ReservaSala("Sala Defectuosa", -15000, capacidad=5))
    )

    # 9. Reserva exitosa con descuento aplicado (sobrecarga de parámetros)
    reserva_1 = ejecutar_operacion_segura(
        9, "Crear y confirmar reserva válida de Sala Norte (4 horas, 10% descuento)",
        lambda: sistema.crear_reserva(cliente_1, sala_juntas, horas=4, descuento=0.10)
    )

    # 10. Reserva fallida (servicio ya ocupado por la reserva anterior)
    ejecutar_operacion_segura(
        10, "Intentar reservar Sala Norte mientras está ocupada",
        lambda: sistema.crear_reserva(cliente_2, sala_juntas, horas=2)
    )

    # 11. Reserva fallida por cálculo inconsistente (descuento del 150%)
    ejecutar_operacion_segura(
        11, "Intentar reservar MacBook Pro con descuento inválido (150%)",
        lambda: sistema.crear_reserva(cliente_2, equipo_mac, horas=3, descuento=1.5)
    )

    # 12. Procesamiento exitoso de reserva y simulación de error inesperado controlado
    ejecutar_operacion_segura(
        12, "Procesar reserva confirmada y liberar sala",
        lambda: reserva_1.procesar()
    )

    # Mostrar resumen final en consola
    sistema.generar_reporte()
    registrar_evento("INFO", "=== FIN DE SIMULACIÓN SIN INTERRUPCIONES ===")
    print("\nRevisa el archivo 'logs/eventos_sistema.log' para ver la auditoría completa.")

if __name__ == "__main__":
    main()
    