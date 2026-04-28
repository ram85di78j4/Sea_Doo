# SeaDoo.ro — Jet-Ski România

Premium website pentru pasionații de jet-ski din România.  
Colecție personală Sea-Doo + fundația pentru prima comunitate serioasă de jet-ski din România.

---

## Stack tehnic

| Componentă | Tehnologie |
|---|---|
| Backend | Python / Django 6.x |
| Bază de date | SQLite (dev) · PostgreSQL (prod via `DATABASE_URL`) |
| Frontend | Tailwind CSS (CDN) |
| Static files (prod) | WhiteNoise |
| Server WSGI (prod) | Gunicorn |
| Admin | Django Admin customizat |
| Upload media | Pillow + Django media |
| Config env | python-decouple (`.env`) |

---

## Setup pe Windows / PyCharm

### 1. Creează și activează mediul virtual

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalează dependențele

```powershell
pip install -r requirements.txt
```

### 3. Aplică migrările

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Creează superuser pentru Admin

```powershell
python manage.py createsuperuser
```

### 5. (Opțional) Încarcă date de test

```powershell
$env:PYTHONIOENCODING="utf-8"; python manage.py seed_data
```

Aceasta va crea 5 jet-ski-uri de test (4 Sea-Doo + 1 Yamaha) cu descrieri în română, slug auto-generat și câmpul `why_worth_seeing` completat.

### 6. Pornește serverul

```powershell
python manage.py runserver
```

Deschide în browser: **http://127.0.0.1:8000**  
Admin panel: **http://127.0.0.1:8000/admin/**

---

## Structura proiectului

```
Sea_Doo/
├── sea_doo/                  # Configurare Django
│   ├── settings/             # Setari splituite Stage 5
│   │   ├── __init__.py
│   │   ├── base.py           # Setari comune
│   │   ├── development.py    # Dev (SQLite, DEBUG=True)
│   │   └── production.py     # Prod (WhiteNoise, HTTPS, decouple)
│   ├── settings.py           # Ignorat (shadowed de pachet)
│   ├── urls.py
│   ├── wsgi.py               # Default: settings.production
│   └── asgi.py
│
├── catalog/                  # Aplicatia principala
│   ├── models.py
│   ├── admin.py
│   ├── forms.py
│   ├── views.py              # incl. health_check, sitemap_xml, robots_txt
│   ├── urls.py
│   ├── migrations/
│   ├── management/commands/seed_data.py
│   └── templates/catalog/
│
├── staticfiles/              # generat de collectstatic (ignorat de git)
├── media/                    # uploaduri (ignorat de git)
├── .env.example              # template variabile de mediu
├── .gitignore
├── manage.py                 # Default: settings.development
├── requirements.txt
└── README.md
```

---

## Secțiuni website

| Secțiune | Descriere |
|---|---|
| **Hero** | Full-screen cinematic cu animații wave |
| **Despre** | Storytelling în română |
| **Colecție** | Grid cu jet-ski-uri favorite |
| **Sea-Doo Featured** | Secțiune premium Sea-Doo |
| **Forum Preview** | 7 categorii + CTA forum.domain.ro |
| **Contact** | Formular → salvat în DB → vizibil în Admin |

---

## Models Django

### `JetSki`
```
title, brand, model, year, engine, horsepower, condition,
status (in_collection / available / sold / favorite),
short_description, full_description, why_worth_seeing,
slug (auto-generat), main_image, video_url,
created_at, updated_at
```

### `JetSkiImage`
```
jetski (FK), image, caption, order, created_at
```
Imagini galerie per jet-ski. Gestionate inline în Admin.

### `ContactMessage`
```
name, email, message, created_at, is_read
```

---

## URL-uri disponibile

