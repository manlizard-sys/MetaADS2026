# Newsletter Orchid: kit listo para usar

Este kit tiene seis partes:
1. La casilla del newsletter en el formulario.
2. La página `/book`.
3. El workflow "Clic en newsletter sin cita".
4. El link del botón.
5. El newsletter #1.
6. La sincronización diaria.

Los textos que ve el cliente están en inglés; las instrucciones, en español.

---

## 1. Casilla en el formulario (GHL, PC)

1. Ve a **Sites → Forms → "Orchid - Hire a VA" → Edit**.
2. Arrastra un campo **Checkbox** debajo del de SMS.
   - **Label:** `Send me Orchid's weekly newsletter (tips on delegating, no spam)`
   - **Opción:** `Yes`
   - **Required:** no.
3. Haz clic en **Save**.
4. En el **workflow 01 - Lead nuevo**, justo después del trigger, agrega:
   - **If/Else:** "Newsletter checkbox **is** Yes" **AND** "Tags **does not include** job-seeker".
   - Rama **Sí:** acción **Add Tag** → `newsletter`.
5. Haz clic en **Save → Publish**.

## 2. Página `/book` (GHL, PC)

1. Ve a **Sites → Funnels → (el funnel de go.orchidpros.com) → Add New Step**.
   - **Name:** `Book`
   - **Path:** `/book`
2. Usa el mismo estilo de `/hire`, con estos tres elementos:
   - **Título:** `Book Your Free 30-Minute Call`
   - **Texto:** `Tell us which tasks are eating your week. We'll show you how a bilingual assistant on U.S. hours could take them off your plate, and how matching works (about 20 business days).`
   - **Elemento Calendar:** "Orchid - Discovery Call".
3. En **Settings → Tracking code** de la página, deja el mismo pixel de Meta que tiene `/hire`.
4. Haz clic en **Save → Publish**.

## 3. Workflow "03 - Clic en newsletter sin cita" (GHL, PC)

1. **Trigger:** Contact Tag → **Tag Added** = `newsletter-clic`.
2. **Wait:** 2 días.
3. **If/Else:** "Has appointment" (o tag `agendo`).
   - Si ya agendó → **End**.
4. **Send Email**:
   - **From:** Orchid / growth@orchidpros.com
   - **Subject:** `Want me to hold a time for you?`
   - **Body:**
     > Hi {{contact.first_name}},
     >
     > Quick note — if finding 30 minutes is the hard part, reply with two times that work and we'll send the invite.
     >
     > Or pick a slot here: https://go.orchidpros.com/book?utm_source=newsletter&utm_medium=email&utm_campaign=followup
     >
     > — The Orchid team
5. **Remove Tag:** `newsletter-clic`, para que pueda volver a entrar con otro newsletter.
6. **Settings** del workflow:
   - **From** = growth@orchidpros.com.
   - **Allow re-entry:** sí.
7. Haz clic en **Save → Publish**.

## 4. Link del botón en cada newsletter

```
https://go.orchidpros.com/book?utm_source=newsletter&utm_medium=email&utm_campaign=AAAA-MM-DD
```

- Cambia `AAAA-MM-DD` por la fecha de envío.
- **Nunca agregues el correo de la persona en el link.** El pixel de Meta lee la URL completa.

## 5. Newsletter #1 (Mailchimp)

- **Subject:** `The 5 tasks owners hand off first`
- **Preview text:** `And how much of your week they take back.`

> Hi *|FNAME|*,
>
> When owners of law firms, real-estate offices and accounting practices start with an assistant, the same five tasks come off their plate first:
>
> 1. **Inbox triage** — sorting, replying to routine questions, flagging what needs you.
> 2. **Scheduling** — booking, rescheduling and reminding clients.
> 3. **Intake calls** — first conversations with new clients, in English or Spanish.
> 4. **Follow-ups** — the emails and calls that slip when the week gets busy.
> 5. **Paperwork prep** — forms, CRM updates and document collection.
>
> Most owners tell us those five alone are 8–12 hours a week.
>
> If you'd like to see which of your tasks an Orchid assistant could take, book a free 30-minute call.
>
> **[Book a Free Call]** → link from section 4
>
> — The Orchid team

**Antes de enviar:**
- El remitente es **growth@orchidpros.com**.
- Envíate una prueba a ti mismo.
- Revisa que el botón lleve el link con la fecha correcta.

## 6. Sincronización diaria (Claude)

Script: `scripts/mailchimp_sync.py`.

Cada día:
- Agrega a Mailchimp a los leads de GHL con el tag `newsletter`. Nunca agrega a los `job-seeker`.
- Respeta las bajas en ambos sentidos.
- Le pone el tag `newsletter-clic` a quien hizo clic en `/book` y no agendó.

Por defecto solo muestra cuántos contactos movería, sin cambiar nada. Escribe solo con `--apply`.

Necesita estas variables en el entorno:
- `MAILCHIMP_API_KEY`
- `MAILCHIMP_AUDIENCE_ID`
