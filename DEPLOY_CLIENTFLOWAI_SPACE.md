# Deployment Guide — clientflowai.space
# VPS: root@207.180.245.29 | Ubuntu 22.04+

---

## Înainte să începi — Safety checks (VPS cu alte site-uri active)

SSH-ează pe server și rulează aceste verificări ÎNAINTE de a atinge Nginx:

```bash
ssh root@207.180.245.29

# 1. Ce site-uri sunt active?
ls -la /etc/nginx/sites-enabled/

# 2. Ce server_name-uri există deja?
nginx -T | grep server_name

# 3. Ce porturi sunt ocupate?
ss -tulnp | grep LISTEN

# 4. Verifică portul 8010 e liber
ss -tulnp | grep 8010
```

> **Reguli stricte:**
> - Nu șterge / nu modifica configs existente din `/etc/nginx/sites-enabled/`
> - Nu opri servicii existente
> - Portul intern ales: **8010** (verifică că nu e ocupat mai sus)
> - Adaugă DOAR un config nou pentru `clientflowai.space`

---

## Pasul 1 — Pachete sistem

```bash
apt update && apt upgrade -y
apt install -y python3 python3-venv python3-pip git nginx certbot python3-certbot-nginx
```

---

## Pasul 2 — Clonare proiect

```bash
cd /var/www
git clone https://github.com/ram85di78j4/Sea_Doo.git clientflowai.space
cd /var/www/clientflowai.space
```

---

## Pasul 3 — Virtualenv și dependențe

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Pasul 4 — Creează fișierul .env

```bash
cp .env.example .env
nano .env
```

Completează cu valorile reale:

```ini
SECRET_KEY=generează-o-cheie-secretă-lungă-de-minim-50-caractere
DEBUG=False
ALLOWED_HOSTS=clientflowai.space,www.clientflowai.space,207.180.245.29
CSRF_TRUSTED_ORIGINS=https://clientflowai.space,https://www.clientflowai.space
FORUM_EXTERNAL_URL=https://forum.clientflowai.space
HERO_VIDEO_URL=
```

**Generare SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(60))"
```

---

## Pasul 5 — Setup Django

```bash
source .venv/bin/activate

# Verificare configurare producție
python manage.py check --deploy --settings=sea_doo.settings.production

# Migrații bază de date
python manage.py migrate --settings=sea_doo.settings.production

# Colectare fișiere statice
python manage.py collectstatic --noinput --settings=sea_doo.settings.production

# Date demo (opțional)
python manage.py seed_data --settings=sea_doo.settings.production

# Creează superuser admin
python manage.py createsuperuser --settings=sea_doo.settings.production
```

---

## Pasul 6 — Test Gunicorn

```bash
source .venv/bin/activate
.venv/bin/gunicorn sea_doo.wsgi:application \
    --bind 127.0.0.1:8010 \
    --workers 3 \
    --timeout 120

# Testează cu Ctrl+C după ce vezi "Arbiter booted"
# Dacă pornește OK, continuă la pasul următor
```

---

## Pasul 7 — Systemd service

Creează fișierul de serviciu:

```bash
nano /etc/systemd/system/clientflowai-space.service
```

Conținut:

```ini
[Unit]
Description=Sea-Doo Romania — clientflowai.space
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/clientflowai.space
Environment="DJANGO_SETTINGS_MODULE=sea_doo.settings.production"
ExecStart=/var/www/clientflowai.space/.venv/bin/gunicorn \
    sea_doo.wsgi:application \
    --bind 127.0.0.1:8010 \
    --workers 3 \
    --timeout 120 \
    --access-logfile /var/log/clientflowai-space-access.log \
    --error-logfile /var/log/clientflowai-space-error.log
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Activare serviciu:

```bash
# Permisiuni folder
chown -R www-data:www-data /var/www/clientflowai.space

# Activare și pornire
systemctl daemon-reload
systemctl enable clientflowai-space
systemctl start clientflowai-space

# Verificare status
systemctl status clientflowai-space
```

---

## Pasul 8 — Nginx config

```bash
nano /etc/nginx/sites-available/clientflowai.space
```

Conținut:

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name clientflowai.space www.clientflowai.space;

    # Static files (WhiteNoise handles these via Django, but Nginx is faster)
    location /static/ {
        alias /var/www/clientflowai.space/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files (user uploads)
    location /media/ {
        alias /var/www/clientflowai.space/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_read_timeout 120s;
        client_max_body_size 10M;
    }
}
```

Activare site:

```bash
# Activează (nu atinge alte configs!)
ln -s /etc/nginx/sites-available/clientflowai.space /etc/nginx/sites-enabled/

# Testează configurația Nginx (nu trebuie erori)
nginx -t

