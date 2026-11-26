# Brief para Claude Code: correos de Orchid en GHL, versión 2 (26 nov 2026)

## Contexto
Los 10 correos de `build/emails/orchid/` (rama `claude/admiring-franklin-wrfknt`) **ya están publicados en GoHighLevel** (sub-cuenta Orchid, Location `r5demglXbNG9LoCszFIw`). Esta versión recoge lo que se aprendió al publicarlos y deja el repo igual a lo que está vivo en GHL.

Claude Code no tiene acceso a GHL. Lo que pase en GHL lo hace Manuel o Claude en el navegador, usando la guía que generes.

Archivos de este paquete:
| Archivo | Contenido |
|---|---|
| `BRIEF.md` | Este documento: tareas y criterios |
| `estado-ghl.md` | Qué está publicado hoy, dónde, con qué asunto, pre-header y remitente |
| `reglas-editores-ghl.md` | Qué conserva y qué borra cada editor de GHL (probado el 26 nov) |
| `merge-fields.md` | Campos dinámicos confirmados en correos reales |

## Tareas

### 1. Ajustar los HTML en `build/emails/orchid/`
1. **URL de empleo:** reemplazar `TODO_URL_CAREERS` por `https://orchidpros.com/work-with-us/` en `01-email-descarte.html` y `04-email-cita-cancelada.html` (y en `index.html`). Que el script `scripts/build_emails.py` la tome de una constante, no a mano.
2. **Etiqueta del encabezado** ("Request received", "Your call is booked", "Call canceled", "New time", "Reminder", etc.): hoy es un `<span>` con `background-color`, `display:inline-block`, `padding` y `border-radius`. Los editores de GHL borran esos estilos del `span` (ver `reglas-editores-ghl.md`). Rehacerla como **tabla anidada con `bgcolor="#FFC857"` en el `<td>`** (más `style="background-color:#FFC857;border-radius:14px;padding:6px 14px;"` en el `td`), sin `span` de fondo. Aplica a los 10 correos y a `_layout.html`.
3. **08 (cancelación):** el botón "Book a new time" apunta siempre al calendario principal (`739uffEjsGH7PH0Zaovn`). Generar **dos variantes**: `08-cal-cancelacion.html` (calendario principal) y `08-cal-cancelacion-newsletter.html` con el enlace `https://api.leadconnectorhq.com/widget/booking/jgKkDzsDyVnOGqklMxaT`. Ojo: el ID del calendario Newsletter tiene una `l` minúscula, no una `I` (`...OGqklMxaT`); el cheatsheet anterior lo tenía con `I`. Verificar con Manuel si hay duda.
4. No cambiar textos, asuntos ni pre-headers salvo lo indicado.

### 2. Reescribir `ghl-cheatsheet.md`
Debe reflejar `estado-ghl.md` y explicar los **dos métodos de publicación**:
- **Workflows (01, 02, 04, 05):** el HTML vive en una **plantilla de GHL (Code editor)**. Para actualizar: Marketing → Emails → Templates → abrir la plantilla → borrar el código → pegar → guardar. **Después** volver a elegir la plantilla en la acción del workflow ("Select existing template"), porque la acción guarda una copia y no se actualiza sola (salvo que se active "Sync Edits to Template"). Guardar el workflow.
- **Calendarios (06 a 10):** pegar en el cuerpo de la notificación → Source code, en **los dos** calendarios.
- **03 (interno):** pegar en la acción "Aviso interno - Nuevo lead" → Source code. El editor le pone Verdana; es aceptable.
- Pendiente fechado: **2 de diciembre de 2026**, cambiar 05 a la plantilla "Orchid · 05 Delegate Brief (sin oferta, desde 2 dic)".

### 3. Vista previa
Actualizar `index.html` para incluir la variante 08-newsletter y comprobar que la etiqueta nueva se ve igual que antes a 600px y 375px.

## Criterio de terminado
- `grep TODO_URL_CAREERS` no devuelve nada.
- Ningún correo usa `<span>` con `background-color`.
- Ningún HTML contiene `<style>`, `<head>`, clases ni `—`.
- `ghl-cheatsheet.md` coincide con `estado-ghl.md` y explica los dos métodos.
- Commit en la misma rama con un mensaje que liste los cambios.

## Fuera de alcance (decisiones de Manuel, no tocar)
- Doble correo al descartar (04 + 08): se dejan los dos.
- Desajuste de dominio (`mail.orchidpros.com` vs `growth@orchidpros.com`): pendiente de configuración en GHL, no en HTML.
- Copias internas de los calendarios (Additional emails): sin cambios.
