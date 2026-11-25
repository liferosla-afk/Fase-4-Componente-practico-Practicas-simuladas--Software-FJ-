from modelos import Entidad, Cliente, Servicio
from excepciones import (
    ErrorBaseSoftwareFJ,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    DatoInvalidoError,
    registrar_evento
)

class Reserva(Entidad):
    """Integra un Cliente, un Servicio, duración y estado de reserva."""
    def __init__(self, cliente: Cliente, servicio: Servicio, horas: int):
        super().__init__()
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere instancias válidas de Cliente y Servicio.")
        if horas <= 0:
            raise DatoInvalidoError("Las horas de reserva deben ser mayores a cero.")
        
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "PENDIENTE"
        self.costo_final = 0.0

    def validar(self) -> bool:
        return self.horas > 0 and self.cliente.validar() and self.servicio.validar()

    def confirmar(self, impuesto: float = 0.19, descuento: float = 0.0):
        """Usa try/except/else para confirmar disponibilidad y calcular costos."""
        try:
            if self.estado != "PENDIENTE":
                raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado {self.estado}.")
            if not self.servicio.disponible:
                raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre}' no está disponible.")
            
            self.costo_final = self.servicio.calcular_costo_total(self.horas, impuesto, descuento)
        except ErrorBaseSoftwareFJ as e:
            registrar_evento("ERROR", f"Fallo al confirmar reserva {self.id}: {e}")
            raise
        else:
            self.estado = "CONFIRMADA"
            self.servicio.disponible = False
            registrar_evento("INFO", f"Reserva {self.id} CONFIRMADA para {self.cliente.nombre}. Total: ${self.costo_final:,.2f}")

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise OperacionNoPermitidaError("La reserva ya se encuentra cancelada.")
        if self.estado == "PROCESADA":
            raise OperacionNoPermitidaError("No se puede cancelar una reserva que ya fue procesada.")
        
        self.estado = "CANCELADA"
        self.servicio.disponible = True
        registrar_evento("WARNING", f"Reserva {self.id} CANCELADA. Servicio '{self.servicio.nombre}' liberado.")

    def procesar(self):
        """Usa try/except/finally para asegurar auditoría del intento de procesamiento."""
        exito = False
        try:
            if self.estado != "CONFIRMADA":
                raise OperacionNoPermitidaError("Solo se pueden procesar reservas previamente CONFIRMADAS.")
            self.estado = "PROCESADA"
            self.servicio.disponible = True
            exito = True
        except ErrorBaseSoftwareFJ as e:
            registrar_evento("ERROR", f"Error procesando reserva {self.id}: {e}")
            raise
        finally:
            estado_auditoria = "EXITOSO" if exito else "FALLIDO"
            registrar_evento("INFO", f"Auditoría de procesamiento reserva {self.id}: {estado_auditoria}")

    def resumen(self) -> str:
        return (
            f"Reserva [{self.id}] | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} ({self.horas}h) | "
            f"Estado: {self.estado} | Total: ${self.costo_final:,.2f}"
        )


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas en listas internas en memoria."""
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    def registrar_cliente(self, nombre: str, documento: str, correo: str) -> Cliente:
        """Demuestra try/except/else y encadenamiento de excepciones (raise ... from)."""
        try:
            for c in self._clientes:
                if c.documento == documento.strip():
                    raise OperacionNoPermitidaError(f"Ya existe un cliente con el documento {documento}.")
            nuevo_cliente = Cliente(nombre, documento, correo)
        except Exception as e:
            registrar_evento("ERROR", f"Error registrando cliente ({nombre}): {e}")
            raise ReservaInvalidaError(f"No fue posible dar de alta al cliente '{nombre}'.") from e
        else:
            self._clientes.append(nuevo_cliente)
            registrar_evento("INFO", f"Cliente registrado: {nuevo_cliente.resumen()}")
            return nuevo_cliente

    def agregar_servicio(self, servicio: Servicio) -> Servicio:
        try:
            if not isinstance(servicio, Servicio):
                raise DatoInvalidoError("El objeto proporcionado no es un Servicio válido.")
            servicio.validar()
            self._servicios.append(servicio)
            registrar_evento("INFO", f"Servicio agregado: {servicio.resumen()}")
            return servicio
        except Exception as e:
            registrar_evento("ERROR", f"Error agregando servicio: {e}")
            raise

    def crear_reserva(self, cliente: Cliente, servicio: Servicio, horas: int, impuesto: float = 0.19, descuento: float = 0.0) -> Reserva:
        try:
            reserva = Reserva(cliente, servicio, horas)
            reserva.confirmar(impuesto=impuesto, descuento=descuento)
            self._reservas.append(reserva)
            return reserva
        except ErrorBaseSoftwareFJ as e:
            raise ReservaInvalidaError(f"Fallo en la creación de reserva para {cliente.nombre}.") from e

    def generar_reporte(self):
        print("\n" + "=" * 65)
        print("RESUMEN ACTUAL DEL SISTEMA - SOFTWARE FJ")
        print("=" * 65)
        print(f"Clientes registrados: {len(self._clientes)}")
        for c in self._clientes:
            print("  -", c.resumen())
        print(f"\nServicios disponibles en catálogo: {len(self._servicios)}")
        for s in self._servicios:
            print("  -", s.resumen())
        print(f"\nReservas gestionadas: {len(self._reservas)}")
        for r in self._reservas:
            print("  -", r.resumen())
        print("=" * 65)