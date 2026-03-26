import webbrowser
import urllib.parse
import time
import pyautogui

class WhatsAppHandler:
    @staticmethod
    def verificar_sesion():
        '''Verifica que WhatsApp esté disponible'''
        try:
            webbrowser.open("whatsapp://")
            time.sleep(2)
            return True
        except:
            return False
    
    @staticmethod
    def enviar_mensaje(numero, mensaje):
        '''Envía un mensaje por WhatsApp'''
        mensaje_cod = urllib.parse.quote(mensaje)
        url_app = f"whatsapp://send?phone={numero}&text={mensaje_cod}"
        try:
            webbrowser.open(url_app)
            time.sleep(1.5)
            pyautogui.press("enter")
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo abrir WhatsApp: {e}")
            return False