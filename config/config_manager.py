import json
import os
from .settings import DEFAULT_CONFIG

class ConfigManager:
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = os.path.join(self.config_dir, "config_whatsapp.json")
        
    def _get_config_dir(self):
        '''Obtiene el directorio de configuración según el sistema operativo'''
        if os.name == 'nt':  # Windows
            base_path = os.getenv('APPDATA')
            if not base_path:
                base_path = os.path.expanduser('~')
        else:  # Linux/Mac
            base_path = os.path.expanduser('~/.config')
        
        app_dir = os.path.join(base_path, 'RentMind')
        
        try:
            if not os.path.exists(app_dir):
                os.makedirs(app_dir, exist_ok=True)
                print(f"[INFO] Directorio creado: {app_dir}")
            else:
                print(f"[INFO] Directorio ya existe: {app_dir}")
        except Exception as e:
            print(f"[ERROR] No se pudo crear el directorio: {e}")
            app_dir = os.getcwd()
            print(f"[INFO] Usando directorio actual: {app_dir}")
        
        return app_dir
    
    def load(self):
        '''Carga la configuración desde el archivo JSON'''
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    for key in DEFAULT_CONFIG:
                        if key not in config:
                            config[key] = DEFAULT_CONFIG[key]
                    print(f"[INFO] Configuración cargada desde: {self.config_file}")
                    return config
            except Exception as e:
                print(f"Error cargando configuración: {e}")
                return DEFAULT_CONFIG.copy()
        print(f"[INFO] Creando nueva configuración en: {self.config_file}")
        return DEFAULT_CONFIG.copy()
    
    def save(self, config):
        '''Guarda la configuración en el archivo JSON'''
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            print(f"[INFO] Configuración guardada en: {self.config_file}")
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False