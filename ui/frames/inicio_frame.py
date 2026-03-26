import customtkinter as ctk
import time
from tkinter import filedialog
from datetime import datetime
import pandas as pd
from ui.dialogs.emoji_window import EmojiWindow
from ui.dialogs.message_dialogs import MessageDialogs
from core.whatsapp_handler import WhatsAppHandler
from core.excel_processor import ExcelProcessor
from utils.text_utils import normalize_header

class InicioFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, settings, config_manager, process_controller):
        super().__init__(parent)
        self.settings = settings
        self.config_manager = config_manager
        self.process_controller = process_controller
        self.ruta_archivo = ""
        self.whatsapp = WhatsAppHandler()
        
        self._crear_ui()
    
    def _crear_ui(self):
        '''Crea la interfaz del frame de inicio'''
        font_size = self.settings["font_size"]
        
        # Frame superior - Selección de archivo
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(pady=20)
        
        self.lbl_archivo = ctk.CTkLabel(
            top_frame, 
            text="No hay archivo seleccionado", 
            font=("Arial", font_size)
        )
        self.lbl_archivo.grid(row=0, column=0, padx=10)
        
        self.btn_seleccionar = ctk.CTkButton(
            top_frame, 
            text="Seleccionar Excel", 
            command=self._seleccionar_archivo, 
            font=("Arial", font_size)
        )
        self.btn_seleccionar.grid(row=0, column=1, padx=10, pady=5)
        
        # Frame de mensajes (lado a lado)
        frame_mensajes = ctk.CTkFrame(self, fg_color="transparent")
        frame_mensajes.pack(pady=10)
        
        # Mensaje de pago
        frame_msg_pago = ctk.CTkFrame(frame_mensajes, fg_color="transparent")
        frame_msg_pago.pack(side="left", padx=10)
        
        self.lbl_mensaje = ctk.CTkLabel(
            frame_msg_pago, 
            text="Mensaje de falta de pago:", 
            font=("Arial", font_size)
        )
        self.lbl_mensaje.pack(anchor="center", pady=(0, 5))
        
        self.mensaje_text = ctk.CTkTextbox(
            frame_msg_pago, 
            width=480, 
            height=80, 
            font=("Arial", font_size)
        )
        self.mensaje_text.insert("1.0", self.settings["ultimo_mensaje"])
        self.mensaje_text.pack(pady=5)
        
        # Mensaje de vencimiento
        frame_msg_venc = ctk.CTkFrame(frame_mensajes, fg_color="transparent")
        frame_msg_venc.pack(side="left", padx=10)
        
        self.lbl_mensaje_vencimiento = ctk.CTkLabel(
            frame_msg_venc, 
            text="Mensaje de renovación:", 
            font=("Arial", font_size)
        )
        self.lbl_mensaje_vencimiento.pack(anchor="center", pady=(0, 5))
        
        self.mensaje_vencimiento_text = ctk.CTkTextbox(
            frame_msg_venc, 
            width=480, 
            height=80, 
            font=("Arial", font_size)
        )
        self.mensaje_vencimiento_text.insert("1.0", self.settings["ultimo_mensaje_vencimiento"])
        self.mensaje_vencimiento_text.pack(pady=5)
        
        # Texto informativo
        lbl_info_nombre = ctk.CTkLabel(
            self, 
            text="({nombre_cliente} coloca el nombre leído del Excel)", 
            font=("Arial", font_size - 1), 
            text_color="gray"
        )
        lbl_info_nombre.pack(anchor="center", pady=(0, 5))
        
        # Botón emojis
        self.btn_emojis = ctk.CTkButton(
            self, 
            text="Emojis 😊", 
            width=120, 
            command=self._abrir_emojis, 
            font=("Arial", font_size)
        )
        self.btn_emojis.pack(pady=5)
        
        # Frame de botones de inicio
        frame_inicio_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_inicio_btns.pack(pady=10)
        
        self.btn_iniciar = ctk.CTkButton(
            frame_inicio_btns, 
            text="Iniciar envíos por\nfalta de pago", 
            width=180, 
            height=50, 
            command=lambda: self._iniciar_envio("pago"), 
            font=("Arial", font_size), 
            fg_color="#1976D2", 
            hover_color="#135FAE"
        )
        self.btn_iniciar.pack(side="left", padx=5)
        
        self.btn_iniciar_vencimiento = ctk.CTkButton(
            frame_inicio_btns, 
            text="Iniciar envíos por\nrenovación", 
            width=180, 
            height=50, 
            command=lambda: self._iniciar_envio("vencimiento"), 
            font=("Arial", font_size), 
            fg_color="#FF9800", 
            hover_color="#F57C00"
        )
        self.btn_iniciar_vencimiento.pack(side="left", padx=5)
        
        self.btn_iniciar_ambos = ctk.CTkButton(
            frame_inicio_btns, 
            text="Iniciar ambos\nenvíos", 
            width=180, 
            height=50, 
            command=lambda: self._iniciar_envio("ambos"), 
            font=("Arial", font_size), 
            fg_color="#4CAF50", 
            hover_color="#45a049"
        )
        self.btn_iniciar_ambos.pack(side="left", padx=5)
        
        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(self, width=600)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        
        # Botones de control
        frame_control_btns = ctk.CTkFrame(self, fg_color="transparent")
        frame_control_btns.pack(pady=5)
        
        self.btn_limpiar_log = ctk.CTkButton(
            frame_control_btns, 
            text="Limpiar Log", 
            command=self._limpiar_log, 
            font=("Arial", font_size), 
            width=150
        )
        self.btn_limpiar_log.pack(side="left", padx=10)
        
        self.btn_pausa = ctk.CTkButton(
            frame_control_btns, 
            text="Pausar", 
            command=self._pausar_reanudar, 
            font=("Arial", font_size), 
            width=150, 
            fg_color="#ff9800", 
            hover_color="#f57c00", 
            state="disabled"
        )
        self.btn_pausa.pack(side="left", padx=10)
        
        self.btn_detener = ctk.CTkButton(
            frame_control_btns, 
            text="Detener", 
            command=self._detener_proceso, 
            font=("Arial", font_size), 
            width=150, 
            fg_color="#f44336", 
            hover_color="#da190b", 
            state="disabled"
        )
        self.btn_detener.pack(side="left", padx=10)
        
        # Log
        self.log_box = ctk.CTkTextbox(
            self, 
            width=600, 
            height=150, 
            font=("Arial", font_size)
        )
        self.log_box.pack(pady=10)
        self.log_box.insert("1.0", "Registro de envíos…")
        self.log_box.configure(state="disabled")
        
        # Footer
        self.lbl_footer = ctk.CTkLabel(
            self, 
            text="Desarrollado por Tobias Gallo - 2025", 
            font=("Arial", font_size), 
            text_color="#AAAAAA"
        )
        self.lbl_footer.pack(pady=(10, 20))
        
        # Warning
        warning_frame = ctk.CTkFrame(self, fg_color="#ff9800")
        warning_frame.pack(padx=20, pady=5, fill="x")
        
        ctk.CTkLabel(
            warning_frame, 
            text="⚠️ IMPORTANTE", 
            font=("Arial", font_size + 1, "bold"), 
            text_color="#1a1a1a"
        ).pack(pady=(10, 5))
        
        ctk.CTkLabel(
            warning_frame, 
            text="Esta versión solo funciona con WhatsApp Desktop/App.\nAsegúrate de tener WhatsApp abierto y tu sesión iniciada\nantes de comenzar el proceso de envío.", 
            font=("Arial", font_size), 
            text_color="#1a1a1a", 
            justify="center"
        ).pack(padx=10, pady=(0, 10))
    
    # Métodos auxiliares
    def _seleccionar_archivo(self):
        archivo = filedialog.askopenfilename(
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        if archivo:
            self.ruta_archivo = archivo
            self.lbl_archivo.configure(text=f"Archivo seleccionado: {archivo}")
            self._limpiar_log()
    
    def _abrir_emojis(self):
        emoji_window = EmojiWindow(self.master, self.mensaje_text)
        emoji_window.abrir()
    
    def _limpiar_log(self):
        self.progress_bar.set(0)
        self.master.update()
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.insert("1.0", "Registro de envíos…")
        self.log_box.configure(state="disabled")
    
    def _escribir_log(self, texto):
        self.log_box.configure(state="normal")
        contenido = self.log_box.get("1.0", "end").strip()
        if contenido == "Registro de envíos…":
            self.log_box.delete("1.0", "end")
        self.log_box.insert("end", texto)
        self.log_box.configure(state="disabled")
        self.log_box.see("end")
    
    def _pausar_reanudar(self):
        if self.process_controller.esta_corriendo():
            self.process_controller.pausar()
            self._escribir_log("\n⏸️ **EJECUCIÓN PAUSADA**.\n")
            self.btn_pausa.configure(text="Reanudar")
        elif self.process_controller.esta_pausado():
            self.process_controller.reanudar()
            self._escribir_log("\n▶️ **EJECUCIÓN REANUDADA**.\n")
            self.btn_pausa.configure(text="Pausar")
        self._actualizar_botones_control()
    
    def _detener_proceso(self):
        self.process_controller.detener()
        self._escribir_log("\n🛑 **EJECUCIÓN DETENIDA** por el usuario.\n")
        self._actualizar_botones_control()
    
    def _actualizar_botones_control(self):
        if self.process_controller.estado == "IDLE":
            self.btn_iniciar.configure(state="normal")
            self.btn_iniciar_vencimiento.configure(state="normal")
            self.btn_iniciar_ambos.configure(state="normal")
            self.btn_pausa.configure(state="disabled", text="Pausar")
            self.btn_detener.configure(state="disabled")
        elif self.process_controller.estado == "RUNNING":
            self.btn_iniciar.configure(state="disabled")
            self.btn_iniciar_vencimiento.configure(state="disabled")
            self.btn_iniciar_ambos.configure(state="disabled")
            self.btn_pausa.configure(state="normal")
            self.btn_detener.configure(state="normal")
        elif self.process_controller.estado == "PAUSED":
            self.btn_iniciar.configure(state="disabled")
            self.btn_iniciar_vencimiento.configure(state="disabled")
            self.btn_iniciar_ambos.configure(state="disabled")
            self.btn_pausa.configure(state="normal", text="Reanudar")
            self.btn_detener.configure(state="normal")
    
    def actualizar_fuente(self, nuevo_tamano):
        '''Actualiza el tamaño de fuente de todos los widgets'''
        for widget in [self.lbl_archivo, self.lbl_mensaje, self.lbl_mensaje_vencimiento, self.btn_seleccionar, self.btn_iniciar, self.btn_iniciar_vencimiento, self.btn_iniciar_ambos, self.btn_emojis, self.btn_limpiar_log, self.btn_pausa, self.btn_detener, self.lbl_footer]:
            try:
                widget.configure(font=("Arial", nuevo_tamano))
            except:
                pass
        
        self.mensaje_text.configure(font=("Arial", nuevo_tamano))
        self.mensaje_vencimiento_text.configure(font=("Arial", nuevo_tamano))
        self.log_box.configure(font=("Arial", nuevo_tamano))
    
    # ========================================================================
    # PROCESO DE ENVÍO (PARTE 2 - Lógica principal)
    # ========================================================================
    
    def _iniciar_envio(self, tipo="pago"):
        '''Inicia el proceso de envío según el tipo especificado'''
        if self.process_controller.estado != "IDLE":
            return
        
        if not self.ruta_archivo:
            MessageDialogs.mostrar_error(
                self.master, 
                "Error de Archivo", 
                "Seleccione un archivo Excel primero.",
                self.settings["sound_on_finish"]
            )
            return
        
        self.process_controller.iniciar()
        self._actualizar_botones_control()
        
        modo_simulacion = self.settings["mode_simulation"]
        
        # Mensaje inicial según tipo
        if modo_simulacion:
            mensajes = {
                "pago": "[MODO SIMULACIÓN] Envíos por falta de pago - Los mensajes NO se enviarán realmente.\n",
                "vencimiento": "[MODO SIMULACIÓN] Envíos por renovación - Los mensajes NO se enviarán realmente.\n",
                "ambos": "[MODO SIMULACIÓN] Envíos combinados - Los mensajes NO se enviarán realmente.\n"
            }
            self._escribir_log(mensajes.get(tipo, ""))
        
        # Verificar WhatsApp
        if not modo_simulacion:
            self._escribir_log("Verificando sesión de WhatsApp...\n")
            if not self.whatsapp.verificar_sesion():
                MessageDialogs.mostrar_error(
                    self.master,
                    "Error de WhatsApp",
                    "No se puede conectar con WhatsApp Desktop.\n\nAsegúrate de tener WhatsApp abierto y sesión iniciada.",
                    self.settings["sound_on_finish"]
                )
                self._escribir_log("[ERROR] WhatsApp no disponible. Proceso cancelado.\n")
                self.process_controller.detener()
                self._actualizar_botones_control()
                return
        
        # Procesar Excel
        try:
            excel_processor = ExcelProcessor(self.ruta_archivo, self.settings)
            df = excel_processor.leer_y_procesar()
            df, columnas_originales, mapa_columnas = excel_processor.mapear_columnas(df)
            
            # Validar datos
            errores = excel_processor.validar_datos(df, columnas_originales, mapa_columnas)
            if errores:
                mensaje_error = "⚠️ Error en el mapeo de columnas\n\n"
                mensaje_error += "Los datos del Excel no coinciden con el mapeo configurado:\n\n"
                mensaje_error += "\n\n".join(errores)
                mensaje_error += "\n\nPor favor, verifica el mapeo de columnas en Configuraciones\ny asegúrate de que cada columna tenga el tipo de dato correcto."
                
                MessageDialogs.mostrar_error(
                    self.master,
                    "Error de Mapeo de Datos",
                    mensaje_error,
                    self.settings["sound_on_finish"]
                )
                self.process_controller.detener()
                self._actualizar_botones_control()
                return
            
            # Procesar envíos
            self._procesar_envios(df, excel_processor, tipo, modo_simulacion)
            
        except Exception as e:
            self.process_controller.detener()
            self._actualizar_botones_control()
            MessageDialogs.mostrar_error(
                self.master,
                "Error fatal de ejecución",
                f"Ocurrió un error grave:\n{e}",
                self.settings["sound_on_finish"]
            )
            self._escribir_log(f"\n[ERROR FATAL] {e}\n")
    
    def _procesar_envios(self, df, excel_processor, tipo, modo_simulacion):
        '''Procesa los envíos fila por fila'''
        pagado_list = [s.strip() for s in self.settings["excel_paid_status"].strip().lower().split('\n') if s.strip()]
        enviar_list = [s.strip() for s in self.settings["excel_send_status"].strip().lower().split('\n') if s.strip()]
        
        total_filas = len(df)
        enviados = 0
        errores = 0
        no_enviados_usuario = 0
        enviados_vencimiento = 0
        filas_enviadas = []
        filas_vencimiento_enviadas = []
        
        self.progress_bar.set(0)
        
        mensajes_log = {
            "pago": "Iniciando proceso de envío por falta de pago...\n",
            "vencimiento": "Iniciando proceso de envío por renovación/vencimiento...\n",
            "ambos": "Iniciando proceso de envío combinado (falta de pago + renovación)...\n"
        }
        self._escribir_log(mensajes_log.get(tipo, ""))
        
        for i in range(total_filas):
            # Control de flujo
            if self.process_controller.esta_detenido():
                self.process_controller.reset()
                break
            
            while self.process_controller.esta_pausado():
                self.master.update()
                time.sleep(0.1)
                if self.process_controller.esta_detenido():
                    self.process_controller.reset()
                    break
            
            if self.process_controller.estado == "IDLE":
                break
            
            # Procesar fila
            fila = df.iloc[i]
            nombre = str(fila["nombre"]).strip() if not df["nombre"].isna().iloc[i] else ""
            numero = fila["numero"]
            estado = str(fila["pago"]).strip() if not df["pago"].isna().iloc[i] else ""
            vencimiento = fila["vencimiento"]
            fila_excel = i + 2
            
            # Normalizar teléfono
            tel = excel_processor.normalizar_telefono(numero)
            
            if tel == "":
                self._escribir_log(f"[FALTAN DATOS] Fila {fila_excel}: {nombre} - No tiene número.\n")
                self.progress_bar.set((i+1)/total_filas)
                self.master.update()
                continue
            
            # Determinar si enviar por pago
            estado_norm = normalize_header(estado)
            enviar_pago = False
            if tipo in ["pago", "ambos"]:
                enviar_pago = estado_norm in enviar_list and estado_norm not in pagado_list
            
            # Determinar si enviar por vencimiento
            enviar_vencimiento = False
            if tipo in ["vencimiento", "ambos"]:
                enviar_vencimiento = excel_processor.verificar_vencimiento(vencimiento)
            
            # Si no hay nada que enviar, continuar
            if not enviar_pago and not enviar_vencimiento:
                # Mostrar por qué no se envió
                if tipo == "pago":
                    self._escribir_log(f"[NO ENVIADO] Fila {fila_excel}: {nombre} - Estado: {estado}\n")
                elif tipo == "vencimiento":
                    dias_restantes = "desconocido"
                    try:
                        if not df["vencimiento"].isna().iloc[i]:
                            if isinstance(vencimiento, str):
                                fecha_venc = pd.to_datetime(vencimiento, dayfirst=True, errors='coerce')
                            else:
                                fecha_venc = pd.to_datetime(vencimiento, errors='coerce')
                            if not pd.isna(fecha_venc):
                                from datetime import datetime
                                dias_restantes = (fecha_venc - datetime.now()).days
                    except:
                        pass
                    self._escribir_log(f"[NO ENVIADO] Fila {fila_excel}: {nombre} - Vencimiento: {vencimiento} (días restantes: {dias_restantes})\n")
                elif tipo == "ambos":
                    # En modo ambos, mostrar ambos estados
                    self._escribir_log(f"[NO ENVIADO] Fila {fila_excel}: {nombre} - Estado: {estado}, Vencimiento: {vencimiento}\n")
                
                self.progress_bar.set((i+1)/total_filas)
                self.master.update()
                continue
            
            # Enviar mensaje de pago
            if enviar_pago:
                resultado = self._enviar_mensaje_pago(nombre, tel, fila_excel, modo_simulacion)
                if resultado == "enviado":
                    enviados += 1
                    filas_enviadas.append(i)
                elif resultado == "error":
                    errores += 1
                elif resultado == "usuario_cancelo":
                    no_enviados_usuario += 1
                    enviar_pago = False
                
                # Delay si también hay que enviar vencimiento
                if enviar_vencimiento and enviar_pago:
                    self._delay_entre_mensajes()
            
            # Enviar mensaje de vencimiento
            if enviar_vencimiento:
                resultado = self._enviar_mensaje_vencimiento(nombre, tel, fila_excel, modo_simulacion)
                if resultado == "enviado":
                    enviados_vencimiento += 1
                    filas_vencimiento_enviadas.append(i)
                elif resultado == "error":
                    errores += 1
                elif resultado == "usuario_cancelo":
                    no_enviados_usuario += 1
            
            # Delay entre envíos
            if i < total_filas - 1 and not modo_simulacion:
                self._delay_entre_mensajes()
            
            self.progress_bar.set((i+1)/total_filas)
            self.master.update()
        
        # Finalizar proceso
        self.process_controller.detener()
        self._actualizar_botones_control()
        
        # Actualizar Excel si está configurado
        if self.settings["write_msj_enviado"] and len(filas_enviadas) > 0:
            if excel_processor.actualizar_excel_enviados(filas_enviadas, "msj_enviado", 4):
                self._escribir_log(f"\n[EXCEL ACTUALIZADO] Columna 'msj_enviado': {len(filas_enviadas)} registros.\n")
            else:
                self._escribir_log("\n[ERROR] No se pudo actualizar Excel (msj_enviado)\n")
        
        if self.settings["write_msj_vencimiento_enviado"] and len(filas_vencimiento_enviadas) > 0:
            if excel_processor.actualizar_excel_enviados(filas_vencimiento_enviadas, "msj_vencimiento_enviado", 5):
                self._escribir_log(f"\n[EXCEL ACTUALIZADO] Columna 'msj_vencimiento_enviado': {len(filas_vencimiento_enviadas)} registros.\n")
            else:
                self._escribir_log("\n[ERROR] No se pudo actualizar Excel (vencimiento)\n")
        
        # Mostrar resumen SIEMPRE
        self._escribir_log("\nProceso finalizado.\n")
        self._mostrar_resumen(tipo, modo_simulacion, enviados, enviados_vencimiento, errores, no_enviados_usuario)
    
    
    def _enviar_mensaje_pago(self, nombre, tel, fila_excel, modo_simulacion):
        '''Envía un mensaje de pago y retorna el resultado'''
        if self.settings["confirm_each"]:
            if not MessageDialogs.mostrar_confirmar_envio(self.master, nombre, tel, self.settings["sound_on_finish"]):
                self._escribir_log(f"[NO ENVIADO - USUARIO] Fila {fila_excel}: {nombre} ({tel}) - Falta de pago\n")
                return "usuario_cancelo"
        
        mensaje_raw = self.mensaje_text.get("1.0", "end").strip()
        mensaje_final = mensaje_raw.replace("{nombre_cliente}", nombre)
        
        if self.settings["firma_automatica"].strip():
            mensaje_final += "\n\n" + self.settings["firma_automatica"].strip()
        
        if modo_simulacion:
            self._escribir_log(f"[SIMULADO - PAGO] Fila {fila_excel}: {nombre} ({tel})\n")
            return "enviado"
        
        # Intentar enviar con reintentos
        intentos = self.settings["retries"] + 1
        for intento in range(intentos):
            if self.process_controller.esta_detenido():
                break
            
            if intento > 0:
                self._escribir_log(f"[REINTENTO {intento}] Fila {fila_excel}: {nombre}\n")
                time.sleep(2)
            
            if self.whatsapp.enviar_mensaje(tel, mensaje_final):
                self._escribir_log(f"[ENVIADO - PAGO] Fila {fila_excel}: {nombre} ({tel})\n")
                return "enviado"
        
        self._escribir_log(f"[ERROR - PAGO] Fila {fila_excel}: {nombre} ({tel}) - No se pudo enviar\n")
        return "error"
    
    def _enviar_mensaje_vencimiento(self, nombre, tel, fila_excel, modo_simulacion):
        '''Envía un mensaje de vencimiento y retorna el resultado'''
        if self.settings["confirm_each"]:
            if not MessageDialogs.mostrar_confirmar_envio(self.master, nombre, tel, self.settings["sound_on_finish"]):
                self._escribir_log(f"[NO ENVIADO - USUARIO] Fila {fila_excel}: {nombre} ({tel}) - Vencimiento\n")
                return "usuario_cancelo"
        
        mensaje_raw = self.mensaje_vencimiento_text.get("1.0", "end").strip()
        mensaje_final = mensaje_raw.replace("{nombre_cliente}", nombre)
        
        if self.settings["firma_automatica"].strip():
            mensaje_final += "\n\n" + self.settings["firma_automatica"].strip()
        
        if modo_simulacion:
            self._escribir_log(f"[SIMULADO - VENCIMIENTO] Fila {fila_excel}: {nombre} ({tel})\n")
            return "enviado"
        
        # Intentar enviar con reintentos
        intentos = self.settings["retries"] + 1
        for intento in range(intentos):
            if self.process_controller.esta_detenido():
                break
            
            if intento > 0:
                self._escribir_log(f"[REINTENTO {intento}] Fila {fila_excel}: {nombre}\n")
                time.sleep(2)
            
            if self.whatsapp.enviar_mensaje(tel, mensaje_final):
                self._escribir_log(f"[ENVIADO - VENCIMIENTO] Fila {fila_excel}: {nombre} ({tel})\n")
                return "enviado"
        
        self._escribir_log(f"[ERROR - VENCIMIENTO] Fila {fila_excel}: {nombre} ({tel}) - No se pudo enviar\n")
        return "error"
    
    def _delay_entre_mensajes(self):
        '''Aplica delay entre mensajes manteniendo la UI responsiva'''
        delay_restante = self.settings["delay_seconds"]
        while delay_restante > 0 and not self.process_controller.esta_detenido() and self.process_controller.estado != "IDLE":
            tiempo_espera = min(0.1, delay_restante)
            time.sleep(tiempo_espera)
            delay_restante -= tiempo_espera
            self.master.update()
    
    def _mostrar_resumen(self, tipo, modo_simulacion, enviados, enviados_vencimiento, errores, no_enviados_usuario):
        '''Muestra el resumen final del proceso'''
        self._escribir_log("\nProceso finalizado.\n")
        
        popup = ctk.CTkToplevel(self.master)
        popup.title("Proceso finalizado")
        popup.geometry("380x220")
        popup.resizable(False, False)
        popup.grab_set()
        
        try:
            popup.iconbitmap("icono.ico")
        except:
            pass
        
        texto_resultado = "Proceso finalizado.\n\n"
        if modo_simulacion:
            texto_resultado += "[MODO SIMULACIÓN]\n\n"
        
        if tipo == "pago":
            texto_resultado += f"Mensajes de pago enviados: {enviados}"
        elif tipo == "vencimiento":
            texto_resultado += f"Mensajes de vencimiento enviados: {enviados_vencimiento}"
        else:
            texto_resultado += f"Mensajes de pago enviados: {enviados}\n"
            texto_resultado += f"Mensajes de vencimiento enviados: {enviados_vencimiento}"
        
        if errores > 0:
            texto_resultado += f"\nErrores: {errores}"
        if no_enviados_usuario > 0:
            texto_resultado += f"\nNo enviados (usuario): {no_enviados_usuario}"
        
        lbl = ctk.CTkLabel(popup, text=texto_resultado, font=("Arial", self.settings["font_size"] + 3))
        lbl.pack(pady=30)
        
        btn_cerrar = ctk.CTkButton(popup, text="Cerrar", width=120, command=popup.destroy)
        btn_cerrar.pack(pady=10)
        
        if self.settings["sound_on_finish"]:
            self.master.bell()