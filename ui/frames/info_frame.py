import customtkinter as ctk
from config.settings import APP_TITLE, APP_VERSION, APP_AUTHOR, APP_YEAR, APP_EMAIL

class InfoFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.settings = settings
        self._crear_contenido()
    
    def _crear_contenido(self):
        font_size = self.settings["font_size"]
        
        # Título
        ctk.CTkLabel(
            self, 
            text="Información de la aplicación", 
            font=("Arial", font_size + 3, "bold")
        ).pack(pady=12)
        
        # Información general
        info_frame = ctk.CTkFrame(self, fg_color="#1f6aa5")
        info_frame.pack(padx=20, pady=10, fill="x")
        ctk.CTkLabel(
            info_frame, 
            text=f"{APP_TITLE}\nVersión: {APP_VERSION}\nDesarrollado por: {APP_AUTHOR}\nAño: {APP_YEAR}", 
            justify="center", 
            font=("Arial", font_size)
        ).pack(padx=20, pady=15)
        
        # Características principales
        self._crear_seccion(
            "✨ Características principales",
            "• Envío automático de mensajes por WhatsApp Desktop/App\n"
            "• Gestión de mensajes por falta de pago\n"
            "• Avisos automáticos de vencimiento y renovación de contratos\n"
            "• Mapeo personalizable de columnas del Excel\n"
            "• Normalización automática de números telefónicos\n"
            "• Modo simulación para pruebas sin envíos reales\n"
            "• Sistema de confirmación individual opcional antes de cada envío\n"
            "• Exportación de logs detallados en formato TXT\n"
            "• Reintentos automáticos en caso de error"
        )
        
        # Guía rápida
        self._crear_seccion(
            "📋 Guía rápida de uso",
            "1. Selecciona tu archivo Excel con los datos\n"
            "2. Configura los mensajes personalizados (usa variables como {nombre_cliente})\n"
            "3. Ajusta las configuraciones según tus necesidades\n"
            "4. Asegúrate de tener WhatsApp Desktop/App abierto\n"
            "5. Inicia el proceso de envío y supervisa el progreso en pantalla"
        )
        
        # Formato del Excel
        self._crear_seccion(
            "📊 Formato del Excel",
            "El archivo Excel debe contener al menos 4 columnas:\n"
            "• Nombre y Apellido del cliente\n"
            "• Número de Teléfono (formato: +54..., 54... o sin prefijo)\n"
            "• Estado del pago (ej: pago, pendiente, deuda)\n"
            "• Fecha de Vencimiento (formato: DD/MM/YYYY)\n\n"
            "Puedes configurar qué columna corresponde a cada dato en Configuraciones."
        )
        
        # Consejos útiles
        self._crear_seccion(
            "💡 Consejos útiles",
            "• Usa el modo simulación antes de enviar mensajes reales\n"
            "• Guarda tus mensajes más usados en la sección de predefinidos\n"
            "• Configura un delay apropiado entre envíos (recomendado: mínimo 10 segundos)\n"
            "• Revisa el log para detectar errores o envíos fallidos\n"
            "• Exporta el log al finalizar para tener un registro completo\n"
            "• La normalización de números ayuda a estandarizar formatos\n"
            "• Usa la firma automática para mensajes recurrentes"
        )
        
        # Soporte
        soporte_frame = ctk.CTkFrame(self, fg_color="#2d2d2d")
        soporte_frame.pack(padx=30, pady=(20, 5), fill="x")
        
        ctk.CTkLabel(
            soporte_frame, 
            text="📞 Soporte", 
            font=("Arial", self.settings["font_size"] + 2, "bold")
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            soporte_frame, 
            text=f"Para soporte técnico, reportar errores o sugerencias contacta al desarrollador\nEmail: {APP_EMAIL}", 
            justify="center", 
            font=("Arial", font_size)
        ).pack(padx=20, pady=(0, 15))
        
        # Versión
        ctk.CTkLabel(
            self, 
            text=f"Versión {APP_VERSION} - {APP_YEAR}", 
            font=("Arial", font_size - 1), 
            text_color="gray"
        ).pack(pady=(20, 20))
    
    def _crear_seccion(self, titulo, contenido):
        '''Crea una sección de información'''
        font_size = self.settings["font_size"]
        
        ctk.CTkLabel(
            self, 
            text=titulo, 
            font=("Arial", font_size + 2, "bold")
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(padx=30, pady=5, fill="x")
        
        ctk.CTkLabel(
            frame, 
            text=contenido, 
            justify="left", 
            font=("Arial", font_size)
        ).pack(anchor="w")