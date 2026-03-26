# RentMind

Aplicación de escritorio para automatizar el envío de mensajes de WhatsApp a clientes de alquiler/suscripciones. Lee datos desde archivos Excel y envía recordatorios personalizados de pagos y vencimientos directamente a través de WhatsApp Desktop.

## Caracteristicas

- **Mensajes en bloque**: Envia recordatorios de deuda y/o vencimiento a multiples clientes de forma automatica
- **Integracion con WhatsApp Desktop**: Usa el esquema de URL nativo (`whatsapp://`) sin necesidad de API externa
- **Procesamiento de Excel**: Carga archivos `.xlsx`/`.xls` con mapeo de columnas personalizable
- **Normalizacion de telefonos**: Convierte distintos formatos al estandar `+54XXXXXXXXX` (Argentina)
- **Modo simulacion**: Prueba el flujo completo sin enviar mensajes reales
- **Control del proceso**: Iniciar, pausar, reanudar y detener en cualquier momento
- **Registro en tiempo real**: Log de cada envio con opcion de exportar a TXT
- **Actualizacion de Excel**: Registra la fecha/hora de envio en el archivo de clientes
- **Configuracion persistente**: Guarda mensajes, ajustes y preferencias entre sesiones

## Requisitos

- Python 3.10+
- WhatsApp Desktop instalado y con sesion activa

### Dependencias Python

```
customtkinter
pandas
pyautogui
openpyxl
```

Instalar con:

```bash
pip install customtkinter pandas pyautogui openpyxl
```

## Uso

```bash
python main.py
```

### Flujo basico

1. **Seleccionar archivo Excel** con los datos de clientes
2. **Mapear columnas**: nombre, telefono, estado de pago, fecha de vencimiento
3. **Configurar mensajes** en la pestana Configuraciones (soporta `{nombre_cliente}` como variable)
4. **Activar Modo Simulacion** para probar sin enviar (recomendado la primera vez)
5. **Hacer clic en Iniciar** y monitorear el progreso en el log

## Estructura del proyecto

```
RentMind/
├── main.py                     # Punto de entrada
├── RentMind.spec               # Configuracion PyInstaller
├── icono.ico                   # Icono de la aplicacion
│
├── config/
│   ├── settings.py             # Constantes y valores por defecto
│   └── config_manager.py       # Carga/guardado de configuracion en JSON
│
├── core/
│   ├── process_controller.py   # Maquina de estados (IDLE/RUNNING/PAUSED)
│   ├── excel_processor.py      # Lectura, validacion y normalizacion del Excel
│   └── whatsapp_handler.py     # Integracion con WhatsApp (URL scheme + PyAutoGUI)
│
├── ui/
│   ├── main_window.py          # Ventana principal y navegacion
│   ├── frames/
│   │   ├── inicio_frame.py     # Frame principal de ejecucion
│   │   ├── config_frame.py     # Frame de ajustes y preferencias
│   │   └── info_frame.py       # Frame de informacion/ayuda
│   └── dialogs/
│       ├── message_dialogs.py  # Popups de error/exito/confirmacion
│       └── emoji_window.py     # Selector de emojis
│
└── utils/
    ├── text_utils.py           # Normalizacion de encabezados
    └── validators.py           # Validacion de inputs
```

## Compilar a ejecutable

Requiere PyInstaller instalado (`pip install pyinstaller`):

```bash
pyinstaller RentMind.spec
```

El ejecutable se genera en `dist/RentMind/`.

## Configuracion

La configuracion se guarda automaticamente en:
- **Windows**: `%APPDATA%\RentMind\config_whatsapp.json`
- **Linux/Mac**: `~/.config/RentMind/config_whatsapp.json`

Incluye mensajes guardados (max 10 por tipo), tema visual, mapeo de columnas y firma personalizada.

## Notas

- Requiere WhatsApp Desktop abierto y con sesion iniciada antes de enviar
- Los datos nunca salen del equipo local (sin API externa, sin nube)
- Enfocado en numeros argentinos (prefijo `+54` por defecto, configurable)
- El delay entre mensajes es configurable (5-60 segundos) para evitar bloqueos

## Autor

Tobias Gallo — 2025