# Reîncarcă Nginx (nu restart — nu perturbă alte site-uri)
systemctl reload nginx
```

---

## Pasul 9 — SSL cu Certbot

```bash
certbot --nginx -d clientflowai.space -d www.clientflowai.space
```

Certbot va:
1. Obține certificatul Let's Encrypt
2. Modifica automat config-ul Nginx pentru HTTPS
3. Adăuga redirect HTTP → HTTPS

Confirma cu email când solicitat, alege opțiunea de redirect forțat (opțiunea 2).

---

## Pasul 10 — Verificări finale

```bash
# 1. Endpoint health
curl -I https://clientflowai.space/health/

# 2. Redirect HTTP → HTTPS
curl -I http://clientflowai.space/

# 3. robots.txt
curl https://clientflowai.space/robots.txt

# 4. sitemap.xml
curl https://clientflowai.space/sitemap.xml

# 5. Landing page (trebuie 200)
curl -s -o /dev/null -w "%{http_code}" https://clientflowai.space/

# 6. Status serviciu
systemctl status clientflowai-space

# 7. Logs recente
tail -50 /var/log/clientflowai-space-error.log
```

---

## Comenzi de administrare zilnică

```bash
# Restart aplicație (după update cod)
systemctl restart clientflowai-space

# Reîncărcare Nginx (fără downtime)
systemctl reload nginx

# Logs live
journalctl -u clientflowai-space -f

# Update cod din GitHub
cd /var/www/clientflowai.space
source .venv/bin/activate
git pull origin main
python manage.py migrate --settings=sea_doo.settings.production
python manage.py collectstatic --noinput --settings=sea_doo.settings.production
systemctl restart clientflowai-space

# Reînnoire SSL (automată, dar poți forța)
certbot renew --dry-run
```

---

## Rezolvare probleme comune

### 502 Bad Gateway
```bash
systemctl status clientflowai-space
tail -30 /var/log/clientflowai-space-error.log
# Cel mai probabil: .venv/bin/gunicorn nu există sau www-data nu are permisiuni
chown -R www-data:www-data /var/www/clientflowai.space
systemctl restart clientflowai-space
```

### Static files lipsesc (CSS/JS nu se încarcă)
```bash
source /var/www/clientflowai.space/.venv/bin/activate
cd /var/www/clientflowai.space
python manage.py collectstatic --noinput --settings=sea_doo.settings.production
# Verifică că /var/www/clientflowai.space/staticfiles/ există și are fișiere
ls staticfiles/
```

### Eroare CSRF / 403
Verifică în `.env`:
```ini
CSRF_TRUSTED_ORIGINS=https://clientflowai.space,https://www.clientflowai.space
```

### Media uploads nu funcționează
```bash
# Verifică că folderul media există și www-data poate scrie în el
mkdir -p /var/www/clientflowai.space/media
chown -R www-data:www-data /var/www/clientflowai.space/media
```

### DisallowedHost / 400 Bad Request
Verifică în `.env`:
```ini
ALLOWED_HOSTS=clientflowai.space,www.clientflowai.space,207.180.245.29
```

---

## Structura finală pe server

```
/var/www/clientflowai.space/
├── .env                          ← variabile producție (nu în git)
├── .venv/                        ← virtualenv Python
├── catalog/                      ← aplicația Django
├── sea_doo/                      ← settings, urls, wsgi
├── staticfiles/                  ← fișiere statice colectate
├── media/                        ← upload-uri utilizatori
├── db.sqlite3                    ← baza de date (SQLite)
└── manage.py

/etc/nginx/sites-available/clientflowai.space  ← config Nginx
/etc/nginx/sites-enabled/clientflowai.space    ← symlink activ
/etc/systemd/system/clientflowai-space.service ← serviciu systemd
/var/log/clientflowai-space-access.log         ← access log
/var/log/clientflowai-space-error.log          ← error log
```

---

## Checklist pre-deploy

- [ ] `.env` completat cu toate valorile
- [ ] `SECRET_KEY` generat aleator (min 50 chars)
- [ ] `DEBUG=False` în `.env`
- [ ] `ALLOWED_HOSTS` include domeniul și IP-ul VPS
- [ ] `CSRF_TRUSTED_ORIGINS` include https://
- [ ] `python manage.py check --deploy` fără erori critice
- [ ] `collectstatic` rulat cu succes
- [ ] Gunicorn pornit cu succes pe portul 8010
- [ ] Nginx config testat cu `nginx -t`
- [ ] SSL certificat obținut cu Certbot
- [ ] `curl https://clientflowai.space/health/` returnează 200
- [ ] Admin accesibil la `https://clientflowai.space/admin/`
- [ ] Upload imagine test în admin funcționează
- [ ] Niciun alt site de pe VPS nu este afectat
