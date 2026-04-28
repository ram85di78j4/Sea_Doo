# QA Local Testing — Sea-Doo România

## Pornire server local (Windows PowerShell)

```powershell
# 1. Activează virtualenv
.venv\Scripts\activate

# 2. Verificare sistem
$env:PYTHONIOENCODING="utf-8"; python manage.py check

# 3. Aplică migrații
$env:PYTHONIOENCODING="utf-8"; python manage.py migrate

# 4. Date demo
$env:PYTHONIOENCODING="utf-8"; python manage.py seed_data

# 5. Pornește serverul
$env:PYTHONIOENCODING="utf-8"; python manage.py runserver
```

> **Sau, fără activare venv:**
> ```powershell
> $env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py runserver
> ```

---

## URL-uri locale

| Pagină | URL |
|---|---|
| Landing page | http://127.0.0.1:8000/ |
| Catalog jet-ski | http://127.0.0.1:8000/catalog/ |
| Comunitate | http://127.0.0.1:8000/comunitate/ |
| Forum | http://127.0.0.1:8000/forum/ |
| Regulile forumului | http://127.0.0.1:8000/forum/reguli/ |
| Membri | http://127.0.0.1:8000/membri/ |
| Profilul meu | http://127.0.0.1:8000/profile/ |
| Editare profil | http://127.0.0.1:8000/profile/edit/ |
| Register | http://127.0.0.1:8000/register/ |
| Login | http://127.0.0.1:8000/login/ |
| Admin | http://127.0.0.1:8000/admin/ |
| Health check | http://127.0.0.1:8000/health/ |
| Despre | http://127.0.0.1:8000/despre/ |
| Contact | http://127.0.0.1:8000/contact/ |

---

## Conturi demo

| Email | Parolă | Rol |
|---|---|---|
| `demo@seadoo.ro` | `demo1234!` | Utilizator forum demo |
| *(creat manual)* | *(ales de tine)* | Admin/superuser |

> **Creare superuser admin:**
> ```powershell
> $env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py createsuperuser
> ```
> Introdu email, parolă. Username se completează automat cu emailul.

---

## Admin — Ghid de utilizare

### Acces
- URL: http://127.0.0.1:8000/admin/
- Loghează-te cu contul superuser

---

### A. Catalog jet-ski

**Adaugă un jet-ski nou:**
1. Admin → **Catalog** → **Jet Ski-uri** → buton `+ Adaugă jet ski`
2. Completează câmpurile:
   - **Titlu** — ex: `2023 Sea-Doo RXT-X 300`
   - **Brand** — alege din lista: Sea-Doo / Yamaha / Kawasaki
   - **Model** — ex: `RXT-X 300`
   - **An** — ex: `2023`
   - **Motor** — ex: `Rotax 1630 ACE 300 CP`
   - **Putere (CP)** — ex: `300`
   - **Status** — `In colecție` / `Disponibil` / `Vândut` / `Favorit`
   - **Slug** — se completează automat din titlu (nu edita manual)
   - **Descriere scurtă** — text scurt pentru carduri
   - **Povestea** — text lung, afișat pe pagina de detaliu
   - **De ce merită văzut** — text afișat în secțiunea specială
3. **Imagine principală** — click `Alege fișier` → upload JPG/WebP (recomandat 1200×800px)
4. Click **Salvează și continuă editarea**

**Adaugă imagini galeriei:**
1. Pe aceeași pagină, scroll jos la secțiunea **Imagini jet-ski**
2. Click `+ Adaugă o altă imagine`
3. Upload fiecare imagine + opțional un titlu/caption
4. Poți adăuga oricâte imagini
5. Click **Salvează**

**Verificare pe site:**
- http://127.0.0.1:8000/catalog/ — apare cardul
- http://127.0.0.1:8000/catalog/<slug>/ — pagina de detaliu cu galerie

---

### B. Forum

**Categorii forum:**
1. Admin → **Catalog** → **Categorii forum** → `+ Adaugă`
2. Completează: Nume, Slug (auto), Icon (emoji), Descriere
3. Bifează **Activ** pentru a fi vizibilă

**Forum topic previews** (afișate pe /comunitate/ dacă nu există topicuri reale):
1. Admin → **Catalog** → **Topicuri forum (preview)** → `+ Adaugă`