| URL | Nume | Descriere |
|---|---|---|
| `/` | `home` | Homepage |
| `/catalog/` | `catalog_list` | Catalog cu search + filtre |
| `/catalog/<slug>/` | `catalog_detail` | Detaliu jet-ski (slug-based) |
| `/comunitate/` | `comunitate` | Comunitate + formular înscriere waitlist |
| `/despre/` | `about` | Pagina despre proiect |
| `/contact/` | `contact_page` | Formular de contact |
| `/termeni/` | `terms` | Termeni și condiții |
| `/confidentialitate/` | `privacy` | Politica de confidențialitate |
| `/admin/` | — | Panel administrare |
| `/sitemap.xml` | `sitemap` | Sitemap XML generat dinamic |
| `/robots.txt` | `robots_txt` | Robots.txt cu referință sitemap |

---

## Admin Panel

URL: `/admin/`  

- **JetSki** — list display, filtre, căutare, slug readonly, preview imagine, inline galerie
- **JetSkiImage** — administrare directă galerie cu preview
- **ForumCategory** — categorii forum cu ordine, icon, inline topic previews
- **ForumTopicPreview** — subiecte demo (titlu, autor, răspunsuri, vizualizări, fixat)
- **CommunityWaitlist** — înscrieri waitlist (readonly, filtre brand/owns_jetski)
- **EventPreview** — evenimente (titlu, locație, dată, imagine, is_active)
- **Testimonial** — testimoniale (nume, oraș, mesaj, rating 1-5, is_active)
- **ContactMessage** — mesaje primite, marcare ca citit (bulk action)

---

## Video Hero (opțional)

Pentru a activa fundalul video pe homepage, setează în `sea_doo/settings.py`:

```python
HERO_VIDEO_URL = '/media/hero.mp4'  # sau URL extern
```

Dacă e gol (`''`), se folosește gradientul implicit.

---

## Setare mediu de lucru (Settings)

`manage.py runserver` folosește automat `sea_doo.settings.development` (fără configurație suplimentară).

Pentru PyCharm, setează **Environment Variables** în Run Configuration:
```
DJANGO_SETTINGS_MODULE=sea_doo.settings.development
```

---

## Deployment pe VPS (Ubuntu/Debian, fără Docker)

### 1. Pregătește serverul

```bash
sudo apt update && sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx -y
```

### 2. Clonează proiectul

```bash
cd /var/www
git clone https://github.com/user/sea_doo.git
cd sea_doo
```

### 3. Creează mediul virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Configurează variabilele de mediu

```bash
cp .env.example .env
nano .env          # editează cu valorile reale
```

Minimum necesar în `.env`:
```
SECRET_KEY=un-secret-lung-si-random-generat
DEBUG=False
ALLOWED_HOSTS=seadoo.ro,www.seadoo.ro
CSRF_TRUSTED_ORIGINS=https://seadoo.ro,https://www.seadoo.ro
```

### 5. Colectează fișierele statice

```bash
DJANGO_SETTINGS_MODULE=sea_doo.settings.production python manage.py collectstatic --noinput
```

### 6. Aplică migrările

```bash
DJANGO_SETTINGS_MODULE=sea_doo.settings.production python manage.py migrate
```

### 7. Creează superuser

```bash
DJANGO_SETTINGS_MODULE=sea_doo.settings.production python manage.py createsuperuser
```

### 8. (Opțional) Încărcă date demo

```bash
DJANGO_SETTINGS_MODULE=sea_doo.settings.production python manage.py seed_data
```

### 9. Pornește cu Gunicorn

```bash
DJANGO_SETTINGS_MODULE=sea_doo.settings.production \
  .venv/bin/gunicorn sea_doo.wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 3 \
  --access-logfile /var/log/gunicorn/access.log \
  --error-logfile /var/log/gunicorn/error.log \
  --daemon
```

Sau prin systemd — creează `/etc/systemd/system/seadoo.service`:

```ini
[Unit]
Description=Sea-Doo Gunicorn
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/sea_doo
EnvironmentFile=/var/www/sea_doo/.env
Environment="DJANGO_SETTINGS_MODULE=sea_doo.settings.production"
ExecStart=/var/www/sea_doo/.venv/bin/gunicorn sea_doo.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable seadoo
sudo systemctl start seadoo
```

