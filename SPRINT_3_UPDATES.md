# Sprint 3 — Parteneri, Hero Video & Monetizare

## Rezumat

Sprint focusat pe infrastructura de monetizare prin parteneri: modele DB, pagini publice, formular de cerere și administrare completă. Plus suport hero video configurat din Admin.

---

## 1. Hero Video

### Cum funcționează
- Template-ul `home.html` verifică `{% if HERO_VIDEO_URL %}`.
- Valoarea vine din `get_site_setting('HERO_VIDEO_URL')` — caută mai întâi în `SiteSetting` (Admin), apoi fallback la `settings.HERO_VIDEO_URL`.
- Dacă URL-ul e gol/lipsă → gradient fallback neschimbat.

### Cum adaugi video
1. Mergi la **Admin → Site Settings → Add**.
2. Key: `HERO_VIDEO_URL`, Value: URL direct la fișier `.mp4` (ex. CDN sau storage propriu).
3. Salvează → hero-ul afișează video automat.

### Specificații video recomandate
- Format: MP4 (H.264)
- Rezoluție: 1920×1080 sau 1280×720
- Durată: 10–30 secunde (loop)
- Dimensiune: max 8 MB pentru încărcare rapidă
- Video: muted, autoplay, loop, playsinline, opacity 35%

---

## 2. Model Partner

### Fișier: `catalog/models.py`

| Câmp | Tip | Note |
|------|-----|-------|
| `name` | CharField | Obligatoriu |
| `slug` | SlugField | Auto-generat din `name`, unic |
| `partner_type` | choices | dealer, service, accessories, rental, event, other |
| `city` | CharField | Opțional |
| `short_description` | TextField | Max 300 caractere |
| `full_description` | TextField | Opțional |
| `website_url` | URLField | Opțional |
| `telegram_url` | URLField | Opțional |
| `phone` | CharField | Opțional |
| `logo` | ImageField | `partners/logos/` |
| `cover_image` | ImageField | `partners/covers/` |
| `badge_text` | CharField | ex. "Verificat", "Nou" |
| `is_featured` | BooleanField | Apare primul în listare |
| `is_active` | BooleanField | Controlează vizibilitatea publică |
| `order` | PositiveIntegerField | Ordine manuală |

### Cum adaugi primul partener
1. **Admin → Parteneri → Adaugă partener**.
2. Completează: Nume, Tip, Descriere scurtă (obligatorii).
3. Opțional: Logo, Cover, Website, Telegram, Telefon.
4. Bifează `Is active = True` și salvează.
5. Partenerul apare imediat pe `/parteneri/` și în secțiunea homepage.

---

## 3. Model PartnerRequest

### Fișier: `catalog/models.py`

Stochează cererile primite prin formularul public.

| Câmp | Tip |
|------|-----|
| `business_name` | CharField |
| `contact_name` | CharField |
| `phone` | CharField |
| `partner_type` | choices |
| `city` | CharField (opțional) |
| `message` | TextField (opțional) |
| `status` | new → contacted → approved → rejected |
| `created_at` | auto |

---

## 4. Partner Request Flow

1. Utilizatorul vizitează `/parteneri/` și derulează la `#devino-partener`.
2. Completează formularul: business, contact, telefon, tip activitate.
3. Submit → POST → `partner_list` view.
4. Backend:
   - Salvează `PartnerRequest` în DB.
   - `logger.info('PARTNER_REQUEST ...')` → Django logs.
   - `_send_telegram(...)` — Telegram notification (eșecul nu crăpă formularul, e prins în try/except).
5. `messages.success(...)` + redirect înapoi la `/parteneri/`.

### Mesaj Telegram
```
🤝 NOU PARTENER — SeaDoo.ro
🏢 Business: [nume]
👤 Contact: [persoana]
📱 Telefon: [tel]
🏷️ Tip: [tip activitate]
📍 Oraș: [oras sau "nespecificat"]
💬 Mesaj: [mesaj sau "–"]
```

---

## 5. Unde sunt CTA-urile parteneri

| Locație | CTA | Destinație |
|---------|-----|-----------|
| Navbar (desktop + mobile) | **"Parteneri"** | `/parteneri/` |
| Footer — Navigare | **"Parteneri"** | `/parteneri/` |
| Footer — banner CTA | **"Devino partener"** | `/parteneri/#devino-partener` |
| Homepage — parteneri section CTA | **"Aplică pentru listare"** | `/parteneri/#devino-partener` |
| Homepage — placeholder cards | **"Aplică »"** | `/parteneri/#devino-partener` |
| `/parteneri/` — empty state | **"Aplică pentru listare"** | `#devino-partener` |

---

## 6. Admin

### PartnerAdmin
- list: logo preview, name, tip, city, is_featured, is_active, order
- Filtre: tip, city, featured, active
- Câmpuri readonly: slug (auto), created_at, updated_at, logo/cover preview
- Acțiuni: editare directă din list (is_featured, is_active, order)

### PartnerRequestAdmin
- list: business_name, contact_name, phone, partner_type, city, status, created_at
- Filtre: tip, status, city
- Câmpuri readonly: toate (date primite de la utilizatori)
- Acțiuni bulk: **Marchează ca Contactat**, **Marchează ca Aprobat**, **Respinge**

---

## 7. Cum se monetizează

### Acum (Sprint 3)
- Lead-uri directe din `catalog_detail` → Telegram.
- Cereri parteneri din `/parteneri/` → salvate în DB + Telegram.
- Parteneri activi afișați public cu link la pagina dedicată.

### Model de venit
1. **Cerere gratuită** → contact manual → negociere listare.
2. **Listare standard** (viitor): taxă lunară fixă.
3. **Listare featured** (viitor): poziție prioritară în grid.

---

## 8. Migrații

```
catalog/migrations/0011_partner_partnerrequest.py
  + Create model Partner
  + Create model PartnerRequest
```

Rulare: `python manage.py migrate` — aplicată fără erori.

---

## 9. Fișiere modificate

| Fișier | Modificare |
|--------|-----------|
| `catalog/models.py` | +`Partner`, +`PartnerRequest` |
| `catalog/forms.py` | +`PartnerRequestForm` |
| `catalog/admin.py` | +`PartnerAdmin`, +`PartnerRequestAdmin` |
| `catalog/views.py` | +`partner_list`, +`partner_detail`; home: `get_site_setting`, `featured_partners` |
| `catalog/urls.py` | +`parteneri/`, +`parteneri/<slug>/` |
| `catalog/templates/catalog/partner_list.html` | NOU |
| `catalog/templates/catalog/partner_detail.html` | NOU |
| `catalog/templates/catalog/home.html` | DB-driven partners section |
| `catalog/templates/catalog/base.html` | Navbar + footer nav + footer CTA link |
| `catalog/migrations/0011_partner_partnerrequest.py` | NOU |

---

## 10. Ce urmează în Sprint 4

- **Lead model** în DB — stocare cereri de ofertă catalog.
- **Admin leads** cu export CSV.
- **Partner statistics** — număr vizualizări pagină partener.
- **SEO schema markup** — LocalBusiness pentru parteneri.
- **Pagină "Despre" actualizată** cu misiunea proiectului.
- **Sistem de notificări** — email opțional pentru lead-uri.

---

## Restricții respectate

- Nu s-au adăugat plăți.
- Nu s-au modificat fișiere de deployment.
- Toate textele vizibile sunt în română.
- `manage.py check` — 0 erori.
- Eșecul Telegram nu crăpă formularul (`try/except`).
