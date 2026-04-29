# Sprint 2 — Conversie, Lead-uri & Monetizare

## Rezumat

Sprint focusat pe captarea lead-urilor directe, clarificarea acțiunilor principale și creșterea bazei de monetizare prin parteneri — fără schimbări de arhitectură.

---

## Lead Flow

### Cum funcționează

1. Utilizatorul vizitează o pagină de catalog (`/catalog/<slug>/`).
2. Vede CTA proeminent: **"Vreau ofertă pentru acest model"**.
3. Click → modal se deschide cu form pre-identificat (model + brand în titlu).
4. Completează: **Nume** (obligatoriu), **Telefon** (opțional), **Mesaj scurt**.
5. Submit AJAX → `POST /catalog/<slug>/oferta/` → view `lead_offer`.
6. Backend:
   - Logează `LEAD_OFFER` via `logger.info` (Django logging).
   - Trimite notificare Telegram prin `_send_telegram()` existent.
7. Modal arată confirmarea fără refresh de pagină.

### Mesaj Telegram trimis
```
🔥 NOU LEAD — SeaDoo.ro
📦 Model: [titlu model]
🏷️ Brand: [brand]
👤 Nume: [nume]
📱 Telefon: [telefon sau "necompletat"]
💬 Mesaj: [mesaj sau "–"]
🔗 Utilizator interesat de ofertă.
```

---

## Unde sunt CTA-urile

| Locație | CTA | Destinație |
|---------|-----|-----------|
| Hero homepage | **"Vezi colecția"** | `/catalog/` |
| Hero homepage | **"Intră în forum"** | `/forum/` |
| Catalog detail | **"Vreau ofertă pentru acest model"** | Modal lead form |
| Catalog detail | **"Trimite mesaj"** | `/contact/` |
| Catalog detail | **"Vezi discuțiile din forum"** | `/forum/` |
| Topic forum (sidebar) | **"Vezi colecția"** | `/catalog/` |
| Parteneri (homepage) | **"Aplică pentru listare"** | Telegram |
| Parteneri (homepage) CTA | **"Vrei să apari aici?"** | Telegram |
| Footer (global) | **"Devino partener"** | Telegram |

---

## Cum se monetizează

### Acum (Sprint 2)
- **Lead-uri directe**: utilizatorii trimit cereri de ofertă → notificare imediată pe Telegram.
- **Parteneri**: secțiune vizibilă cu spații disponibile + CTA în footer pe fiecare pagină → conversie prin Telegram.

### Model de venit așteptat
1. **Lead-uri**: captare gratuită → conversie manuală prin proprietar.
2. **Parteneri listați**: taxă lunară fixă pentru listare în secțiunea "Parteneri recomandați".

---

## Modificări implementate

### S2T1+T2+T10 — Lead button, modal și tracking

**Fișiere modificate:**
- `catalog/views.py`: view nou `lead_offer(request, slug)`.
- `catalog/urls.py`: URL nou `catalog/<slug>/oferta/` → `name='lead_offer'`.
- `catalog/templates/catalog/catalog_detail.html`: CTA card + modal HTML/JS.

**Detalii:**
- Formularul trimite AJAX cu `X-Requested-With: XMLHttpRequest`.
- Backend returnează `JsonResponse({'ok': True})` la succes.
- Fallback non-JS: redirect cu `messages.success`.
- Tracking: `logger.info('LEAD_OFFER slug=...')` + `_send_telegram(...)`.
- Modal: deschis/închis cu JS vanilla, fără librării externe, ESC funcționează.
- Input-uri: `py-3` (≥ h-10), forme responsive.

### S2T3 — Partners upgrade

**Fișier:** `catalog/templates/catalog/home.html`

- Badge: `"Loc disponibil"` → `"Spațiu disponibil"` (culoare accent: yellow/cyan).
- Hover state: `border-yellow-400/40 bg-gray-800/60` + icon `group-hover`.
- Link: `"Devino partener"` → `"Aplică pentru listare"` (`font-bold`).

### S2T4 — CTA global parteneri în footer

**Fișier:** `catalog/templates/catalog/base.html`

Banner adăugat deasupra strips-ului de branduri în footer:
- Titlu: "Ești dealer sau service?"
- Text: "Atrage clienți direct din comunitate."
- Buton: "Devino partener" → Telegram.
- Vizibil pe **toate paginile** site-ului.

### S2T5 — Forum → Catalog (cross-link)

**Fișier:** `catalog/templates/catalog/topic_detail.html`

Bloc discret în sidebar sub "Subiecte similare":
- "Cauți un model similar? Catalog complet cu specificații reale."
- Link: "Vezi colecția →"

### S2T6 — Catalog → Forum (cross-link)

**Fișier:** `catalog/templates/catalog/catalog_detail.html`

Bloc între descriere și action buttons:
- "Vrei păreri reale despre acest model? Alți proprietari discută pe forum."
- Link: "Vezi discuțiile din forum →"

### S2T7 — Homepage hero CTA

**Fișier:** `catalog/templates/catalog/home.html`

- Hero secundar: `"Intră în comunitate"` → `"Intră în forum"` (link → `/forum/`).
- Logică: forumul este destinația concretă, mai acționabilă decât "comunitate".

### S2T8 — Microcopy

- `"Scrie-mi acum"` → `"Trimite mesaj"` (mai direct, fără persoana I).
- `"Devino partener"` → `"Aplică pentru listare"` pe cardurile parteneri.
- CTA lead: `"Completează rapid — revenim în aceeași zi."` (social proof + urgență).

---

## Ce urmează în Sprint 3

- **Model `Partner`** în baza de date: slug, logo, descriere, tip (dealer/service/accesorii), URL, is_active.
- **Admin** pentru gestionarea partenerilor listați.
- **Pagină dedicată parteneri** (`/parteneri/`) cu carduri reale.
- **Stocare lead-uri** în DB (model `Lead` cu model, nume, telefon, mesaj, created_at).
- **Admin pentru lead-uri** cu export CSV.
- **Statistici simple**: număr lead-uri pe model, trafic pe pagini cheie.
- **SEO on-page**: meta tags îmbunătățite, schema markup pentru catalog.

---

## Restricții respectate

- Nu s-au adăugat modele noi în baza de date.
- Nu s-au modificat fișiere de deployment.
- Toate textele vizibile sunt în română.
- `manage.py check` — 0 erori.
