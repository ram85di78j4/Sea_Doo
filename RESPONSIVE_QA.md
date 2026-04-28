# Responsive / Mobile QA — Sea-Doo România

_Actualizat: Stage 13 (Pre-deploy audit)_

---

## Pagini auditate

| Template | URL |
|---|---|
| `base.html` | Navbar, banner, footer — toate paginile |
| `home.html` | `/` |
| `catalog_list.html` | `/catalog/` |
| `catalog_detail.html` | `/catalog/<slug>/` |
| `comunitate.html` | `/comunitate/` |
| `forum_index.html` | `/forum/` |
| `forum_category.html` | `/forum/categorie/<slug>/` |
| `topic_detail.html` | `/forum/topic/<slug>/` |
| `topic_form.html` | `/forum/subiect-nou/` |
| `member_directory.html` | `/membri/` |
| `member_profile.html` | `/membri/<username>/` |
| `profile.html` | `/profile/` |
| `profile_edit.html` | `/profile/edit/` |
| `login.html` | `/login/` |
| `register.html` | `/register/` |
| `contact_page.html` | `/contact/` |

---

## Dimensiuni viewport testate

| Viewport | Device | Status |
|---|---|---|
| 375px | iPhone SE / iPhone 12 mini | ✅ Testat |
| 390px | iPhone 14 | ✅ Testat |
| 430px | iPhone 14 Plus | ✅ Testat |
| 768px | iPad / tablet | ✅ Testat |
| 1280px | Desktop standard | ✅ Testat |

---

## Probleme găsite și fixuri aplicate

### 1. Flash messages overflow pe 375px
- **Fișier:** `base.html` linia 179
- **Problemă:** `fixed top-20 right-4 max-w-sm` — `max-w-sm` (384px) depășea lățimea ecranului de 375px cu `right-4` (16px), cauzând overflow orizontal
- **Fix:** `fixed top-20 left-4 right-4 sm:left-auto sm:right-4 sm:max-w-sm` — pe mobile ocupă toată lățimea, pe desktop revine la poziția originală
- **Status:** ✅ Rezolvat

### 2. Launch banner overflow pe ecrane mici
- **Fișier:** `base.html` linia 90
- **Problemă:** `flex items-center justify-center gap-4` fără `flex-wrap` — text + buton CTA pe o singură linie putea ieși din ecran cu text lung
- **Fix:** `flex flex-wrap items-center justify-center gap-2 sm:gap-4`
- **Status:** ✅ Rezolvat

### 3. Hero heading prea mare pe 375px
- **Fișier:** `home.html` linia 53
- **Problemă:** `text-5xl` (48px) ca prim breakpoint pe mobile — "Acolo unde pasiunea" la 48px riscă overflow orizontal pe 375px
- **Fix:** `text-4xl sm:text-5xl md:text-7xl lg:text-8xl` — 36px pe mobile, 48px de la 640px
- **Status:** ✅ Rezolvat

### 4. Floating card "Sea-Doo RXT-X 300" overflow pe mobile
- **Fișier:** `home.html` linia 178
- **Problemă:** `absolute -bottom-5 -left-5` — cardul iese în afara containerului pe mobile, cauzând scroll orizontal
- **Fix:** Adăugat `hidden sm:block` — cardul se ascunde pe mobile, apare de la 640px
- **Status:** ✅ Rezolvat

### 5. Statistici topic (views) nu se ascundeau pe mobile în forum_category
- **Fișier:** `forum_category.html` linia 90
- **Problemă:** Coloana de replies + views era vizibilă pe mobile, lăsând prea puțin spațiu pentru titlul topicului
- **Fix:** Coloana views primește `hidden sm:flex` — vizibilă doar de la 640px. replies rămâne vizibil pe orice ecran
- **Status:** ✅ Rezolvat

### 6. Selecții filtru catalog neresponsive pe mobile
- **Fișier:** `catalog_list.html` linia 37-71
- **Problemă:** Search input cu `min-w-[200px]` și 3 selects fără `w-full` — pe mobile toate elementele aveau lățimi fixe, nu umpleau ecranul corect
- **Fix:**
  - Search input: `w-full sm:flex-1 sm:min-w-[200px] sm:max-w-xs` — full width pe mobile
  - Fiecare select: adăugat `w-full sm:w-auto` — full width pe mobile, auto pe desktop
- **Status:** ✅ Rezolvat

---

## Probleme ne-critice (nu necesită fix imediat)

| Pagina | Problemă | Decizie |
|---|---|---|
| `home.html` | Cardul floating SeaDoo Featured section (`absolute -bottom-4 -right-4 bg-yellow-400`) poate ieși ușor pe 375px | ℹ️ Mic, nu cauzează scroll orizontal |
| `catalog_detail.html` | Quick specs `grid-cols-3` strâns pe 375px | ℹ️ Valorile sunt scurte (număr CP, an, brand) — OK |
| `topic_detail.html` | Buton "Postează răspuns" aliniat dreapta | ℹ️ Funcționează corect, touch target OK |
| Admin panel `/admin/` | Nu este responsive (Django admin standard) | ℹ️ Așteptat, admin e pentru desktop |

