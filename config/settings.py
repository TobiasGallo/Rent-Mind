# Configuración de la aplicación

# Información de la app
APP_TITLE = "RentMind"
APP_VERSION = "1.0"
APP_AUTHOR = "Tobias Gallo"
APP_YEAR = "2025"
APP_EMAIL = "tobiasgallo89@gmail.com"

# Configuración de UI
DEFAULT_WINDOW_SIZE = "1000x950"
DEFAULT_THEME = "dark"
DEFAULT_COLOR_THEME = "blue"

# Icono
ICON_PATH = "icono.ico"

# Configuración predeterminada
DEFAULT_CONFIG = {
    "delay_seconds": 10,
    "retries": 0,
    "sound_on_finish": True,
    "mode_simulation": False,
    "confirm_each": False,
    "theme": "Oscuro",
    "font_size": 13,
    "norm_remove_leading_zeros": True,
    "norm_force_plus54": True,
    "norm_strip_symbols": True,
    "auto_clear_log": False,
    "write_msj_enviado": False,
    "excel_paid_status": "ya pago\npagado\npago",
    "excel_send_status": "no pago\ndeuda\nimpago",
    "columna_1": "Nombre y Apellido",
    "columna_2": "Número de Teléfono",
    "columna_3": "Estado",
    "columna_4": "Vencimiento",
    "mensajes_guardados": [],
    "ultimo_mensaje": "Hola {nombre_cliente}, este es un recordatorio de pago.",
    "firma_automatica": "",
    "mensajes_vencimiento_guardados": [],
    "ultimo_mensaje_vencimiento": "Hola {nombre_cliente}, tu servicio vence pronto. Por favor, renueva tu suscripción.",
    "dias_aviso_vencimiento": 60,
    "write_msj_vencimiento_enviado": False
}

# Emojis disponibles
EMOJIS = ["😀","😁","😂","🤣","😊","😍","😘","😎","🤩","😡","😱","😴","👍","🙏","🎉","🔥","💸","📞","✔️","❌","💬","🤖","🧡","✨","😜","😇","😌","😔","😢","😤","😆","😋"]

# Opciones de columnas
COLUMNAS_OPCIONES = ["Nombre y Apellido", "Número de Teléfono", "Estado", "Vencimiento"]