### 10. Configurează Nginx

`/etc/nginx/sites-available/seadoo`:

```nginx
server {
    listen 80;
    server_name seadoo.ro www.seadoo.ro;

    location /media/ {
        alias /var/www/sea_doo/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/seadoo /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### 11. SSL cu Certbot

```bash
sudo certbot --nginx -d seadoo.ro -d www.seadoo.ro
```

Certbot adaugă automat redirect HTTP→HTTPS în configul Nginx.

### 12. Verificare finală

```bash
curl https://seadoo.ro/health/
# {"status": "ok", "app": "Sea_Doo"}
```

---

## PostgreSQL (opțional prod)

```bash
pip install psycopg2-binary
```

Adaugă în `.env`:
```
DATABASE_URL=postgres://seadoo_user:parola@localhost:5432/seadoo_db
```

---

## Extindere viitoare

**Stage 2 — Completat:**
- [x] Galerie multiple imagini per jet-ski (JetSkiImage + inline admin + lightbox)
- [x] Slug auto-generat pentru URL-uri prietenoase
- [x] SEO meta tags + Open Graph în toate paginile
- [x] Video background hero (configurabil din settings.py)
- [x] Search full-text în catalog (titlu, marcă, model, motor)
- [x] Pagini statice: Despre, Contact, Termeni, Confidențialitate
- [x] Detaliu jet-ski: secțiuni "Povestea modelului" + "De ce merită văzut" + CTA

**Stage 3 — Completat:**
- [x] Modele: ForumCategory, ForumTopicPreview, CommunityWaitlist
- [x] Admin complet pentru toate modelele noi (inline topics în categorie)
- [x] Pagina /comunitate/ cu hero, beneficii, categorii, topicuri recente, formular waitlist
- [x] Navigare actualizată: Acasă, Catalog, Comunitate, Despre, Contact
- [x] Homepage: categorii forum dinamice din DB, CTA către /comunitate/
- [x] Formular înscriere waitlist cu validare și mesaj confirmare
- [x] FORUM_EXTERNAL_URL în settings.py (placeholder pentru Flarum)
- [x] Seed data: 9 categorii forum + 10 topic previews demo

**Stage 4 — Completat:**
- [x] Modele noi: EventPreview, Testimonial + admin cu preview imagine
- [x] Secțiune trust cards pe homepage (4 carduri: colecție, comunitate, modele, forum)
- [x] Secțiune evenimente pe homepage și /comunitate/#evenimente
- [x] Secțiune testimoniale pe homepage (rating stele, avatar inițiale)
- [x] Stats row homepage: contori dinamici din DB
- [x] sitemap.xml generat dinamic (toate paginile + catalog slugs)
- [x] robots.txt cu Disallow /admin/ și referință sitemap
- [x] Contact page: CTA-uri pentru catalog, comunitate, colaborări, evenimente
- [x] Seed data: 3 evenimente + 3 testimoniale demo
- [x] Migration: 0003_eventpreview_testimonial

**Demo launch checklist:**
- [ ] Adaugă imagini reale din Admin → Jet-Ski-uri (main_image per model)
- [ ] Adaugă imagini pentru evenimente din Admin → Evenimente
- [ ] Setează `HERO_VIDEO_URL` dacă ai un clip video de fundal
- [ ] Actualizează `FORUM_EXTERNAL_URL` cu domeniul real când e pregătit
- [ ] Înlocuiește `contact@seadoo.ro` cu emailul real în `contact_page.html`
- [ ] Rulează `manage.py createsuperuser` pentru contul de admin
- [ ] Setează `DEBUG = False` și `ALLOWED_HOSTS` înainte de deployment
- [ ] Configurează PostgreSQL pentru producție (vezi secțiunea de mai jos)

**Stage 5 — Completat:**
- [x] Settings splituite: `base.py`, `development.py`, `production.py`
- [x] `manage.py` → default `sea_doo.settings.development`
- [x] `wsgi.py` + `asgi.py` → default `sea_doo.settings.production`
- [x] `python-decouple` pentru toate variabilele de mediu sensibile
- [x] `WhiteNoise` pentru static files în producție (middleware + storage)
- [x] Security headers complete în `production.py` (HSTS, SSL redirect, CSRF, X-Frame)
- [x] `DATABASE_URL` optional via `dj-database-url` (fallback SQLite)
- [x] `.env.example` cu toate variabilele documentate
- [x] `.gitignore` complet (`.env`, `staticfiles/`, `media/`, `__pycache__/` etc.)
- [x] `requirements.txt` actualizat cu noile dependențe
- [x] Endpoint `/health/` → `{"status": "ok", "app": "Sea_Doo"}`
- [x] Ghid complet deployment VPS (systemd + Nginx + Certbot) în README

**Stage 6 — Completat:**
- [x] Model `SiteSetting` (key/value/description/is_public/updated_at) + `get_site_setting()` helper
- [x] Context processor `catalog/context_processors.py` — injectează setările în toate template-urile
- [x] Constante identitate în `settings/base.py`: `SITE_NAME`, `SITE_TAGLINE`, `SITE_DESCRIPTION`, `CONTACT_EMAIL`, `CONTACT_PHONE`, `INSTAGRAM_URL`, `TIKTOK_URL`, `YOUTUBE_URL`
- [x] `SiteSettingAdmin` în `/admin/` cu preview valoare și `list_editable`
- [x] `base.html`: title/meta/OG folosesc variabile dinamice din context
- [x] Navbar: tagline vizibil pe desktop lângă logo
- [x] Footer: 4 coloane — brand+social icons, navigare, comunitate+forum, contact
- [x] Footer: social icons condiționale (Instagram, TikTok, YouTube) + disclaimer legal
- [x] `home.html`: hero copy premium — "Acolo unde pasiunea devine legendă"
- [x] `home.html`: about copy — "Nu e un hobby. E un stil de viață."
- [x] `home.html`: secțiune "Branduri urmărite" — Sea-Doo, Yamaha WaveRunner, Kawasaki
- [x] `home.html`: secțiune "Pentru cine este comunitatea" — 5 tipuri de membri
- [x] `contact_page.html`: email dinamic din `{{ CONTACT_EMAIL }}`
- [x] Migration: `0004_sitesetting`

**Cum personalizezi brandul și rețelele sociale:**
1. `/admin/` → **Setari site** → adaugă cheia (ex: `INSTAGRAM_URL`) cu valoarea dorită
2. Asigură-te că `is_public = True`
3. Modificarea apare imediat în toate paginile, fără restart server

**Stage 7 — Completat:**
- [x] Banner lansare admin-editabil (`LAUNCH_BANNER_ENABLED/TEXT/CTA_TEXT/CTA_URL`) în `base.html`
- [x] Secțiune pre-lansare pe homepage — "Comunitatea se deschide în curând" cu 2 CTA-uri
- [x] `CommunityWaitlist.wants_updates` BooleanField + `CommunityWaitlistForm` actualizat
- [x] Formular comunitate: checkbox "Vreau să primesc noutăți", bloc inline succes (`?joined=1`), 3 trust icons
- [x] Logo: iconiță SVG wave în cerc galben (fără emoji, fără logo oficial)
- [x] Navbar + footer: `{{ SITE_NAME }}` dinamic, fără hardcoded "SeaDoo.ro"
- [x] `home.html` meta/title/OG din context processor (`SITE_NAME`, `SITE_TAGLINE`, `SITE_DESCRIPTION`)
- [x] Bloc final CTA pe homepage — "Prima comunitate jet-ski premium din România"
- [x] `seed_data` extins cu 7 `SiteSetting` demo (SITE_NAME, SITE_TAGLINE, CONTACT_EMAIL, banner)
- [x] Migration: `0005_communitywaitlist_wants_updates`

**Cum schimbi numele public al platformei:**
1. `/admin/` → **Setari site** → editează cheia `SITE_NAME`
2. Același lucru pentru `SITE_TAGLINE` și `SITE_DESCRIPTION`
3. Apare imediat în navbar, footer, title, OG tags — fără nicio modificare de cod

**Cum activezi bannerul de lansare:**
1. `/admin/` → **Setari site** → setează `LAUNCH_BANNER_ENABLED` = `true`
2. Editează `LAUNCH_BANNER_TEXT` cu mesajul dorit
3. Opțional: editează `LAUNCH_BANNER_CTA_TEXT` și `LAUNCH_BANNER_CTA_URL`
4. Dezactivează oricând: setează `LAUNCH_BANNER_ENABLED` = `false`

**Checklist copy final înainte de lansare publică:**
- [ ] Rulează `manage.py seed_data` pentru valori demo
- [ ] Actualizează `SITE_NAME` și `SITE_TAGLINE` cu brandul final în `/admin/`
- [ ] Setează `CONTACT_EMAIL` cu adresa reală
- [ ] Adaugă `INSTAGRAM_URL`, `TIKTOK_URL`, `YOUTUBE_URL` când conturile sunt gata
- [ ] Activează `LAUNCH_BANNER_ENABLED = true` cu 48h înainte de lansare
- [ ] Dezactivează bannerul după lansarea oficială

**Stage 8 — Completat:**
- [x] Model `MemberProfile` (OneToOne → User, city, owns_jetski, favorite_brand, bio, avatar, created_at)
- [x] `signals.py` — auto-creare profil la înregistrare (`post_save` pe User)
- [x] `apps.py` — `ready()` conectează semnalele
- [x] `RegistrationForm` (email ca username, validare unicitate email, save profil)
- [x] `ProfileEditForm` (first_name + câmpuri profil + avatar upload)
- [x] `EmailLoginForm` (label "Email" în loc de "Username")
- [x] Vederile: `register_view`, `profile_view` (`@login_required`), `profile_edit_view`
- [x] URL-uri: `/register/`, `/login/`, `/logout/`, `/profile/`, `/profile/edit/`
- [x] `settings/base.py`: `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`
- [x] `MemberProfileAdmin` cu `search_fields` pe email, city, brand
- [x] `base.html` navbar: Autentificare / Creează cont (guest) | Profil / Deconectare (auth)
- [x] `comunitate.html`: mesaj "Bine ai venit, {name}" + CTA profil (auth) | waitlist + register CTA (guest)
- [x] 4 template-uri noi: `register.html`, `login.html`, `profile.html`, `profile_edit.html`
- [x] Migration: `0006_memberprofile`

**Configurare conturi — testare locală:**
```powershell
# Creare superuser admin
.venv\Scripts\python.exe manage.py createsuperuser

