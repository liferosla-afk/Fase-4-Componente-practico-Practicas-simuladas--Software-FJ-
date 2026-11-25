from abc import ABC, abstractmethod
from datetime import datetime
import uuid
from excepciones import (
    DatoInvalidoError,
    ParametroFaltanteError,
    CalculoInconsistenteError
)

class Entidad(ABC):
    """Clase abstracta base para todas las entidades del sistema."""
    def __init__(self):
        self._id = str(uuid.uuid4())[:8].upper()
        self._fecha_registro = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def resumen(self) -> str:
        pass

    @abstractmethod
    def validar(self) -> bool:
        pass


class Cliente(Entidad):
    """Representa un cliente con datos encapsulados y validaciones estrictas."""
    def __init__(self, nombre: str, documento: str, correo: str):
        super().__init__()
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.validar()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not valor.strip():
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        if len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str):
        if not valor or not valor.strip():
            raise ParametroFaltanteError("El documento de identidad es obligatorio.")
        if not valor.strip().isdigit() or len(valor.strip()) < 6:
            raise DatoInvalidoError("El documento debe contener mínimo 6 dígitos numéricos.")
        self.__documento = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise DatoInvalidoError(f"Correo electrónico inválido: '{valor}'.")
        self.__correo = valor.strip().lower()

    def validar(self) -> bool:
        return bool(self.__nombre and self.__documento and self.__correo)

    def resumen(self) -> str:
        doc_oculto = "*" * (len(self.__documento) - 3) + self.__documento[-3:]
        return f"Cliente [{self.id}] {self.__nombre} | Doc: {doc_oculto} | Email: {self.__correo}"


class Servicio(Entidad, ABC):
    """Clase abstracta para los servicios que ofrece Software FJ."""
    def __init__(self, nombre: str, tarifa_hora: float):
        super().__init__()
        if not nombre or not nombre.strip():
            raise ParametroFaltanteError("El nombre del servicio no puede estar vacío.")
        if tarifa_hora <= 0:
            raise DatoInvalidoError("La tarifa por hora debe ser mayor a cero.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    @abstractmethod
    def calcular_tarifa_base(self, horas: int) -> float:
        pass

    @abstractmethod
    def validar_parametros(self) -> bool:
        pass

    def calcular_costo_total(self, horas: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """Método sobrecargado mediante parámetros opcionales (impuesto y descuento)."""
        if horas <= 0:
            raise DatoInvalidoError("La duración de la reserva debe ser mayor a 0 horas.")
        if not (0 <= descuento < 1):
            raise CalculoInconsistenteError("El descuento debe estar entre 0.0 (0%) y 0.99 (99%).")
        if impuesto < 0:
            raise CalculoInconsistenteError("El impuesto no puede ser negativo.")

        subtotal = self.calcular_tarifa_base(horas)
        con_descuento = subtotal * (1 - descuento)
        total = con_descuento * (1 + impuesto)
        return round(total, 2)

    def validar(self) -> bool:
        return self.validar_parametros()


class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas de reuniones o capacitación."""
    def __init__(self, nombre: str, tarifa_hora: float, capacidad: int, tiene_proyector: bool = True):
        super().__init__(nombre, tarifa_hora)
        self.capacidad = capacidad
        self.tiene_proyector = tiene_proyector
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if self.capacidad < 2 or self.capacidad > 100:
            raise DatoInvalidoError("La capacidad de la sala debe estar entre 2 y 100 personas.")
        return True

    def calcular_tarifa_base(self, horas: int) -> float:
        recargo_equipo = 15000.0 if self.tiene_proyector else 0.0
        return (self._tarifa_hora * horas) + recargo_equipo

    def resumen(self) -> str:
        estado = "Disponible" if self._disponible else "Ocupada"
        return f"Sala [{self.id}] {self._nombre} (Cap: {self.capacidad}) - ${self._tarifa_hora:,.0f}/h [{estado}]"


class AlquilerEquipo(Servicio):
    """Servicio especializado para préstamo de hardware tecnológico."""
    def __init__(self, nombre: str, tarifa_hora: float, categoria_equipo: str, deposito_seguridad: float):
        super().__init__(nombre, tarifa_hora)
        self.categoria_equipo = categoria_equipo
        self.deposito_seguridad = deposito_seguridad
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if not self.categoria_equipo or not self.categoria_equipo.strip():
            raise ParametroFaltanteError("Debe especificar la categoría del equipo.")
        if self.deposito_seguridad < 0:
            raise DatoInvalidoError("El depósito de seguridad no puede ser negativo.")
        return True

    def calcular_tarifa_base(self, horas: int) -> float:
        return (self._tarifa_hora * horas) + self.deposito_seguridad

    def resumen(self) -> str:
        estado = "Disponible" if self._disponible else "Alquilado"
        return f"Equipo [{self.id}] {self._nombre} ({self.categoria_equipo}) - ${self._tarifa_hora:,.0f}/h [{estado}]"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica o empresarial."""
    def __init__(self, nombre: str, tarifa_hora: float, area_experto: str, nivel_senior: bool = False):
        super().__init__(nombre, tarifa_hora)
        self.area_experto = area_experto
        self.nivel_senior = nivel_senior
        self.validar_parametros()

    def validar_parametros(self) -> bool:
        if not self.area_experto or not self.area_experto.strip():
            raise ParametroFaltanteError("Debe indicar el área de especialidad de la asesoría.")
        return True

    def calcular_tarifa_base(self, horas: int) -> float:
        multiplicador = 1.25 if self.nivel_senior else 1.0
        return (self._tarifa_hora * horas) * multiplicador

    def resumen(self) -> str:
        nivel = "Senior" if self.nivel_senior else "Estándar"
        return f"Asesoría [{self.id}] {self._nombre} ({self.area_experto} - {nivel}) - ${self._tarifa_hora:,.0f}/h"
