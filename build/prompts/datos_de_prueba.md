# Datos para envíos de prueba (regla del usuario, 15 nov 2026)

Toda prueba de formulario (landings, formularios de Meta, GHL) usa SIEMPRE este formato, con un número nuevo en cada envío:

| Campo | Formato | Ejemplo (43) |
|---|---|---|
| Nombre | TEST NN | TEST 43 |
| Teléfono | 30571240NN | 3057124043 |
| Email | hmlizarralde+NN@gmail.com | hmlizarralde+43@gmail.com |

Números ya usados: 43, 44, 45, 46; 47, 48 y 49 asignados a las pruebas BF del 16 nov (salud, emprendedores, newsletter); 50 y 51 a la prueba de formularios del 22 nov (salud, emprendedores). **Siguiente libre: 53 (52 reservado para la prueba de la página de agendar del newsletter).** Actualiza esta línea cada vez que se use uno.

scripts/ghl.py deja fuera de los reportes los contactos cuyo nombre empieza por "test" (salvo con --include-tests).