# Pornire server
$env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py runserver
```
- Înregistrare cont nou: `http://127.0.0.1:8000/register/`
- Autentificare: `http://127.0.0.1:8000/login/`
- Profil: `http://127.0.0.1:8000/profile/`
- Admin → Profile membri: `http://127.0.0.1:8000/admin/catalog/memberprofile/`

**Note implementare:**
- Username = email (primele 150 caractere) — login se face cu email
- Profilul se creează automat la înregistrare via signal `post_save`
- `avatar` se salvează în `media/avatars/` — preview live în formularul de editare
- Formularul waitlist rămâne funcțional și independent de contul de utilizator

**Stage 9 — Completat:**
- [x] Model `ForumTopic` (category FK, author FK, title, slug, content, views_count, is_pinned, is_locked, created_at, updated_at)
- [x] Model `ForumReply` (topic FK, author FK, content, created_at, updated_at)
- [x] `ForumTopicForm`, `ForumReplyForm` cu stiluri Tailwind consistente
- [x] Vederi: `forum_index`, `forum_category`, `topic_detail`, `topic_new`, `topic_reply`
- [x] URL-uri: `/forum/`, `/forum/categorie/<slug>/`, `/forum/topic/nou/`, `/forum/topic/<slug>/`, `/forum/topic/<slug>/raspunde/`
- [x] Reguli acces: citire publică, postare/răspuns doar autentificat, locked topics blocate
- [x] Incrementare `views_count` la fiecare vizitare a subiectului
- [x] `ForumTopicAdmin` + `ForumReplyAdmin` cu filtre (category, pinned, locked) și search
- [x] `ForumReplyInline` în `ForumTopicAdmin`
- [x] Navbar: link Forum adăugat (desktop + mobil)
- [x] `comunitate.html`: categorii linkuite la `/forum/categorie/<slug>/`, subiecte reale dacă există, altfel preview-uri
- [x] Empty states cu CTA Login/Register
- [x] Migration: `0007_forumtopic_forumreply`

