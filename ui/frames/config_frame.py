import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from ui.dialogs.message_dialogs import MessageDialogs
from utils.validators import Validators
from config.settings import COLUMNAS_OPCIONES

class ConfigFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, settings, config_manager, inicio_frame):
        super().__init__(parent)
        self.settings = settings
        self.config_manager = config_manager
        self.inicio_frame = inicio_frame  # Referencia al frame de inicio
        
        # Variables de configuración
        self._inicializar_variables()
        self._crear_ui()
    
    def _inicializar_variables(self):
        '''Inicializa las variables de configuración'''
        self.retries_var = tk.StringVar(value=str(self.settings["retries"]))
        self.sound_var = tk.BooleanVar(value=self.settings["sound_on_finish"])
        self.sim_var = tk.BooleanVar(value=self.settings["mode_simulation"])
        self.confirm_var = tk.BooleanVar(value=self.settings["confirm_each"])
        self.zero_var = tk.BooleanVar(value=self.settings["norm_remove_leading_zeros"])
        self.plus54_var = tk.BooleanVar(value=self.settings["norm_force_plus54"])
        self.strip_var = tk.BooleanVar(value=self.settings["norm_strip_symbols"])
        self.auto_clear_var = tk.BooleanVar(value=self.settings["auto_clear_log"])
        self.write_msj_var = tk.BooleanVar(value=self.settings["write_msj_enviado"])
        self.write_msj_venc_var = tk.BooleanVar(value=self.settings["write_msj_vencimiento_enviado"])
        self.theme_var = tk.StringVar(value=self.settings["theme"])
        self.columna_1_var = tk.StringVar(value=self.settings["columna_1"])
        self.columna_2_var = tk.StringVar(value=self.settings["columna_2"])
        self.columna_3_var = tk.StringVar(value=self.settings["columna_3"])
        self.columna_4_var = tk.StringVar(value=self.settings["columna_4"])
    
    def _crear_ui(self):
        '''Crea la interfaz del frame de configuración'''
        font_size = self.settings["font_size"]
        INTERNAL_PADX = 15
        
        # Frame izquierdo
        self.config_left = ctk.CTkFrame(self)
        self.config_left.pack(side="left", padx=12, pady=12, fill="y")
        
        # Frame derecho
        self.config_right = ctk.CTkFrame(self)
        self.config_right.pack(side="left", padx=12, pady=12, fill="both", expand=True)
        
        # ===== CONFIGURACIÓN IZQUIERDA =====
        self._crear_config_izquierda(font_size, INTERNAL_PADX)
        
        # ===== CONFIGURACIÓN DERECHA =====
        self._crear_config_derecha(font_size, INTERNAL_PADX)
    
    def _crear_config_izquierda(self, font_size, padx):
        '''Crea la sección izquierda de configuraciones'''
        # Título
        ctk.CTkLabel(
            self.config_left, 
            text="Ajustes del proceso de envío", 
            font=("Arial", font_size + 1, "bold")
        ).pack(pady=(6, 8), anchor="w", padx=padx)
        
        # Delay
        ctk.CTkLabel(
            self.config_left, 
            text="Delay entre envíos (segundos):", 
            font=("Arial", font_size)
        ).pack(anchor="w", padx=padx)
        
        self.spin_delay = ctk.CTkEntry(self.config_left, width=80, font=("Arial", font_size))
        self.spin_delay.insert(0, str(self.settings["delay_seconds"]))
        self.spin_delay.pack(anchor="w", pady=(2, 2), padx=padx)
        
        ctk.CTkLabel(
            self.config_left, 
            text="Mínimo: 5, Máximo: 60", 
            font=("Arial", 10), 
            text_color="gray"
        ).pack(anchor="w", pady=(0, 8), padx=padx)
        
        # Método de envío
        ctk.CTkLabel(
            self.config_left, 
            text="Método de envío:", 
            font=("Arial", font_size)
        ).pack(anchor="w", padx=padx)
        
        ctk.CTkLabel(
            self.config_left, 
            text="WhatsApp Desktop/App únicamente", 
            text_color="#4CAF50", 
            font=("Arial", font_size - 2, "bold")
        ).pack(anchor="w", pady=(2, 8), padx=padx)
        
        # Reintentos
        ctk.CTkLabel(
            self.config_left, 
            text="Reintentos si falla:", 
            font=("Arial", font_size)
        ).pack(anchor="w", padx=padx)
        
        ctk.CTkOptionMenu(
            self.config_left, 
            values=["0", "1", "2"], 
            variable=self.retries_var, 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(2, 8), padx=padx)
        
        # Checkboxes
        ctk.CTkCheckBox(
            self.config_left, 
            text="Sonido", 
            variable=self.sound_var, 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(2, 8), padx=padx)
        
        ctk.CTkCheckBox(
            self.config_left, 
            text="Modo simulación (no envía)", 
            variable=self.sim_var, 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(2, 8), padx=padx)
        
        ctk.CTkCheckBox(
            self.config_left, 
            text="Confirmar antes de cada envío", 
            variable=self.confirm_var, 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(2, 12), padx=padx)
        
        # Apariencia
        ctk.CTkLabel(
            self.config_left, 
            text="Apariencia / Experiencia", 
            font=("Arial", font_size + 1, "bold")
        ).pack(pady=(14, 8), anchor="w", padx=padx)
        
        ctk.CTkLabel(
            self.config_left, 
            text="Tema:", 
            font=("Arial", font_size)
        ).pack(anchor="w", padx=padx)
        
        ctk.CTkOptionMenu(
            self.config_left, 
            values=["Oscuro", "Claro"], 
            variable=self.theme_var, 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(2, 8), padx=padx)
        
        ctk.CTkLabel(
            self.config_left, 
            text="Tamaño de fuente:", 
            font=("Arial", font_size)
        ).pack(anchor="w", padx=padx)
        
        self.fontsize_entry = ctk.CTkEntry(self.config_left, width=80, font=("Arial", font_size))
        self.fontsize_entry.insert(0, str(self.settings["font_size"]))
        self.fontsize_entry.pack(anchor="w", pady=(2, 2), padx=padx)
        
        ctk.CTkLabel(
            self.config_left, 
            text="Rango: 8-24", 
            font=("Arial", 10), 
            text_color="gray"
        ).pack(anchor="w", pady=(0, 8), padx=padx)
        
        # Botón aplicar
        ctk.CTkButton(
            self.config_left, 
            text="Aplicar configuraciones", 
            command=self._aplicar_configuraciones, 
            fg_color="#4CAF50", 
            hover_color="#45a049", 
            font=("Arial", font_size)
        ).pack(pady=12, padx=padx)
    
    def _crear_config_derecha(self, font_size, padx):
        '''Crea la sección derecha de configuraciones'''
        # Procesamiento del Excel
        ctk.CTkLabel(
            self.config_right, 
            text="Procesamiento del Excel", 
            font=("Arial", font_size + 1, "bold")
        ).pack(pady=(6, 8), anchor="w", padx=padx)
        
        # Normalización de números
        frame_norm = ctk.CTkFrame(self.config_right)
        frame_norm.pack(fill="x", pady=(4, 8), padx=padx)
        
        ctk.CTkLabel(
            frame_norm, 
            text="Normalización de números:", 
            font=("Arial", font_size)
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=6, pady=6)
        
        ctk.CTkCheckBox(
            frame_norm, 
            text="Quitar ceros iniciales", 
            variable=self.zero_var, 
            font=("Arial", font_size)
        ).grid(row=1, column=0, padx=6, pady=4, sticky="w")
        
        ctk.CTkCheckBox(
            frame_norm, 
            text="Forzar prefijo +54", 
            variable=self.plus54_var, 
            font=("Arial", font_size)
        ).grid(row=1, column=1, padx=6, pady=4, sticky="w")
        
        ctk.CTkCheckBox(
            frame_norm, 
            text="Quitar espacios y símbolos", 
            variable=self.strip_var, 
            font=("Arial", font_size)
        ).grid(row=1, column=2, padx=6, pady=4, sticky="w")
        
        # Mapeo de columnas
        self._crear_mapeo_columnas(font_size, padx)
        
        # Estados de pago
        self._crear_estados_pago(font_size, padx)
        
        # Mensajes predefinidos
        self._crear_mensajes_predefinidos(font_size, padx)
        
        # Mensajes de vencimiento
        self._crear_mensajes_vencimiento(font_size, padx)
        
        # Configuraciones adicionales
        self._crear_config_adicionales(font_size, padx)
    
    def _crear_mapeo_columnas(self, font_size, padx):
        '''Crea la sección de mapeo de columnas'''
        ctk.CTkLabel(
            self.config_right, 
            text="Mapeo manual de columnas (opcional):", 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(12, 4), padx=padx)
        
        frame_mapeo = ctk.CTkFrame(self.config_right)
        frame_mapeo.pack(fill="x", pady=(4, 8), padx=padx)
        
        # Labels
        for i, texto in enumerate(["Columna 1:", "Columna 2:", "Columna 3:", "Columna 4:"], 0):
            ctk.CTkLabel(
                frame_mapeo, 
                text=texto, 
                font=("Arial", font_size)
            ).grid(row=0, column=i, padx=6, pady=(4, 2), sticky="w")
        
        # Selectores
        variables = [self.columna_1_var, self.columna_2_var, self.columna_3_var, self.columna_4_var]
        for i, var in enumerate(variables):
            ctk.CTkOptionMenu(
                frame_mapeo, 
                values=COLUMNAS_OPCIONES, 
                variable=var, 
                font=("Arial", font_size), 
                width=135
            ).grid(row=1, column=i, padx=6, pady=(2, 4), sticky="w")
    
    def _crear_estados_pago(self, font_size, padx):
        '''Crea la sección de estados de pago'''
        ctk.CTkLabel(
            self.config_right, 
            text="Estados considerados 'pagado' (uno por línea):", 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(8, 2), padx=padx)
        
        self.text_pagados = ctk.CTkTextbox(
            self.config_right, 
            width=360, 
            height=80, 
            font=("Arial", font_size)
        )
        self.text_pagados.pack(anchor="w", pady=(2, 6), padx=padx)
        self.text_pagados.insert("1.0", self.settings["excel_paid_status"])
        
        ctk.CTkLabel(
            self.config_right, 
            text="Estados que deben enviarse (uno por línea):", 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(6, 2), padx=padx)
        
        self.text_enviar = ctk.CTkTextbox(
            self.config_right, 
            width=360, 
            height=80, 
            font=("Arial", font_size)
        )
        self.text_enviar.pack(anchor="w", pady=(2, 6), padx=padx)
        self.text_enviar.insert("1.0", self.settings["excel_send_status"])
    
    def _crear_mensajes_predefinidos(self, font_size, padx):
        '''Crea la sección de mensajes predefinidos para pago'''
        ctk.CTkLabel(
            self.config_right, 
            text="Mensajes predefinidos para falta de pago", 
            font=("Arial", font_size + 1, "bold")
        ).pack(pady=(12, 6), anchor="w", padx=padx)
        
        frame_mensajes = ctk.CTkFrame(self.config_right)
        frame_mensajes.pack(fill="x", pady=(4, 8), padx=padx)
        
        # Listbox
        self.lista_mensajes = tk.Listbox(
            frame_mensajes, 
            height=5, 
            width=72, 
            font=("Arial", font_size)
        )
        self.lista_mensajes.pack(padx=6, pady=(6, 4))
        
        # Cargar mensajes guardados
        for msg in self.settings["mensajes_guardados"]:
            preview = msg[:60] + "..." if len(msg) > 60 else msg
            self.lista_mensajes.insert("end", preview)
        
        # Botones
        frame_btns = ctk.CTkFrame(frame_mensajes, fg_color="transparent")
        frame_btns.pack(pady=(4, 6))
        
        ctk.CTkButton(
            frame_btns, 
            text="Guardar mensaje", 
            command=self._guardar_mensaje_actual, 
            font=("Arial", font_size), 
            width=160, 
            fg_color="#1976D2", 
            hover_color="#135FAE"
        ).pack(side="left", padx=4)
        
        ctk.CTkButton(
            frame_btns, 
            text="Cargar seleccionado", 
            command=self._cargar_mensaje_seleccionado, 
            font=("Arial", font_size), 
            width=160, 
            fg_color="#4CAF50", 
            hover_color="#45a049"
        ).pack(side="left", padx=4)
        
        ctk.CTkButton(
            frame_btns, 
            text="Eliminar seleccionado", 
            command=self._eliminar_mensaje_seleccionado, 
            font=("Arial", font_size), 
            width=160, 
            fg_color="#f44336", 
            hover_color="#da190b"
        ).pack(side="left", padx=4)
        
        ctk.CTkLabel(
            frame_mensajes, 
            text="(Máximo 10 mensajes)", 
            font=("Arial", 10), 
            text_color="gray"
        ).pack(pady=(4, 6))
    
    def _crear_mensajes_vencimiento(self, font_size, padx):
        '''Crea la sección de mensajes predefinidos para vencimiento'''
        ctk.CTkLabel(
            self.config_right, 
            text="Mensajes predefinidos para renovación", 
            font=("Arial", font_size + 1, "bold")
        ).pack(pady=(12, 6), anchor="w", padx=padx)
        
        frame_mensajes_venc = ctk.CTkFrame(self.config_right)
        frame_mensajes_venc.pack(fill="x", pady=(4, 8), padx=padx)
        
        # Listbox
        self.lista_mensajes_venc = tk.Listbox(
            frame_mensajes_venc, 
            height=5, 
            width=72, 
            font=("Arial", font_size)
        )
        self.lista_mensajes_venc.pack(padx=6, pady=(6, 4))
        
        # Cargar mensajes guardados
        for msg in self.settings["mensajes_vencimiento_guardados"]:
            preview = msg[:60] + "..." if len(msg) > 60 else msg
            self.lista_mensajes_venc.insert("end", preview)
        
        # Botones
        frame_btns = ctk.CTkFrame(frame_mensajes_venc, fg_color="transparent")
        frame_btns.pack(pady=(4, 6))
        
        ctk.CTkButton(
            frame_btns, 
            text="Guardar mensaje", 
            command=self._guardar_mensaje_vencimiento_actual, 
            font=("Arial", font_size), 
            width=160, 
            fg_color="#1976D2", 
            hover_color="#135FAE"
        ).pack(side="left", padx=4)
        
        ctk.CTkButton(
            frame_btns, 
            text="Cargar seleccionado", 
            command=self._cargar_mensaje_vencimiento_seleccionado, 
            font=("Arial", font_size), 
            width=160, 
            fg_color="#4CAF50", 
            hover_color="#45a049"
        ).pack(side="left", padx=4)
        
        ctk.CTkButton(
            frame_btns, 
            text="Eliminar seleccionado", 
            command=self._eliminar_mensaje_vencimiento_seleccionado, 
            font=("Arial", font_size), 
            width=160, 
            fg_color="#f44336", 
            hover_color="#da190b"
        ).pack(side="left", padx=4)
        
        ctk.CTkLabel(
            frame_mensajes_venc, 
            text="(Máximo 10 mensajes)", 
            font=("Arial", 10), 
            text_color="gray"
        ).pack(pady=(4, 6))
    
    def _crear_config_adicionales(self, font_size, padx):
        '''Crea configuraciones adicionales'''
        # Días de aviso
        ctk.CTkLabel(
            self.config_right, 
            text="Días de aviso antes del vencimiento:", 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(6, 2), padx=padx)
        
        self.dias_vencimiento_entry = ctk.CTkEntry(
            self.config_right, 
            width=80, 
            font=("Arial", font_size)
        )
        self.dias_vencimiento_entry.insert(0, str(self.settings["dias_aviso_vencimiento"]))
        self.dias_vencimiento_entry.pack(anchor="w", pady=(2, 6), padx=padx)
        
        # Firma automática
        ctk.CTkLabel(
            self.config_right, 
            text="Firma automática (opcional):", 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(6, 2), padx=padx)
        
        self.firma_entry = ctk.CTkEntry(
            self.config_right, 
            width=360, 
            font=("Arial", font_size)
        )
        self.firma_entry.insert(0, self.settings["firma_automatica"])
        self.firma_entry.pack(anchor="w", pady=(2, 6), padx=padx)
        
        # Logs y monitoreo
        ctk.CTkLabel(
            self.config_right, 
            text="Logs y monitoreo", 
            font=("Arial", font_size + 1, "bold")
        ).pack(pady=(12, 6), anchor="w", padx=padx)
        
        ctk.CTkButton(
            self.config_right, 
            text="Exportar log a TXT", 
            command=self._exportar_log, 
            font=("Arial", font_size), 
            width=180, 
            fg_color="#1976D2", 
            hover_color="#135FAE"
        ).pack(anchor="w", pady=(4, 8), padx=padx)
        
        ctk.CTkCheckBox(
            self.config_right, 
            text="Agregar columna 'msj_enviado' al Excel (si se envió)", 
            variable=self.write_msj_var, 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(6, 4), padx=padx)
        
        ctk.CTkCheckBox(
            self.config_right, 
            text="Agregar columna 'msj_vencimiento_enviado' al Excel", 
            variable=self.write_msj_venc_var, 
            font=("Arial", font_size)
        ).pack(anchor="w", pady=(4, 8), padx=padx)
    
    # ========================================================================
    # MÉTODOS DE FUNCIONALIDAD (PARTE 2)
    # ========================================================================
    
    def _aplicar_configuraciones(self):
        '''Aplica y guarda todas las configuraciones'''
        # Validar delay
        es_valido, delay = Validators.validar_delay(self.spin_delay.get())
        if not es_valido:
            MessageDialogs.mostrar_error(
                self.master,
                "Error de Validación",
                "El Delay entre envíos debe estar entre 5 y 60 segundos.",
                self.settings["sound_on_finish"]
            )
            self.spin_delay.delete(0, "end")
            self.spin_delay.insert(0, str(self.settings["delay_seconds"]))
            return
        
        # Validar tamaño de fuente
        es_valido, fontsize = Validators.validar_fontsize(self.fontsize_entry.get())
        if not es_valido:
            MessageDialogs.mostrar_error(
                self.master,
                "Error de Validación",
                "El Tamaño de fuente debe estar entre 8 y 24.",
                self.settings["sound_on_finish"]
            )
            self.fontsize_entry.delete(0, "end")
            self.fontsize_entry.insert(0, str(self.settings["font_size"]))
            return
        
        # Validar mapeo de columnas
        columnas = [
            self.columna_1_var.get(),
            self.columna_2_var.get(),
            self.columna_3_var.get(),
            self.columna_4_var.get()
        ]
        
        if not Validators.validar_columnas_unicas(columnas):
            MessageDialogs.mostrar_error(
                self.master,
                "Error en Mapeo de Columnas",
                "Has repetido campos en el mapeo de columnas.\n\n"
                "Cada columna debe tener un tipo de dato diferente:\n"
                "- Nombre y Apellido\n"
                "- Número de Teléfono\n"
                "- Estado\n"
                "- Vencimiento\n\n"
                "Por favor, revisa tu configuración y asegúrate de que\n"
                "no haya campos duplicados.",
                self.settings["sound_on_finish"]
            )
            return
        
        # Guardar configuraciones
        try:
            self.settings["delay_seconds"] = delay
            self.settings["font_size"] = fontsize
            self.settings["retries"] = int(self.retries_var.get())
            self.settings["sound_on_finish"] = self.sound_var.get()
            self.settings["mode_simulation"] = self.sim_var.get()
            self.settings["confirm_each"] = self.confirm_var.get()
            self.settings["norm_remove_leading_zeros"] = self.zero_var.get()
            self.settings["norm_force_plus54"] = self.plus54_var.get()
            self.settings["norm_strip_symbols"] = self.strip_var.get()
            self.settings["auto_clear_log"] = self.auto_clear_var.get()
            self.settings["write_msj_enviado"] = self.write_msj_var.get()
            self.settings["write_msj_vencimiento_enviado"] = self.write_msj_venc_var.get()
            self.settings["excel_paid_status"] = self.text_pagados.get("1.0", "end").strip()
            self.settings["excel_send_status"] = self.text_enviar.get("1.0", "end").strip()
            self.settings["columna_1"] = columnas[0]
            self.settings["columna_2"] = columnas[1]
            self.settings["columna_3"] = columnas[2]
            self.settings["columna_4"] = columnas[3]
            self.settings["firma_automatica"] = self.firma_entry.get().strip()
            self.settings["dias_aviso_vencimiento"] = int(self.dias_vencimiento_entry.get())
            self.settings["theme"] = self.theme_var.get()
            
            # Aplicar tema
            if self.settings["theme"] == "Oscuro":
                ctk.set_appearance_mode("dark")
            else:
                ctk.set_appearance_mode("light")
            
            # Actualizar fuente en inicio_frame
            if self.inicio_frame:
                self.inicio_frame.actualizar_fuente(fontsize)
            
            # Guardar
            if self.config_manager.save(self.settings):
                MessageDialogs.mostrar_confirmacion(
                    self.master,
                    "Configuraciones",
                    "Configuraciones guardadas y aplicadas correctamente.",
                    self.settings["sound_on_finish"]
                )
            else:
                MessageDialogs.mostrar_error(
                    self.master,
                    "Error de Guardado",
                    "No se pudieron guardar las configuraciones.",
                    self.settings["sound_on_finish"]
                )
        except Exception as e:
            MessageDialogs.mostrar_error(
                self.master,
                "Error Interno",
                f"Error al aplicar configuraciones:\n{e}",
                self.settings["sound_on_finish"]
            )
    
    def _guardar_mensaje_actual(self):
        '''Guarda el mensaje actual del inicio en la lista'''
        if not self.inicio_frame:
            return
        
        mensaje_actual = self.inicio_frame.mensaje_text.get("1.0", "end").strip()
        
        if not mensaje_actual:
            MessageDialogs.mostrar_error(
                self.master,
                "Error",
                "No hay ningún mensaje para guardar.",
                self.settings["sound_on_finish"]
            )
            return
        
        if len(self.settings["mensajes_guardados"]) >= 10:
            MessageDialogs.mostrar_error(
                self.master,
                "Límite alcanzado",
                "Ya tienes 10 mensajes guardados.\nDebes eliminar uno antes de agregar otro.",
                self.settings["sound_on_finish"]
            )
            return
        
        if mensaje_actual in self.settings["mensajes_guardados"]:
            MessageDialogs.mostrar_error(
                self.master,
                "Mensaje duplicado",
                "Este mensaje ya está guardado.",
                self.settings["sound_on_finish"]
            )
            return
        
        self.settings["mensajes_guardados"].append(mensaje_actual)
        preview = mensaje_actual[:60] + "..." if len(mensaje_actual) > 60 else mensaje_actual
        self.lista_mensajes.insert("end", preview)
        self.config_manager.save(self.settings)
    
    def _cargar_mensaje_seleccionado(self):
        '''Carga el mensaje seleccionado en el textbox del inicio'''
        if not self.inicio_frame:
            return
        
        try:
            indice = self.lista_mensajes.curselection()[0]
            mensaje_seleccionado = self.settings["mensajes_guardados"][indice]
            
            self.inicio_frame.mensaje_text.delete("1.0", "end")
            self.inicio_frame.mensaje_text.insert("1.0", mensaje_seleccionado)
            
            self.settings["ultimo_mensaje"] = mensaje_seleccionado
            self.config_manager.save(self.settings)
            
            MessageDialogs.mostrar_confirmacion(
                self.master,
                "Mensaje cargado",
                "El mensaje ha sido cargado correctamente.",
                self.settings["sound_on_finish"]
            )
        except IndexError:
            MessageDialogs.mostrar_error(
                self.master,
                "Error",
                "Debes seleccionar un mensaje de la lista primero.",
                self.settings["sound_on_finish"]
            )
    
    def _eliminar_mensaje_seleccionado(self):
        '''Elimina el mensaje seleccionado de la lista'''
        try:
            indice = self.lista_mensajes.curselection()[0]
            self.settings["mensajes_guardados"].pop(indice)
            self.lista_mensajes.delete(indice)
            self.config_manager.save(self.settings)
        except IndexError:
            MessageDialogs.mostrar_error(
                self.master,
                "Error",
                "Debes seleccionar un mensaje de la lista primero.",
                self.settings["sound_on_finish"]
            )
    
    def _guardar_mensaje_vencimiento_actual(self):
        '''Guarda el mensaje de vencimiento actual'''
        if not self.inicio_frame:
            return
        
        mensaje_actual = self.inicio_frame.mensaje_vencimiento_text.get("1.0", "end").strip()
        
        if not mensaje_actual:
            MessageDialogs.mostrar_error(
                self.master,
                "Error",
                "No hay ningún mensaje para guardar.",
                self.settings["sound_on_finish"]
            )
            return
        
        if len(self.settings["mensajes_vencimiento_guardados"]) >= 10:
            MessageDialogs.mostrar_error(
                self.master,
                "Límite alcanzado",
                "Ya tienes 10 mensajes guardados.\nDebes eliminar uno antes de agregar otro.",
                self.settings["sound_on_finish"]
            )
            return
        
        if mensaje_actual in self.settings["mensajes_vencimiento_guardados"]:
            MessageDialogs.mostrar_error(
                self.master,
                "Mensaje duplicado",
                "Este mensaje ya está guardado.",
                self.settings["sound_on_finish"]
            )
            return
        
        self.settings["mensajes_vencimiento_guardados"].append(mensaje_actual)
        preview = mensaje_actual[:60] + "..." if len(mensaje_actual) > 60 else mensaje_actual
        self.lista_mensajes_venc.insert("end", preview)
        self.config_manager.save(self.settings)
    
    def _cargar_mensaje_vencimiento_seleccionado(self):
        '''Carga el mensaje de vencimiento seleccionado'''
        if not self.inicio_frame:
            return
        
        try:
            indice = self.lista_mensajes_venc.curselection()[0]
            mensaje_seleccionado = self.settings["mensajes_vencimiento_guardados"][indice]
            
            self.inicio_frame.mensaje_vencimiento_text.delete("1.0", "end")
            self.inicio_frame.mensaje_vencimiento_text.insert("1.0", mensaje_seleccionado)
            
            self.settings["ultimo_mensaje_vencimiento"] = mensaje_seleccionado
            self.config_manager.save(self.settings)
            
            MessageDialogs.mostrar_confirmacion(
                self.master,
                "Mensaje cargado",
                "El mensaje ha sido cargado correctamente.",
                self.settings["sound_on_finish"]
            )
        except IndexError:
            MessageDialogs.mostrar_error(
                self.master,
                "Error",
                "Debes seleccionar un mensaje de la lista primero.",
                self.settings["sound_on_finish"]
            )
    
    def _eliminar_mensaje_vencimiento_seleccionado(self):
        '''Elimina el mensaje de vencimiento seleccionado'''
        try:
            indice = self.lista_mensajes_venc.curselection()[0]
            self.settings["mensajes_vencimiento_guardados"].pop(indice)
            self.lista_mensajes_venc.delete(indice)
            self.config_manager.save(self.settings)
        except IndexError:
            MessageDialogs.mostrar_error(
                self.master,
                "Error",
                "Debes seleccionar un mensaje de la lista primero.",
                self.settings["sound_on_finish"]
            )
    
    def _exportar_log(self):
        '''Exporta el contenido del log a un archivo TXT'''
        if not self.inicio_frame:
            return
        
        contenido_log = self.inicio_frame.log_box.get("1.0", "end").strip()
        
        if contenido_log == "Registro de envíos…" or not contenido_log:
            MessageDialogs.mostrar_error(
                self.master,
                "Log vacío",
                "El log está vacío. No hay nada que exportar.",
                self.settings["sound_on_finish"]
            )
            return
        
        try:
            archivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                initialfile=f"log_whatsapp_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            if archivo:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido_log)
                MessageDialogs.mostrar_confirmacion(
                    self.master,
                    "Exportación exitosa",
                    f"Log exportado correctamente a:\n{archivo}",
                    self.settings["sound_on_finish"]
                )
        except Exception as e:
            MessageDialogs.mostrar_error(
                self.master,
                "Error al exportar",
                f"No se pudo exportar el log:\n{e}",
                self.settings["sound_on_finish"]
            )