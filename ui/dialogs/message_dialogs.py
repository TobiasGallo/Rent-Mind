import customtkinter as ctk
from config.settings import ICON_PATH

class MessageDialogs:
    @staticmethod
    def mostrar_error(parent, titulo, mensaje, sound_on=True):
        '''Muestra un diálogo de error'''
        if sound_on:
            parent.bell()
        
        dialogo = ctk.CTkToplevel(parent)
        dialogo.title(titulo)
        dialogo.geometry("450x200")
        dialogo.resizable(False, False)
        dialogo.grab_set()
        dialogo.focus_set()
        
        try:
            dialogo.iconbitmap(ICON_PATH)
        except:
            pass
        
        lbl = ctk.CTkLabel(dialogo, text=mensaje, font=("Arial", 14), justify="center", wraplength=400)
        lbl.pack(pady=30, padx=20)
        
        btn_cerrar = ctk.CTkButton(dialogo, text="Aceptar", width=120, command=dialogo.destroy, fg_color="#f44336", hover_color="#da190b")
        btn_cerrar.pack(pady=10)
        
        dialogo.protocol("WM_DELETE_WINDOW", dialogo.destroy)
        parent.wait_window(dialogo)
    
    @staticmethod
    def mostrar_confirmacion(parent, titulo, mensaje, sound_on=True):
        '''Muestra un diálogo de confirmación'''
        if sound_on:
            parent.bell()
        
        dialogo = ctk.CTkToplevel(parent)
        dialogo.title(titulo)
        dialogo.geometry("380x180")
        dialogo.resizable(False, False)
        dialogo.grab_set()
        dialogo.focus_set()
        
        try:
            dialogo.iconbitmap(ICON_PATH)
        except:
            pass
        
        lbl = ctk.CTkLabel(dialogo, text="✅ " + mensaje, font=("Arial", 14, "bold"), justify="center", wraplength=350)
        lbl.pack(pady=30, padx=20)
        
        btn_cerrar = ctk.CTkButton(dialogo, text="Aceptar", width=120, command=dialogo.destroy, fg_color="#4CAF50", hover_color="#45a049")
        btn_cerrar.pack(pady=10)
        
        dialogo.protocol("WM_DELETE_WINDOW", dialogo.destroy)
        parent.wait_window(dialogo)
    
    @staticmethod
    def mostrar_confirmar_envio(parent, nombre, numero, sound_on=True):
        '''Muestra diálogo para confirmar envío individual'''
        if sound_on:
            parent.bell()
        
        dialogo = ctk.CTkToplevel(parent)
        dialogo.title("Confirmar envío")
        dialogo.geometry("400x200")
        dialogo.resizable(False, False)
        dialogo.grab_set()
        
        try:
            dialogo.iconbitmap(ICON_PATH)
        except:
            pass
        
        resultado = {"enviar": False}
        
        lbl = ctk.CTkLabel(dialogo, text=f"¿Enviar mensaje a?\n\n{nombre}\n{numero}", font=("Arial", 15), justify="center")
        lbl.pack(pady=30)
        
        frame_btns = ctk.CTkFrame(dialogo, fg_color="transparent")
        frame_btns.pack(pady=10)
        
        def confirmar():
            resultado["enviar"] = True
            dialogo.destroy()
        
        def cancelar():
            resultado["enviar"] = False
            dialogo.destroy()
        
        btn_si = ctk.CTkButton(frame_btns, text="Sí, enviar", width=120, command=confirmar, fg_color="#4CAF50", hover_color="#45a049")
        btn_si.pack(side="left", padx=10)
        
        btn_no = ctk.CTkButton(frame_btns, text="No enviar", width=120, command=cancelar, fg_color="#f44336", hover_color="#da190b")
        btn_no.pack(side="left", padx=10)
        
        dialogo.wait_window()
        return resultado["enviar"]