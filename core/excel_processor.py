import pandas as pd
from datetime import datetime
from utils.text_utils import normalize_header

class ExcelProcessor:
    def __init__(self, ruta_archivo, settings):
        self.ruta_archivo = ruta_archivo
        self.settings = settings
        
    def leer_y_procesar(self):
        '''Lee y procesa el archivo Excel'''
        df = pd.read_excel(self.ruta_archivo)
        df = df.dropna(how="all")
        df = df[df.notna().any(axis=1)]
        df = df.reset_index(drop=True)
        return df
    
    def mapear_columnas(self, df):
        '''Aplica el mapeo de columnas'''
        mapa_columnas = {
            self.settings["columna_1"]: 0,
            self.settings["columna_2"]: 1,
            self.settings["columna_3"]: 2,
            self.settings["columna_4"]: 3
        }
        
        if len(df.columns) < 4:
            raise ValueError("El Excel debe tener al menos 4 columnas.")
        
        columnas_originales = list(df.columns)
        df = df.rename(columns={
            columnas_originales[mapa_columnas["Nombre y Apellido"]]: "nombre",
            columnas_originales[mapa_columnas["Número de Teléfono"]]: "numero",
            columnas_originales[mapa_columnas["Estado"]]: "pago",
            columnas_originales[mapa_columnas["Vencimiento"]]: "vencimiento"
        })
        
        return df, columnas_originales, mapa_columnas
    
    def validar_datos(self, df, columnas_originales, mapa_columnas):
        '''Valida que los datos coincidan con el mapeo'''
        errores = []
        
        # Validar números
        muestra_numeros = df["numero"].head(10)
        numeros_validos = sum(1 for val in muestra_numeros if pd.notna(val) and (str(val).strip().replace(" ", "").replace("-", "").replace("+", "").replace("(", "").replace(")", "").isdigit()or isinstance(val, (int, float))))
        
        if numeros_validos < len(muestra_numeros) * 0.5:
            col_idx = mapa_columnas.get("Número de Teléfono")
            col_nombre = columnas_originales[col_idx] if col_idx is not None else "Desconocida"
            errores.append(f"La columna '{col_nombre}' está configurada como 'Número de Teléfono',\\npero contiene datos que no parecen números de teléfono.")
        
        # Validar estados
        muestra_estados = df["pago"].head(10)
        estados_validos = sum(1 for val in muestra_estados if pd.notna(val) and not str(val).strip().lower().replace(".", "").replace(",", "").isdigit())
        
        if estados_validos < len(muestra_estados) * 0.5:
            col_idx = mapa_columnas.get("Estado")
            col_nombre = columnas_originales[col_idx] if col_idx is not None else "Desconocida"
            errores.append(f"La columna '{col_nombre}' está configurada como 'Estado',\\npero contiene datos que no parecen estados de pago.")
        
        # Validar nombres
        muestra_nombres = df["nombre"].head(10)
        nombres_validos = sum(1 for val in muestra_nombres if pd.notna(val) and any(c.isalpha() for c in str(val).strip()))
        
        if nombres_validos < len(muestra_nombres) * 0.5:
            col_idx = mapa_columnas.get("Nombre y Apellido")
            col_nombre = columnas_originales[col_idx] if col_idx is not None else "Desconocida"
            errores.append(f"La columna '{col_nombre}' está configurada como 'Nombre y Apellido',\\npero contiene datos que no parecen nombres.")
        
        return errores
    
    def normalizar_telefono(self, numero):
        '''Normaliza un número de teléfono'''
        if pd.isna(numero):
            return ""
        
        if isinstance(numero, float):
            tel = str(int(numero))
        else:
            tel = str(numero).strip()
        
        if self.settings["norm_strip_symbols"]:
            tel = "".join(char for char in tel if char.isdigit() or char == '+')
        
        if self.settings["norm_remove_leading_zeros"] and not tel.startswith("+"):
            tel = tel.lstrip("0")
        
        if self.settings["norm_force_plus54"]:
            if not tel.startswith("+"):
                tel = "+" + tel if tel.startswith("54") else "+54" + tel
        
        return tel
    
    def verificar_vencimiento(self, vencimiento):
        '''Verifica si una fecha está dentro del rango de vencimiento'''
        try:
            if pd.notna(vencimiento):
                if isinstance(vencimiento, str):
                    fecha_venc = pd.to_datetime(vencimiento, dayfirst=True, errors='coerce')
                else:
                    fecha_venc = pd.to_datetime(vencimiento, errors='coerce')
                
                if pd.notna(fecha_venc):
                    fecha_actual = datetime.now()
                    dias_diferencia = (fecha_venc - fecha_actual).days
                    return 0 <= dias_diferencia <= self.settings["dias_aviso_vencimiento"]
        except:
            pass
        return False
    
    def actualizar_excel_enviados(self, filas_enviadas, columna_nombre="msj_enviado", columna_pos=4):
        '''Actualiza el Excel con los mensajes enviados'''
        try:
            df_original = pd.read_excel(self.ruta_archivo)
            fecha_hoy = datetime.now().strftime("%d/%m/%Y")
            
            while len(df_original.columns) <= columna_pos:
                df_original[f'Columna_{len(df_original.columns)}'] = ''
            
            columnas = list(df_original.columns)
            columnas[columna_pos] = columna_nombre
            df_original.columns = columnas
            
            for idx in filas_enviadas:
                df_original.at[idx, columna_nombre] = f"Mensaje enviado ({fecha_hoy})"
            
            df_original.to_excel(self.ruta_archivo, index=False)
            return True
        except Exception as e:
            print(f"Error actualizando Excel: {e}")
            return False