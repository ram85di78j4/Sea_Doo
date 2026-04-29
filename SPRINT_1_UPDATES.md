# Sprint 1 — UX & Monetizare

## Rezumat

Prima rundă de îmbunătățiri concentrate pe experiența utilizatorului, distribuire conținut, lizibilitate și fundația pentru monetizare prin parteneri.

---

## Modificări implementate

### T1 — Forum: embed imagini din URL-uri

**Fișiere noi:**
- `catalog/templatetags/__init__.py`
- `catalog/templatetags/forum_extras.py`

**Filtru custom:** `render_post_content`
- Toate liniile de text sunt escapate HTML (securitate).
- Liniile care sunt URL-uri standalone de imagini (`.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`) sunt convertite automat în tag-uri `<img>` responsive.
- Imagini cu clase: `max-w-full rounded-xl border border-white/10`, atribut `loading="lazy"`.

**Template-uri actualizate:**
- `catalog/templates/catalog/topic_detail.html`: filtrul aplicat pe conținutul topicului și al răspunsurilor.

---

### T2 — Butoane de distribuire

**Butoane adăugate:** Copiază link, WhatsApp, Telegram (texte în română).

**Pagini actualizate:**
- `catalog/templates/catalog/topic_detail.html`: bara de distribuire în sidebar.
- `catalog/templates/catalog/catalog_detail.html`: butoane inline sub acțiunile principale.

**Detalii tehnice:**
- `copyTopicLink()` / `copyJetskiLink()`: folosesc `navigator.clipboard` cu fallback la `execCommand('copy')`.
- Link-urile WhatsApp/Telegram construite dinamic cu `request.build_absolute_uri`.

---

### T3 — Mobile stats fix

**Fișier:** `catalog/templates/catalog/home.html`

- Rândul de statistici (sub hero) trece de la `flex-wrap` la `grid-cols-2` pe mobile.
- Cifre: `text-xl` pe mobile, `text-3xl` de la `sm:`.
- Etichete: `text-xs` pe mobile, `text-sm` de la `sm:`.
- Spațiere redusă pe mobile: `gap-4`, `mt-10`, `pt-6`.

---

### T4 — Contrast îmbunătățit

**Fișier:** `catalog/templates/catalog/home.html`

- Secțiunea "Pentru cine": text corp schimbat din `text-gray-600` în `text-gray-400`.
- Subtitluri statistici din hero: `text-gray-600` → `text-gray-500`.
- Secțiunea parteneri: text descriere `text-gray-400`.

---

### T5 — Secțiune Parteneri recomandați

**Fișier:** `catalog/templates/catalog/home.html`

Secțiune nouă inserată între "Pentru cine" și "Testimoniale".

**Conținut:**
- 3 carduri placeholder (Dealer jet-ski, Service motoare, Accesorii & echipamente).
- Fiecare card: icon SVG, titlu, subtitlu categoria, descriere, link "Devino partener" → Telegram.
- Banner CTA cu link principal la `https://t.me/+44ZEVTaRYAUxYTg8`.

**Restricții respectate:**
- Fără model de baze de date pentru parteneri.
- Text neutru "Loc disponibil" pe badge.
- Niciun partener real inclus.

---

### T6 — Badge-uri parteneri

Stiluri inline în secțiunea de parteneri (T5):
- Badge "Loc disponibil": `bg-gray-800 border border-gray-700 text-gray-500 text-xs font-semibold px-2.5 py-0.5 rounded-full`.
- Reutilizabil pentru viitoare carduri de parteneri reali.

---

### T7 — Empty states forum îmbunătățite

**Fișiere:**
- `catalog/templates/catalog/forum_index.html`
- `catalog/templates/catalog/forum_category.html`

**Îmbunătățiri:**
- Titlu schimbat din "Nu există subiecte încă" în "Fii primul care deschide o discuție."
- Subtitlu mai angajant cu `text-gray-400` (contrast mai bun).
- 3 sugestii de subiecte afișate ca link-uri (dacă autentificat) sau carduri pasive (vizitator).
- Linkurile de sugestii populează câmpul de titlu al formularului de topic nou via query string `?titlu=`.

---

## Fișiere modificate

| Fișier | Modificare |
|--------|-----------|
| `catalog/templatetags/__init__.py` | Creat (nou) |
| `catalog/templatetags/forum_extras.py` | Creat (nou) |
| `catalog/templates/catalog/topic_detail.html` | Filtru embed imagini, butoane share, JS |
| `catalog/templates/catalog/catalog_detail.html` | Butoane share, JS |
| `catalog/templates/catalog/home.html` | Stats mobile, contrast, secțiune parteneri |
| `catalog/templates/catalog/forum_index.html` | Empty state îmbunătățit |
| `catalog/templates/catalog/forum_category.html` | Empty state îmbunătățit |

---

## Restricții respectate

- Nu s-au adăugat modele noi în baza de date.
- Nu s-au modificat URL-uri sau fișiere de deployment.
- Nu s-au adăugat funcționalități de plată.
- Toate textele vizibile sunt în limba română.
- Nicio pagină existentă nu a fost spartă (`manage.py check` — 0 erori).