**Moderare topicuri reale** (după ce utilizatorii postează):
1. Admin → **Catalog** → **Topicuri forum (real)**
2. Acțiuni disponibile din lista (checkbox + dropdown „Acțiune"):
   - **📌 Fixează** — pune topic în top
   - **📌 Dezfixează** — scoate din top
   - **🔒 Blochează** — oprește reply-urile
   - **🔓 Deblochează**
   - **🗑 Șterge soft** — ascunde din forum public (nu șterge din DB)
3. Din detaliu topic: editează direct câmpurile `is_pinned`, `is_locked`, `is_deleted`

**Moderare răspunsuri:**
1. Admin → **Catalog** → **Răspunsuri forum**
2. Acțiuni: **Șterge soft** / **Restaurează**
3. Filtru: **Șterse** / **Active**

**Rapoarte:**
1. Admin → **Catalog** → **Rapoarte forum**
2. Culori status: 🟡 Nou / 🟢 Verificat / ⚫ Respins
3. Acțiuni: **Marchează ca verificat** / **Respinge raport**

---

### C. Comunitate

**Waitlist:**
- Admin → **Catalog** → **Liste de așteptare** — vezi înscrierile

**Evenimente:**
1. Admin → **Catalog** → **Previzualizări evenimente** → `+ Adaugă`
2. Completează: Titlu, Slug, Locație, Dată eveniment, Descriere scurtă
3. Upload imagine eveniment (recomandat 800×500px)
4. Bifează **Activ** pentru a apărea pe site

**Testimoniale:**
1. Admin → **Catalog** → **Testimoniale** → `+ Adaugă`
2. Completează: Autor, Text, Rating (1-5 stele), Rol/titlu
3. Bifează **Activ** pentru a fi vizibil

---

### D. Setări site (SiteSettings)

**URL:** Admin → **Catalog** → **Setări site**

| Cheie | Efect |
|---|---|
| `SITE_NAME` | Numele afișat în titlu și header |
| `SITE_TAGLINE` | Tagline-ul de sub logo |
| `SITE_DESCRIPTION` | Meta description pentru SEO |
| `CONTACT_EMAIL` | Email afișat în footer și contact |
| `CONTACT_PHONE` | Telefon afișat în footer |
| `INSTAGRAM_URL` | Link Instagram în footer |
| `TIKTOK_URL` | Link TikTok în footer |
| `YOUTUBE_URL` | Link YouTube în footer |
| `LAUNCH_BANNER_ENABLED` | `true` activează bannerul de lansare |
| `LAUNCH_BANNER_TEXT` | Textul din banner |
| `LAUNCH_BANNER_CTA_TEXT` | Textul butonului din banner |
| `LAUNCH_BANNER_CTA_URL` | URL-ul butonului din banner |
| `HERO_VIDEO_URL` | URL embed video pentru hero |

> **Toate valorile sunt text simplu.** Boolean: `true` sau `false`.
> Schimbările sunt instant — fără restart server.

---

## Checklist admin

- [ ] Loghează-te la `/admin/`
- [ ] Adaugă un jet-ski cu imagine principală și 3 imagini galerie
- [ ] Creează o categorie forum nouă
- [ ] Activează bannerul de lansare (`LAUNCH_BANNER_ENABLED = true`)
- [ ] Schimbă `SITE_NAME` și verifică titlul în browser
- [ ] Verifică lista de așteptare după o testare înregistrare

---

## Checklist catalog

- [ ] `/catalog/` se încarcă corect
- [ ] Filtrare după brand funcționează
- [ ] Filtrare după an funcționează
- [ ] Căutare după text funcționează
- [ ] Pagina de detaliu se deschide cu URL slug
- [ ] Galeria de imagini se deschide (lightbox)
- [ ] Jet-ski fără imagine nu dă eroare (afișează placeholder)
- [ ] „Modele similare" apar jos pe pagina de detaliu
- [ ] Status (In colecție / Disponibil / Vândut) se vede pe card

---

## Checklist forum

- [ ] `/forum/` se încarcă, categoriile apar
- [ ] Search funcționează (caută titlu/autor/categorie)
- [ ] Sort „Cele mai recente" funcționează
- [ ] Sort „Cele mai vizualizate" funcționează
- [ ] Sort „Cele mai comentate" funcționează
- [ ] Filtru categorie funcționează
- [ ] Filtru „Fixate" funcționează
- [ ] Paginare apare la >10 subiecte
- [ ] Pagina categorie `/forum/categorie/<slug>/` afișează topic count și ultima activitate
- [ ] `/forum/topic/<slug>/` afișează topic + statistici (views, reply count)
- [ ] Sidebar „Autor" afișat pe topic detail
- [ ] Sidebar „Subiecte similare" afișat pe topic detail
- [ ] Paginare răspunsuri la >10 replies
- [ ] Creare topic funcționează (login necesar)
- [ ] Reply funcționează
- [ ] Topic blocat nu permite reply
- [ ] Raportare topic funcționează (de la alt cont)
- [ ] Raportare reply funcționează
- [ ] `/forum/reguli/` se afișează

---

## Checklist autentificare

- [ ] `/register/` — creare cont nou funcționează
- [ ] `/login/` — autentificare cu email + parolă
- [ ] `/logout/` — deconectare redirecționează la home
- [ ] `/profile/` — afișează date profil, badges, activitate forum
- [ ] `/profile/edit/` — editare nume, oraș, brand, bio, avatar, show_in_directory
- [ ] `/membri/` — director membri cu card-uri
- [ ] `/membri/<username>/` — profil public cu topics + replies + badges
- [ ] Profil cu `show_in_directory=False` → 404 pe `/membri/<username>/`
- [ ] Admin user fără profil existent → `/profile/` nu dă eroare (get_or_create)

---

## Checklist upload imagini media

### Configurare media în development
Verifică `sea_doo/settings/development.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Pași upload
1. **Jet-ski — imagine principală:**
   - Admin → Jet Ski-uri → alege un model → câmpul `Imagine principală`
   - Upload JPG (recomandat: 1200×800px, <2MB)
   - Salvează → verifică pe `/catalog/` și `/catalog/<slug>/`

2. **Jet-ski — galerie (3 imagini):**
   - Pe aceeași pagină, secțiunea `Imagini jet-ski`
   - Adaugă 3 imagini separate
   - Verifică lightbox pe pagina de detaliu

3. **Eveniment — imagine:**
   - Admin → Previzualizări evenimente → alege eveniment → câmpul `Imagine`
   - Upload JPG (recomandat: 800×500px)
   - Verifică pe `/comunitate/` secțiunea Evenimente

4. **Avatar utilizator:**
   - Loghează-te ca utilizator → `/profile/edit/` → secțiunea Avatar
   - Upload imagine pătrat (recomandat: 200×200px)
   - Verifică pe `/profile/` și `/membri/<username>/`

### Verificare afișare imagini
- [ ] Imaginea principală apare pe card în `/catalog/`
- [ ] Imaginea principală apare mare pe `/catalog/<slug>/`
- [ ] Galeria se deschide corect în lightbox
- [ ] Imaginea evenimentului apare pe `/comunitate/`
- [ ] Avatarul apare pe `/profile/` și pe pagina de topic detail (sidebar autor)

---

## Checklist mobil (375px / 768px)

Deschide DevTools (F12) → Toggle device toolbar → iPhone SE (375px):
- [ ] Navbar se pliază corect, meniu hamburger funcționează
- [ ] Hero text lizibil, buton CTA vizibil
- [ ] Cardurile catalog — 1 coloană pe mobil
- [ ] Forum index — search form utilizabil
- [ ] Topic detail — sidebar autor dispare (coloana principală full-width)
- [ ] Pagina de membri — 1 coloană pe mobil
- [ ] Footer — coloane se stivuiesc vertical

---

## Probleme cunoscute (Known Issues)

_Actualizat: Stage 12_

| # | Problemă | Status |
|---|---|---|
| 1 | Admin users fără MemberProfile → crash pe `/profile/` | ✅ Rezolvat (get_or_create) |
| 2 | ForumTopic real nu exista în seed data | ✅ Rezolvat (adăugat în seed_data) |
| 3 | `--deploy` check arată 6 warnings SSL (normale în dev) | ℹ️ Așteptat, ignoră în dev |
| 4 | Imagini fără upload → tag `<img>` cu src gol în unele templates | ✅ Protejat cu `{% if %}` |

---

## Fixuri aplicate (Fixes Applied)

### Stage 12 (curent)
- `views.py` — `profile_view` și `profile_edit_view` folosesc `get_or_create` în loc de acces direct
- `views.py` — `member_public_profile` — eliminat import redundant inner `User`
- `seed_data.py` — adăugat demo user `demo@seadoo.ro` + 3 `ForumTopic` reale
- `views.py` — `forum_index` cu search+filter+pagination
- `views.py` — `forum_category` cu topic_count + latest_activity + pagination
- `views.py` — `topic_detail` cu reply_count, related_topics, paginated replies
- `topic_detail.html` — layout 2 coloane: main + sidebar (autor + subiecte similare)
- `base.html` footer — coloana Comunitate cu linkuri reale

### Stage 11
- `MemberProfile.get_badges()` → "Membru Beta" ca primă insignă
- `show_in_directory` BooleanField + migration 0009

### Stage 10
- `ForumReport`, `ForumTopic.is_deleted`, `ForumReply.is_deleted` — soft delete
- Admin moderation actions: pin/lock/soft-delete/restore/mark-reviewed

---

## Comenzi utile

```powershell
# Verificare sistem
$env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py check

# Verificare deploy (arată warnings SSL — normale)
$env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py check --deploy

# Creare superuser
$env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py createsuperuser

# Reset seed data (dacă vrei să recreezi toate datele demo)
# ATENȚIE: șterge DB și recreează tot
# del db.sqlite3
# .venv\Scripts\python.exe manage.py migrate
# .venv\Scripts\python.exe manage.py seed_data
# .venv\Scripts\python.exe manage.py createsuperuser

# Colectare fișiere statice (pentru producție)
$env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py collectstatic --noinput

# Shell Django (pentru debug manual)
$env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py shell
```
