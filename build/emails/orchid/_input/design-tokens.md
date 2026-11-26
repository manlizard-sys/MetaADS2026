# Design tokens actuales (extraídos del HTML de "Reserva confirmada")

Estos valores salen del código fuente del correo 07 en GHL. Los correos 01, 02, 04, 09 y 10 usan la misma estructura visual. Sirven de punto de partida; se pueden refinar.

## Colores
| Uso | Valor |
|---|---|
| Fondo exterior del correo | `#F3F0FA` |
| Tarjeta principal | `#FFFFFF`, border-radius 14px |
| Cabecera (banda con logo) | `#3F1D83` (morado Orchid) |
| Titular | `#1C1233` |
| Texto de cuerpo | `#4A4460` |
| Etiquetas secundarias / texto pequeño | `#6B6485` |
| Bloque de detalles: fondo | `#F3F0FA` |
| Bloque de detalles: borde izquierdo | `4px solid #FFC857` (amarillo Orchid) |
| Botón principal: fondo | `#FFC857` |
| Botón principal: texto | `#1C1233` |
| Enlace secundario (p. ej. "Cancel your call") | `#3F1D83`, subrayado |
| Separador de la firma | `1px solid #ECE8F7` |
| Pie: fondo | `#1C1233` |
| Pie: texto | `#D9D3F0` |
| Pie: enlaces | `#FFFFFF`, subrayado |

## Tipografía
| Elemento | Estilo |
|---|---|
| Titular | Georgia, 'Times New Roman', serif; 28px; line-height 34px; `#1C1233` |
| Cuerpo | Arial, Helvetica, sans-serif; 16px; line-height 24px; `#4A4460` |
| Etiqueta del bloque ("When", "Where") | Arial 13px; line-height 16px; `#6B6485` |
| Valor del bloque | Arial 16px; line-height 22px; bold; `#1C1233` |
| Botón | Arial 15px; bold; `#1C1233` |
| Línea "Can't make it?" | Arial 14px; line-height 20px; `#6B6485` |
| Despedida ("Talk soon,") | Arial 16px; line-height 24px; `#4A4460` |
| Nombre de la firma | Georgia 18px; `#1C1233` |
| Subfirma ("Orchid") | Arial 14px; line-height 20px; `#6B6485` |
| Pie | Arial 12px; line-height 18px; `#D9D3F0`; centrado |

## Medidas
- Tabla exterior: width 100%, padding de celda `32px 12px`, align center.
- Tarjeta: width 600, max-width 600px, overflow hidden.
- Cabecera: padding `28px 36px`, align left; logo width 130.
- Titular: padding `36px 36px 8px 36px`.
- Párrafo intro: padding `0 36px 24px 36px`.
- Bloque de detalles: celda con padding `0 36px`; dentro, etiqueta `18px 20px 6px 20px`, valor `0 20px 14px 20px` (último valor `0 20px 18px 20px`); border-radius 8px.
- Botón: celda con padding `20px 36px 8px 36px`; enlace `display:inline-block; padding:13px 26px; border-radius:999px; text-decoration:none`.
- Línea "Can't make it?": padding `10px 36px 28px 36px`.
- Firma: padding `0 36px 36px 36px`, border-top 1px `#ECE8F7`.
- Pie: padding `20px 36px`.

## Estructura HTML actual (resumen)
```html
<table role="presentation" width="100%" style="background-color:#F3F0FA;margin:0;padding:0;" cellpadding="0" cellspacing="0" border="0">
  <tr><td style="padding:32px 12px;" align="center">
    <table role="presentation" width="600" style="width:100%;max-width:600px;background-color:#FFFFFF;border-radius:14px;overflow:hidden;" cellpadding="0" cellspacing="0" border="0">
      <!-- Cabecera -->
      <tr><td style="background-color:#3F1D83;padding:28px 36px;" align="left">
        <img src="https://orchidpros.com/wp-content/uploads/2026/01/cropped-cropped-LOGO_WHITE-scaled-1.png" width="130" alt="Orchid" style="height:auto;width:130px;display:block;border:0;">
      </td></tr>
      <!-- Titular -->
      <tr><td style="padding:36px 36px 8px 36px;font-family:Georgia,'Times New Roman',serif;font-size:28px;line-height:34px;color:#1C1233;">
        <p style="margin:0;">You're booked, {{contact.first_name}}.</p>
      </td></tr>
      <!-- Intro -->
      <tr><td style="padding:0 36px 24px 36px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:24px;color:#4A4460;">
        <p style="margin:0;">Your discovery call with Orchid is confirmed. Here are the details.</p>
      </td></tr>
      <!-- Bloque de detalles (When / Where) -->
      <tr><td style="padding:0 36px;">
        <table role="presentation" width="100%" style="background-color:#F3F0FA;border-left:4px solid #FFC857;border-radius:8px;" cellpadding="0" cellspacing="0" border="0">
          <tr><td style="padding:18px 20px 6px 20px;font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:16px;color:#6B6485;">When</td></tr>
          <tr><td style="padding:0 20px 14px 20px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:22px;color:#1C1233;font-weight:bold;"><strong>{{appointment.start_time}} ({{appointment.timezone}})</strong></td></tr>
          <tr><td style="padding:0 20px 6px 20px;font-family:Arial,Helvetica,sans-serif;font-size:13px;line-height:16px;color:#6B6485;">Where</td></tr>
          <tr><td style="padding:0 20px 18px 20px;font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:22px;color:#1C1233;font-weight:bold;"><strong>{{appointment.meeting_location}}</strong></td></tr>
        </table>
      </td></tr>
      <!-- Párrafo -->
      <!-- Botón amarillo: href="{{appointment.reschedule_link}}" -->
      <!-- "Can't make it? Cancel your call" : href="{{appointment.cancellation_link}}" -->
      <!-- Firma con border-top #ECE8F7 -->
      <!-- Pie #1C1233: "N3XUS, LLC d/b/a ORCHID, <dirección>" + enlace orchidpros.com -->
    </table>
  </td></tr>
</table>
```

## Nota sobre la vista previa de GHL
El editor de GHL muestra estos correos con fondo oscuro (tema oscuro de la app). Las capturas de `capturas/` se ven oscuras por eso; el correo real que recibe el contacto es claro (fondo `#F3F0FA`, tarjeta blanca).