**Forum URLs:**
- Index: `http://127.0.0.1:8000/forum/`
- Categorie: `http://127.0.0.1:8000/forum/categorie/<slug>/`
- Subiect nou: `http://127.0.0.1:8000/forum/topic/nou/` (necesită cont)
- Subiect: `http://127.0.0.1:8000/forum/topic/<slug>/`

**Notă Flarum:**
Forumul intern Django este MVP. `FORUM_EXTERNAL_URL` rămâne configurat în `SiteSetting` și poate
fi setat oricând pentru a direcționa spre `forum.domain.ro` cu Flarum. Cele două sisteme
(`ForumTopicPreview` pentru demo + `ForumTopic` real) coexistă fără conflict.

**Stage 10 — Completat:**
- [x] Model `ForumReport` (reporter FK, topic FK nullable, reply FK nullable, reason choices, details, status: new/reviewed/dismissed, created_at, reviewed_at)
- [x] Soft delete: `is_deleted` + `deleted_at` pe `ForumTopic` și `ForumReply`
- [x] `ForumReportForm` cu reason + details
- [x] Vederi: `report_topic`, `report_reply` (login required, nu poți raporta propriul conținut, dubluri blocate)
- [x] URL-uri: `/forum/raporteaza/topic/<id>/`, `/forum/raporteaza/reply/<id>/`
- [x] Pagină reguli: `/forum/reguli/` (6 reguli în română)
- [x] Link reguli în `forum_index` și reminder pe `topic_detail`
- [x] Butoane „Raportează" pe subiect și pe fiecare răspuns (doar utilizatori autentificați, nu autorul)
- [x] Conținut șters (soft) ascuns din toate paginile publice
- [x] `ForumTopicAdmin`: acțiuni pin/unpin/lock/unlock/soft-delete
- [x] `ForumReplyAdmin`: acțiuni soft-delete/restaurare + filtru `is_deleted`
- [x] `ForumReportAdmin`: acțiuni mark_reviewed/dismiss, badge status colorat, link țintă
- [x] Migration: `0008_forumreply_deleted_at_forumreply_is_deleted_and_more`