---

## Checklist final mobil

### Navbar și Layout general
- [x] Navbar hamburger apare pe < md (768px)
- [x] Meniu mobil se deschide/închide corect
- [x] Launch banner nu cauzează scroll orizontal
- [x] Flash messages apar în interiorul ecranului pe 375px
- [x] Footer se stivuiește în 1 coloană pe mobile (grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4)
- [x] Footer bottom bar — flex-col pe mobile, flex-row pe md

### Landing page (/)
- [x] Hero heading lizibil la 375px (text-4xl = 36px)
- [x] CTA buttons stivuite vertical pe mobile (flex-col sm:flex-row)
- [x] Stats row cu flex-wrap — se stivuiesc corect
- [x] Trust cards — 2 coloane pe mobile (grid-cols-2)
- [x] About section — 1 coloană pe mobile (lg:grid-cols-2)
- [x] Floating card ascuns pe mobile (hidden sm:block)
- [x] Featured collection — 1 coloană pe mobile (grid-cols-1 md:grid-cols-2 lg:grid-cols-3)
- [x] Forum categories — 1 coloană pe mobile (grid-cols-1 md:grid-cols-2)
- [x] Brands section — 1 coloană pe mobile (grid-cols-1 md:grid-cols-3)
- [x] Pre-launch section — flex-col pe mobile

### Catalog (/catalog/)
- [x] Filter bar — search full width pe mobile
- [x] Selects filtru — full width pe mobile
- [x] Grid cards — 1 coloană pe mobile (grid-cols-1 md:grid-cols-2 lg:grid-cols-3)
- [x] Card images — aspect-video, object-cover
- [x] Empty state centrat corect

### Catalog detaliu (/catalog/<slug>/)
- [x] Layout principal — 1 coloană pe mobile (lg:grid-cols-2)
- [x] Quick specs — grid-cols-3 funcționează cu valori scurte
- [x] Specs grid — grid-cols-2 funcționează
- [x] Gallery — grid-cols-2 pe mobile
- [x] Lightbox — funcționează cu click/touch
- [x] Related models — grid-cols-1 md:grid-cols-3

### Forum (/forum/)
- [x] Categories grid — grid-cols-2 sm:grid-cols-3 lg:grid-cols-4
- [x] Search form — flex-col sm:flex-row
- [x] Topic rows — flex cu min-w-0 pe coloana de titlu
- [x] Stats column — views ascuns pe mobile
- [x] Paginare — centrată, butoane clare

### Forum categorie (/forum/categorie/<slug>/)
- [x] Header — flex-col md:flex-row
- [x] Topic rows — views ascuns pe mobile (hidden sm:flex)
- [x] Paginare — funcționează

### Topic detaliu (/forum/topic/<slug>/)
- [x] Two-column layout — flex-col pe mobile, sidebar sub conținut
- [x] Breadcrumb — flex-wrap
- [x] Reply form — vizibil, textarea full-width
- [x] Sidebar autor — w-full pe mobile

### Forum topic nou (/forum/subiect-nou/)
- [x] Form fields full-width
- [x] Buttons — flex-1 + fixed width cancel

### Membri (/membri/)
- [x] Grid — grid-cols-1 sm:grid-cols-2 lg:grid-cols-3
- [x] Member card — flex cu avatar și info

### Profil (/profile/, /profile/edit/)
- [x] Header card — flex-col sm:flex-row
- [x] Details grid — grid-cols-1 sm:grid-cols-2
- [x] Forum activity — grid-cols-1 md:grid-cols-2
- [x] Edit form — grid-cols-1 sm:grid-cols-2 pentru city/brand

### Autentificare (/login/, /register/)
- [x] Centrat vertical cu min-h-screen
- [x] Form card max-w-md / max-w-lg
- [x] Passwords side-by-side pe sm (grid-cols-1 sm:grid-cols-2)
- [x] Submit button full-width

### Contact (/contact/)
- [x] Two-column — grid-cols-1 lg:grid-cols-2
- [x] Form full-width pe mobile
- [x] Info list — single column, flex items

---

## Comenzi pentru testare rapidă în browser

```
# DevTools → Toggle device toolbar (Ctrl+Shift+M)
# Selectează: iPhone SE (375px), iPhone 14 (390px), iPad (768px)
# Verifică: nu există scroll orizontal pe nicio pagină
```

**Test scroll orizontal (JavaScript console):**
```javascript
document.querySelectorAll('*').forEach(el => {
  if (el.scrollWidth > document.documentElement.clientWidth) {
    console.warn('Overflow element:', el, el.className);
  }
});
```

---

## Status final

| Categorie | Status |
|---|---|
| Navbar / Layout | ✅ Complet responsive |
| Landing page | ✅ Complet responsive |
| Catalog | ✅ Complet responsive |
| Forum | ✅ Complet responsive |
| Autentificare | ✅ Complet responsive |
| Profil / Membri | ✅ Complet responsive |
| Contact | ✅ Complet responsive |
| Admin panel | ℹ️ Nu se aplică (Django admin standard) |
