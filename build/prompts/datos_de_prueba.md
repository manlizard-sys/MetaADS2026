# Datos para envíos de prueba (regla del usuario, 15 nov 2026)

Toda prueba de formulario (landings, formularios de Meta, GHL) usa SIEMPRE este formato, con un número nuevo en cada envío:

| Campo | Formato | Ejemplo (43) |
|---|---|---|
| Nombre | TEST NN | TEST 43 |
| Teléfono | 30571240NN | 3057124043 |
| Email | hmlizarralde+NN@gmail.com | hmlizarralde+43@gmail.com |

Números ya usados: 43, 44, 45, 46. **Siguiente libre: 47.** Actualiza esta línea cada vez que se use uno.

scripts/ghl.py deja fuera de los reportes los contactos cuyo nombre empieza por "test" (salvo con --include-tests).