**Moderare admin:**
- Rapoarte: `/admin/catalog/forumreport/`
- Acțiuni topic: pin, unpin, lock, unlock, șterge soft
- Acțiuni reply: șterge soft, restaurează

**Stage 11 — Completat:**
- [x] `show_in_directory` BooleanField pe `MemberProfile` (default True)
- [x] `get_badges()` pe `MemberProfile` — calculează: Membru nou, Proprietar jet-ski, Activ în forum (≥10 posts), Contributor (≥5 subiecte)
- [x] Vedere `member_directory`: `/membri/` — carduri publice cu avatar/inițiale, oraș, brand, badge Activ
- [x] Vedere `member_public_profile`: `/membri/<username>/` — profil complet, subiecte recente, răspunsuri recente, badge-uri (vizibil doar dacă `show_in_directory=True`)
- [x] `profile_view` actualizat: trimite `my_topics`, `my_replies`, `my_report_count`, `badges`
- [x] `profile.html`: secțiune Insigne + secțiune activitate forum (subiecte + răspunsuri proprii)
- [x] `profile_edit.html`: checkbox `show_in_directory` cu link spre `/membri/`
- [x] Navbar: link „Membri" adăugat (desktop + mobil)
- [x] `MemberProfileAdmin`: `list_editable = ('show_in_directory',)`, filtru `show_in_directory`, search extins cu `user__last_name`
- [x] Migration: `0009_memberprofile_show_in_directory`

