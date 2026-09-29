# Guía: correr la campaña de Orchid desde tu PC (Windows)

Los pasos A a F solo LEEN información de Meta. No se crea ni se activa nada.

## A. Instalar Python y FFmpeg (una sola vez)
1. Tecla Windows, escribe `powershell`, Enter.
2. Pega y presiona Enter (si pregunta, responde `Y`):
   ```powershell
   winget install Python.Python.3.12
   winget install Gyan.FFmpeg
   ```
3. Cierra PowerShell y ábrelo de nuevo.
4. Comprueba que se instalaron (deben mostrar un número de versión):
   ```powershell
   python --version
   ffprobe -version
   ```

## B. Descargar los scripts
1. Con tu sesión de GitHub abierta, entra a
   https://github.com/manlizard-sys/metaads2026/tree/claude/orchid-leads-meta-api-0oi9vx
2. Botón verde **Code**, luego **Download ZIP**.
3. Descomprime el ZIP en el Escritorio y renombra la carpeta a `metaads2026`.

## C. Copiar los videos
1. Dentro de `metaads2026`, crea una carpeta llamada `creatives`.
2. Copia ahí todos los videos de `ORCHID PROS\META READY`.

## D. Crear el archivo .env con un token NUEVO
El token anterior quedó expuesto en el chat; genera uno nuevo.
1. Meta Business Settings → Users → System users → Generate new token.
   Permisos: `ads_management`, `ads_read`, `business_management`, `pages_show_list`,
   `pages_read_engagement`, `instagram_basic`.
2. Abre el Bloc de notas y escribe una sola línea:
   ```
   META_ACCESS_TOKEN=pega_aqui_el_token
   ```
3. Archivo → Guardar como:
   - Carpeta: `metaads2026`
   - Tipo: **Todos los archivos (\*.\*)** (si no, se guarda como `.env.txt` y no funciona)
   - Nombre: `.env`

## E. Ejecutar la verificación (solo lectura)
En PowerShell:
```powershell
cd "$env:USERPROFILE\Desktop\metaads2026\scripts"
```
Si ese comando da error, usa este otro:
```powershell
cd "$env:USERPROFILE\OneDrive\Desktop\metaads2026\scripts"
```
Luego:
```powershell
$env:PYTHONUTF8=1
pip install requests
python step1_verify.py > ..\build\step1.txt
python inspect_creatives.py > ..\build\creatives.txt
python step2_audience.py > ..\build\audience.txt
```

## F. Enviar los resultados
Abre `metaads2026\build` y pega en el chat el contenido de:
- `step1.txt`
- `creatives.txt`
- `audience.txt`

Ninguno contiene el token. Si algún comando muestra un error, cópialo tal cual al chat.

## Después (no lo corras todavía)
Con tus respuestas yo completo la configuración (página, Instagram, audiencia, conceptos y copies)
y te aviso cuándo descargar de nuevo la carpeta `scripts`. Recién entonces:
- `python step4_build.py --confirm` crea todo en PAUSED y genera `build\previews.html`.
- `python step5_activate.py --publicar` activa, solo cuando respondas "publicar".
