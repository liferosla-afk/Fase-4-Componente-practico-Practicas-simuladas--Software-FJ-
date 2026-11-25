import logging
import os

# Crear carpeta de logs si no existe
os.makedirs("logs", exist_ok=True)

# Configuración del registro de eventos y errores
logging.basicConfig(
    filename="logs/eventos_sistema.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

def registrar_evento(nivel: str, mensaje: str):
    """Guarda eventos y errores en el archivo de logs."""
    nivel = nivel.upper()
    if nivel == "INFO":
        logging.info(mensaje)
    elif nivel == "WARNING":
        logging.warning(mensaje)
    elif nivel == "ERROR":
        logging.error(mensaje)
    elif nivel == "CRITICAL":
        logging.critical(mensaje)

# --- Jerarquía de Excepciones Personalizadas ---

class ErrorBaseSoftwareFJ(Exception):
    """Excepción raíz para el sistema de Software FJ."""
    pass

class DatoInvalidoError(ErrorBaseSoftwareFJ):
    """Se lanza cuando un dato no cumple el formato o rango esperado."""
    pass

class ParametroFaltanteError(ErrorBaseSoftwareFJ):
    """Se lanza cuando falta un argumento obligatorio."""
    pass

class ServicioNoDisponibleError(ErrorBaseSoftwareFJ):
    """Se lanza cuando se intenta reservar un servicio ocupado o inactivo."""
    pass

class ReservaInvalidaError(ErrorBaseSoftwareFJ):
    """Se lanza ante errores en el flujo o estado de una reserva."""
    pass

class OperacionNoPermitidaError(ErrorBaseSoftwareFJ):
    """Se lanza cuando se intenta una acción prohibida por negocio."""
    pass

class CalculoInconsistenteError(ErrorBaseSoftwareFJ):
    """Se lanza cuando los valores matemáticos dan resultados ilógicos."""
    pass