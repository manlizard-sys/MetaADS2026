# Newsletter Orchid: kit listo para usar (todo en GHL)

Decisión: los newsletters se envían desde GHL. Las audiencias de Mailchimp se migran a GHL con `scripts/mailchimp_to_ghl.py`, y después se cancela Mailchimp.

Este kit tiene seis partes:
1. La casilla del newsletter en el formulario.
2. La página `/book`.
3. El workflow "Clic en newsletter sin cita".
4. El link del botón.
5. El newsletter #1.
6. La migración desde Mailchimp.

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

1. **Trigger:** **Trigger Link Clicked** → el trigger link "Book (newsletter)". Créalo en **Marketing → Trigger Links** con la URL de la sección 4, y úsalo como botón en cada newsletter.
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
5. **Settings** del workflow:
   - **From** = growth@orchidpros.com.
   - **Allow re-entry:** sí.
6. Haz clic en **Save → Publish**.

## 4. Link del botón en cada newsletter

```
https://go.orchidpros.com/book?utm_source=newsletter&utm_medium=email&utm_campaign=AAAA-MM-DD
```

- Cambia `AAAA-MM-DD` por la fecha de envío.
- **Nunca agregues el correo de la persona en el link.** El pixel de Meta lee la URL completa.

## 5. Newsletter #1 (GHL → Marketing → Emails → Campaigns)

- **Subject:** `The 5 tasks owners hand off first`
- **Preview text:** `And how much of your week they take back.`

> Hi {{contact.first_name}},
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
- Destinatarios: la Smart List de la audiencia, excluyendo los tags `mc-baja` y `job-seeker`, y los contactos en DND.
- Las primeras semanas, envía **en tandas** (opción "Send in batches"; por ejemplo 300 por día). Así el dominio nuevo gana reputación y no cae en spam.
- Envíate una prueba a ti mismo.
- Revisa que el botón lleve el link con la fecha correcta.

## 6. Migración desde Mailchimp (Claude)

Script: `scripts/mailchimp_to_ghl.py`.

- Copia cada audiencia de Mailchimp a GHL con un tag:
  - `mc-attorneys`
  - `mc-real-estate`
  - `mc-hiring-colombia`
- Quien se dio de baja o rebotó en Mailchimp entra con **DND de email** y el tag `mc-baja`. Así nunca recibe marketing desde GHL.
- Los tags que ya existen en GHL se conservan.
- Por defecto solo cuenta lo que haría. Importa solo con `--apply`.

Necesita `MAILCHIMP_API_KEY` en el entorno. No hace falta el Audience ID: el script encuentra las audiencias solo.

**Smart Lists en GHL** (Contacts → Smart Lists), una por newsletter:
- **Attorneys:** tag `mc-attorneys`, o Business type = Law firm.
- **Real Estate:** tag `mc-real-estate`, o Business type = Real estate.
- **General Services:** el resto de leads con el tag `newsletter`.
- **Equipo Colombia:** tag `mc-hiring-colombia`. Es solo para comunicaciones internas: nunca la mezcles con los newsletters de clientes.
