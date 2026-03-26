import customtkinter as ctk
from config.settings import EMOJIS, ICON_PATH

class EmojiWindow:
    def __init__(self, parent, mensaje_text):
        self.parent = parent
        self.mensaje_text = mensaje_text
        self.ventana = None
    
    def abrir(self):
        '''Abre la ventana de emojis'''
        self.ventana = ctk.CTkToplevel(self.parent)
        self.ventana.title("Emojis")
        self.ventana.geometry("400x360")
        self.ventana.grab_set()
        
        try:
            self.ventana.iconbitmap(ICON_PATH)
        except:
            pass
        
        frame_scroll = ctk.CTkScrollableFrame(self.ventana, width=330, height=320)
        frame_scroll.pack(padx=10, pady=10)
        
        max_por_fila = 4
        fila = 0
        columna = 0
        
        for emoji in EMOJIS:
            boton = ctk.CTkButton(
                frame_scroll, 
                text=emoji, 
                font=("Arial", 26), 
                width=60, 
                height=60, 
                fg_color="#1f6aa5", 
                hover_color="#144870",
                command=lambda e=emoji: self._insertar_emoji(e)
            )
            boton.grid(row=fila, column=columna, padx=10, pady=10)
            
            columna += 1
            if columna >= max_por_fila:
                columna = 0
                fila += 1
    
    def _insertar_emoji(self, emoji):
        '''Inserta el emoji y cierra la ventana'''
        self.mensaje_text.insert("insert", emoji)
        self.ventana.destroy()