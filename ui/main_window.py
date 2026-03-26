import customtkinter as ctk
import os
import sys
from config.settings import *
from config.config_manager import ConfigManager
from core.process_controller import ProcessController
from ui.frames.inicio_frame import InicioFrame
from ui.frames.config_frame import ConfigFrame
from ui.frames.info_frame import InfoFrame

def resource_path(relative_path):
    """Obtiene la ruta absoluta para el recurso, manejando la compilación con PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MainWindow:
    def __init__(self):
        # Inicializar configuración
        self.config_manager = ConfigManager()
        self.settings = self.config_manager.load()
        self.process_controller = ProcessController()
        
        # Configurar apariencia
        ctk.set_appearance_mode(DEFAULT_THEME)
        ctk.set_default_color_theme(DEFAULT_COLOR_THEME)
        
        # Crear ventana principal
        self.app = ctk.CTk()
        self.app.title(APP_TITLE)
        self.app.geometry(DEFAULT_WINDOW_SIZE)
        
        # Aplicar icono
        try:
            # --- MODIFICA ESTA SECCIÓN ---
            icon_path = resource_path("icono.ico")
            self.app.iconbitmap(icon_path)
            # -----------------------------
        except Exception as e:
            # Es bueno imprimir el error para depurar si falla
            print(f"Error al establecer el icono: {e}") 
            pass
        
        # Aplicar tema guardado
        if self.settings["theme"] == "Oscuro":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        
        # Crear UI
        self._crear_ui()
        
        # Protocolo de cierre
        self.app.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _crear_ui(self):
        '''Crea la interfaz de usuario completa'''
        # Frame principal
        main_frame = ctk.CTkFrame(self.app)
        main_frame.pack(fill="both", expand=True, padx=12, pady=8)
        
        # Frame de navegación
        nav_frame = ctk.CTkFrame(main_frame, height=48)
        nav_frame.pack(fill="x", pady=(4, 12))
        
        # Crear frames de contenido
        self.frame_inicio = InicioFrame(
            main_frame, 
            self.settings, 
            self.config_manager, 
            self.process_controller
        )
        
        self.frame_config = ConfigFrame(
            main_frame, 
            self.settings, 
            self.config_manager,
            self.frame_inicio  # Pasar referencia al frame de inicio
        )
        
        self.frame_info = InfoFrame(
            main_frame, 
            self.settings
        )
        
        # Función para cambiar de frame
        def show_frame(frame_to_show):
            for f in (self.frame_inicio, self.frame_config, self.frame_info):
                f.pack_forget()
            frame_to_show.pack(fill="both", expand=True, padx=12, pady=6)
        
        # Botones de navegación
        btn_inicio = ctk.CTkButton(
            nav_frame, 
            text="Inicio", 
            width=140, 
            fg_color="#1976D2", 
            hover_color="#135FAE",
            command=lambda: show_frame(self.frame_inicio)
        )
        btn_inicio.pack(side="left", padx=8, pady=6)
        
        btn_config = ctk.CTkButton(
            nav_frame, 
            text="Configuraciones", 
            width=200, 
            fg_color="#1976D2", 
            hover_color="#135FAE",
            command=lambda: show_frame(self.frame_config)
        )
        btn_config.pack(side="left", padx=8, pady=6)
        
        btn_info = ctk.CTkButton(
            nav_frame, 
            text="Info", 
            width=120, 
            fg_color="#1976D2", 
            hover_color="#135FAE",
            command=lambda: show_frame(self.frame_info)
        )
        btn_info.pack(side="left", padx=8, pady=6)
        
        # Mostrar frame inicial
        show_frame(self.frame_inicio)
        
        # Actualizar botones de control
        self.frame_inicio._actualizar_botones_control()
    
    def _on_closing(self):
        '''Maneja el cierre de la aplicación'''
        # Detener proceso si está corriendo
        self.process_controller.detener()
        
        # Guardar configuraciones finales
        self.settings["excel_paid_status"] = self.frame_config.text_pagados.get("1.0", "end").strip()
        self.settings["excel_send_status"] = self.frame_config.text_enviar.get("1.0", "end").strip()
        self.settings["ultimo_mensaje"] = self.frame_inicio.mensaje_text.get("1.0", "end").strip()
        self.settings["ultimo_mensaje_vencimiento"] = self.frame_inicio.mensaje_vencimiento_text.get("1.0", "end").strip()
        self.config_manager.save(self.settings)
        
        # Cerrar aplicación
        self.app.destroy()
    
    def run(self):
        '''Ejecuta la aplicación'''
        self.app.mainloop()