**Membri URLs:**
- Director: `http://127.0.0.1:8000/membri/`
- Profil public: `http://127.0.0.1:8000/membri/<username>/` (404 dacă `show_in_directory=False`)

**Badge-uri:**
| Badge | Condiție |
|---|---|
| Membru nou | Oricine are profil |
| Proprietar jet-ski | `owns_jetski=True` |
| Activ în forum | ≥10 subiecte + răspunsuri |
| Contributor | ≥5 subiecte |

**Stage 12 — Completat:**
- [x] Forum index: search box (titlu, conținut, autor, categorie) + sort (recent/vizualizări/comentate) + filtru categorie + filtru fixate + paginare 10/pagină
- [x] Forum category: topic count + ultima activitate + paginare 10/pagină
- [x] Topic detail: layout 2 coloane (main + sidebar); stats bar (views + reply_count + dată); author card cu avatar, badge-uri, link profil public; related topics sidebar; paginare răspunsuri 10/pagină
- [x] Badge-uri beta vizibile în sidebar topic și carduri publice: Membru Beta, Proprietar jet-ski, Activ în forum, Contributor
- [x] Footer: coloana Comunitate actualizată cu Comunitate, Forum, Membri, Regulile forumului, Evenimente
- [x] `get_badges()` actualizat: "Membru Beta" (prima insignă pentru toți membrii în faza beta)
- [x] Import `Count` + `Paginator` adăugate în views.py

**URLs noi/actualizate:**
- Căutare: `/forum/?q=...&sort=replies&categorie=slug&fixate=1`
- Paginare: `/forum/?pagina=2`, `/forum/categorie/slug/?pagina=2`, `/forum/topic/slug/?pagina=2`

## Beta Launch Checklist

```bash
# 1. Creează superuser admin
$env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py createsuperuser

# 2. Rulează serverul
$env:PYTHONIOENCODING="utf-8"; .venv\Scripts\python.exe manage.py runserver
```

**Pași de configurare inițială:**
- [ ] Creează cont admin superuser
- [ ] Adaugă date reale: SiteSetting (SITE_NAME, CONTACT_EMAIL, CONTACT_PHONE, INSTAGRAM_URL etc.)
- [ ] Adaugă minim 5 jet-ski-uri reale cu imagini în /admin/catalog/jetski/
- [ ] Creează 3 categorii de forum (ex: Tehnic, Drumeții, Vânzări) în /admin/catalog/forumcategory/
- [ ] Creează 5 subiecte starter ca admin pentru a anima forumul
- [ ] Testează fluxul complet register → login → completare profil → post forum
- [ ] Testează raportare: creează 2 conturi, raportează un subiect de la celălalt cont
- [ ] Testează mobile layout la 375px și 768px
- [ ] Verifică paginarea la mai mult de 10 subiecte
- [ ] Verifică că `show_in_directory=False` ascunde profilul din /membri/
- [ ] Verifică că subiectele soft-delete nu apar pe pagini publice
- [ ] Rulează `manage.py check --deploy` înainte de producție

**Urmează:**
- [ ] Integrare Flarum pe `forum.domain.ro`
- [ ] Sistem newsletter/email
- [ ] CI/CD pipeline (GitHub Actions → deploy pe VPS)

---

*Construit cu pasiune pentru apele României. 🌊*
