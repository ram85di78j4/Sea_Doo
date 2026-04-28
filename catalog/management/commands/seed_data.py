import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from catalog.models import JetSki, ForumCategory, ForumTopicPreview, ForumTopic, ForumReply, EventPreview, Testimonial, SiteSetting, MemberProfile


SAMPLE_EVENTS = [
    {
        'title': 'Intalnire pe lacul Snagov',
        'slug': 'intalnire-lac-snagov',
        'location': 'Lacul Snagov, Ilfov',
        'event_date': datetime.date(2025, 6, 14),
        'short_description': (
            'Prima intalnire a pasionatilor de jet-ski din zona Bucuresti. '
            'Navigam impreuna pe lacul Snagov, schimbam experiente si facem cunostinta. '
            'Toti posesorii de jet-ski sunt bineveniti, indiferent de brand sau model.'
        ),
    },
    {
        'title': 'Tura pe Dunare - Portile de Fier',
        'slug': 'tura-dunare-portile-de-fier',
        'location': 'Portile de Fier, Mehedinti',
        'event_date': datetime.date(2025, 7, 19),
        'short_description': (
            'O tura spectaculoasa prin Defileul Dunarii, intre Orsova si Drobeta-Turnu Severin. '
            'Peisaje de exceptie, ape largi si o experienta de neuitat pentru oricine iubeste '
            'navigatia cu jet-ski pe apa dulce.'
        ),
    },
    {
        'title': 'Weekend Jet-Ski la Constanta',
        'slug': 'weekend-jet-ski-constanta',
        'location': 'Plaja Modern, Constanta',
        'event_date': datetime.date(2025, 8, 9),
        'short_description': (
            'Doua zile de navigatie pe Marea Neagra, zona Constanta - Mamaia. '
            'Valuri, soare si adrenalina garantata. Cazare recomandata disponibila '
            'prin organizatori. Locuri limitate - inscrie-te din timp!'
        ),
    },
]


SAMPLE_TESTIMONIALS = [
    {
        'name': 'Radu Constantin',
        'city': 'Bucuresti',
        'message': (
            'Am gasit pe SeaDoo.ro tot ce aveam nevoie inainte sa cumpar primul meu jet-ski. '
            'Descrierile sunt reale, nu marketing gol. Mi-a salvat mii de euro evitand un model '
            'nepotrivit pentru ce aveam eu nevoie.'
        ),
        'rating': 5,
    },
    {
        'name': 'Mihaela Ionescu',
        'city': 'Cluj-Napoca',
        'message': (
            'Cel mai serios site de jet-ski din Romania. Am participat la intalnirea de pe '
            'lacul Snagov si am cunoscut oameni minunati. Comunitatea aceasta chiar construieste '
            'ceva autentic.'
        ),
        'rating': 5,
    },
    {
        'name': 'Alexandru Marin',
        'city': 'Constanta',
        'message': (
            'Eram sceptic la inceput, dar catalogul cu povesti reale si specificatii tehnice '
            'oneste m-a convins. Acum am un GTX Limited 300 si l-am ales pe baza articolului '
            'de pe acest site. Nu regret nicio clipa.'
        ),
        'rating': 5,
    },
]


SAMPLE_CATEGORIES = [
    {'name': 'Sea-Doo Romania', 'slug': 'sea-doo-romania', 'description': 'Discutii despre modelele Sea-Doo, experiente si sfaturi', 'icon': 'S', 'order': 1},
    {'name': 'Yamaha WaveRunner', 'slug': 'yamaha-waverunner', 'description': 'Totul despre gama Yamaha WaveRunner', 'icon': 'Y', 'order': 2},
    {'name': 'Kawasaki Jet Ski', 'slug': 'kawasaki-jet-ski', 'description': 'Forum dedicat modelelor Kawasaki', 'icon': 'K', 'order': 3},
    {'name': 'Sfaturi cumparare', 'slug': 'sfaturi-cumparare', 'description': 'Ghid pentru cumpararea primului jet-ski. Ce sa verifici, ce sa eviti', 'icon': '?', 'order': 4},
    {'name': 'Service si mentenanta', 'slug': 'service-mentenanta', 'description': 'Intretinere, reparatii DIY, service-uri recomandate', 'icon': 'T', 'order': 5},
    {'name': 'Trasee pe apa', 'slug': 'trasee-pe-apa', 'description': 'Dunare, Marea Neagra, lacuri. Trasee documentate in Romania', 'icon': 'M', 'order': 6},
    {'name': 'Evenimente', 'slug': 'evenimente', 'description': 'Intalniri, competitii, ride-uri de grup', 'icon': 'E', 'order': 7},
    {'name': 'Piese si accesorii', 'slug': 'piese-accesorii', 'description': 'Recomandari, furnizori, achizitii grupate', 'icon': 'P', 'order': 8},
    {'name': 'Vanzari intre membri', 'slug': 'vanzari-membri', 'description': 'Marketplace de incredere in cadrul comunitatii', 'icon': 'V', 'order': 9},
]


SAMPLE_TOPICS = [
    {
        'category_slug': 'sea-doo-romania',
        'title': 'RXT-X 300 vs GTX 300 - ce alegeti pentru ture lungi?',
        'author_name': 'Andrei_SD',
        'replies_count': 24,
        'views_count': 312,
        'is_pinned': True,
    },
    {
        'category_slug': 'sfaturi-cumparare',
        'title': 'Ghid complet: ce verifici cand cumperi un jet-ski second-hand',
        'author_name': 'MariusAqua',
        'replies_count': 47,
        'views_count': 891,
        'is_pinned': True,
    },
    {
        'category_slug': 'service-mentenanta',
        'title': 'Inlocuire impelora Rotax 1630 - pas cu pas',
        'author_name': 'TechRider',
        'replies_count': 18,
        'views_count': 445,
        'is_pinned': False,
    },
    {
        'category_slug': 'trasee-pe-apa',
        'title': 'Traseul Tulcea - Sulina pe Dunare: tot ce trebuie sa stii',
        'author_name': 'DeltaRider',
        'replies_count': 33,
        'views_count': 628,
        'is_pinned': False,
    },
    {
        'category_slug': 'yamaha-waverunner',
        'title': 'FX SVHO 2023 - primele impresii dupa 50 de ore pe apa',
        'author_name': 'YamahaFan',
        'replies_count': 15,
        'views_count': 290,
        'is_pinned': False,
    },
    {
        'category_slug': 'sea-doo-romania',
        'title': 'Sea-Doo Fish Pro - merita pentru pescuit in Romania?',
        'author_name': 'FisherKing',
        'replies_count': 29,
        'views_count': 374,
        'is_pinned': False,
    },
    {
        'category_slug': 'evenimente',
        'title': 'Ride de grup pe Dunare - weekend 15-16 iunie 2025',
        'author_name': 'EventOrganizer',
        'replies_count': 41,
        'views_count': 503,
        'is_pinned': False,
    },
    {
        'category_slug': 'piese-accesorii',
        'title': 'Unde gasiti piese originale Sea-Doo in Romania la preturi ok?',
        'author_name': 'SparePartsPro',
        'replies_count': 56,
        'views_count': 712,
        'is_pinned': False,
    },
    {
        'category_slug': 'kawasaki-jet-ski',
        'title': 'Ultra 310X - cel mai puternic jet-ski aspirat natural. Pareri?',
        'author_name': 'KawasakiPilot',
        'replies_count': 12,
        'views_count': 198,
        'is_pinned': False,
    },
    {
        'category_slug': 'vanzari-membri',
        'title': 'Vand Sea-Doo Spark 2019 90CP - stare foarte buna, 120 ore',
        'author_name': 'VanzatorSigur',
        'replies_count': 8,
        'views_count': 267,
        'is_pinned': False,
    },
]


SAMPLE_JETSKIS = [
    {
        'title': 'RXT-X 300 — Viteză Absolută',
        'brand': 'Sea-Doo',
        'model': 'RXT-X 300',
        'year': 2022,
        'engine': 'Rotax 1630 ACE Turbocharged',
        'horsepower': 300,
        'condition': 'Excelentă',
        'status': 'favorite',
        'short_description': (
            'Cel mai rapid din colecție. O mașinărie construită pentru performanță pură — '
            '300 de cai putere care te aruncă în față cu o forță brută incredibilă.'
        ),
        'full_description': (
            'Sea-Doo RXT-X 300 este apogeul performanței pe apă. Cu motorul Rotax 1630 ACE '
            'turbocompresor de 300 CP, această mașinărie atinge viteze de peste 130 km/h pe apă.\n\n'
            'Sistemul de frânare inteligentă iTC și controlul tracțiunii îl fac mai ușor de '
            'controlat decât ar părea la aceste performanțe. Prima dată când am urcat pe el, '
            'am rămas fără cuvinte.\n\n'
            'Achiziționat în 2022, folosit pe Dunăre și Marea Neagră. Stare perfectă.'
        ),
        'why_worth_seeing': (
            'Motorul turbocharged Rotax 1630 ACE de 300 CP este cel mai puternic din gamă. '
            'Sistemul iTC (intelligent Throttle Control) și frânarea inteligentă îl fac sigur '
            'chiar și la viteze extreme. Dacă vrei să simți ce înseamnă 130 km/h pe apă, '
            'acesta este modelul.'
        ),
        'video_url': '',
    },
    {
        'title': 'GTX Limited 300 — Lux pe Apă',
        'brand': 'Sea-Doo',
        'model': 'GTX Limited 300',
        'year': 2021,
        'engine': 'Rotax 1630 ACE Turbocharged',
        'horsepower': 300,
        'condition': 'Foarte bună',
        'status': 'in_collection',
        'short_description': (
            'Versiunea de lux a familiei GTX. Confort premium, putere maximă și dotări de top '
            'pentru plimbări lungi pe Dunăre sau Marea Neagră.'
        ),
        'full_description': (
            'GTX Limited 300 combină performanța brută a motorului 300 CP cu un nivel de '
            'confort rar întâlnit pe un jet-ski. Scaune reglabile, sistem audio Bluetooth, '
            'culoar de stocare generos.\n\n'
            'Este alegerea perfectă pentru ture lungi sau pentru cei care vor să impresioneze '
            'fără să renunțe la performanță. Un echilibru perfect între sport și touring.'
        ),
        'why_worth_seeing': (
            'Sistemul audio Bluetooth, scaunul pasager confortabil și compartimentul de '
            'depozitare mare îl fac ideal pentru ture de o zi întreagă. 300 CP într-un '
            'pachet luxos — cel mai confortabil jet-ski din colecție.'
        ),
        'video_url': '',
    },
    {
        'title': 'Spark Trixx 90 — Distracție Pură',
        'brand': 'Sea-Doo',
        'model': 'Spark Trixx 90',
        'year': 2020,
        'engine': 'Rotax 900 ACE',
        'horsepower': 90,
        'condition': 'Bună',
        'status': 'in_collection',
        'short_description': (
            'Mic dar extrem de jucăuș. Spark Trixx este conceput pentru trick-uri și distracție. '
            'Perfect pentru lacuri și locuri cu spațiu de manevrat.'
        ),
        'full_description': (
            'Sea-Doo Spark Trixx a revoluționat categoria entry-level. Cu plăcile de extensie '
            'și bara de menaj, poți face wheelie-uri și sări valuri cu ușurință.\n\n'
            'Este mașinăria preferată de cei care vin prima dată pe apă — ușor de controlat, '
            'imposibil de plictisit. Și da, și adulții se distrează pe el.'
        ),
        'why_worth_seeing': (
            'Plăcile de extensie laterale și bara de menaj îl transformă într-o platformă '
            'de acrobații pe apă. Cel mai jucăuș jet-ski din colecție — și cel mai accesibil '
            'ca preț de intrare în lumea Sea-Doo.'
        ),
        'video_url': '',
    },
    {
        'title': 'GTI SE 130 — Perfecțiunea Zilnică',
        'brand': 'Sea-Doo',
        'model': 'GTI SE 130',
        'year': 2019,
        'engine': 'Rotax 1503 NA',
        'horsepower': 130,
        'condition': 'Bună',
        'status': 'available',
        'short_description': (
            'Modelul echilibrat din colecție. Nici prea puternic, nici prea lent — perfect pentru '
            'orice tip de utilizare, de la plimbări relaxante până la sesiuni mai dinamice.'
        ),
        'full_description': (
            'GTI SE 130 este probabil cel mai versatil jet-ski din colecție. 130 CP sunt '
            'suficienți pentru distracție fără a fi copleșitor pentru un începător.\n\n'
            'Este mașinăria pe care o recomand pentru oricine vrea să înceapă cu jet-ski-ul '
            'serios. Fiabilă, economică, distractivă. Disponibilă pentru vânzare — '
            'contactează-mă pentru detalii.'
        ),
        'why_worth_seeing': (
            'Raportul putere/preț/consum este imbatabil. Rotax 1503 NA este unul dintre '
            'cele mai fiabile motoare din industrie. Ideal ca primul jet-ski propriu sau '
            'ca adăugire accesibilă la o colecție.'
        ),
        'video_url': '',
    },
    {
        'title': 'FX HO — Yamaha în Garajul Sea-Doo',
        'brand': 'Yamaha',
        'model': 'FX HO',
        'year': 2018,
        'engine': 'Yamaha 1812cc NA',
        'horsepower': 180,
        'condition': 'Bună',
        'status': 'sold',
        'short_description': (
            'Singurul Yamaha din colecție. O mașinărie solidă, de incredibilă fiabilitate. '
            'A plecat la o nouă casă, dar amintirile rămân.'
        ),
        'full_description': (
            'Yamaha FX HO a demonstrat că fiabilitatea japoneză nu are rival. 180 CP dintr-un '
            'motor aspirat natural — nu turbo — dar cu o livrare liniară a puterii care te '
            'face să zâmbești de fiecare dată.\n\n'
            'L-am vândut cu inima grea după 3 sezoane. Dacă dai de el pe piață, ia-l. '
            'Nu vei regreta.'
        ),
        'why_worth_seeing': (
            'Singurul Yamaha din colecție — și o lecție despre ce înseamnă fiabilitate '
            'japoneză. Motorul 1812cc aspirat natural livrează putere liniară, fără '
            'surprize. O referință valoroasă alături de gama Sea-Doo.'
        ),
        'video_url': '',
    },
]


class Command(BaseCommand):
    help = 'Populeaza baza de date cu date de test'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.HTTP_INFO('\n[~]  Sea-Doo Romania -- Seed Data\n'))

        # --- Jet-ski-uri ---
        js_created = js_skipped = 0
        for data in SAMPLE_JETSKIS:
            obj, was_created = JetSki.objects.get_or_create(
                title=data['title'],
                defaults=data,
            )
            if was_created:
                js_created += 1
                self.stdout.write(f'  [+]  JetSki creat: {obj}')
            else:
                js_skipped += 1
                self.stdout.write(f'  [=]  JetSki exista: {obj}')

        self.stdout.write('')
        if js_created:
            self.stdout.write(self.style.SUCCESS(f'[OK]  {js_created} jet-ski-uri create!'))
        if js_skipped:
            self.stdout.write(self.style.WARNING(f'[i]   {js_skipped} jet-ski-uri existente, omise.'))

        # --- Categorii forum ---
        self.stdout.write(self.style.HTTP_INFO('\n[~]  Forum categories...\n'))
        cat_created = cat_skipped = 0
        for data in SAMPLE_CATEGORIES:
            cat, was_created = ForumCategory.objects.get_or_create(
                slug=data['slug'],
                defaults=data,
            )
            if was_created:
                cat_created += 1
                self.stdout.write(f'  [+]  Categorie: {cat}')
            else:
                cat_skipped += 1
                self.stdout.write(f'  [=]  Categorie existenta: {cat}')

        self.stdout.write('')
        if cat_created:
            self.stdout.write(self.style.SUCCESS(f'[OK]  {cat_created} categorii create!'))
        if cat_skipped:
            self.stdout.write(self.style.WARNING(f'[i]   {cat_skipped} categorii existente, omise.'))

        # --- Subiecte forum ---
        self.stdout.write(self.style.HTTP_INFO('\n[~]  Forum topics...\n'))
        topic_created = topic_skipped = 0
        for data in SAMPLE_TOPICS:
            cat_slug = data.pop('category_slug')
            try:
                category = ForumCategory.objects.get(slug=cat_slug)
                topic, was_created = ForumTopicPreview.objects.get_or_create(
                    title=data['title'],
                    defaults={**data, 'category': category},
                )
                if was_created:
                    topic_created += 1
                    self.stdout.write(f'  [+]  Topic: {topic.title[:50]}')
                else:
                    topic_skipped += 1
                    self.stdout.write(f'  [=]  Topic existent: {topic.title[:50]}')
            except ForumCategory.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'  [!]  Categorie negasita: {cat_slug}'))
            data['category_slug'] = cat_slug

        self.stdout.write('')
        if topic_created:
            self.stdout.write(self.style.SUCCESS(f'[OK]  {topic_created} topicuri create!'))
        if topic_skipped:
            self.stdout.write(self.style.WARNING(f'[i]   {topic_skipped} topicuri existente, omise.'))

        # --- Evenimente ---
        self.stdout.write(self.style.HTTP_INFO('\n[~]  Events...\n'))
        ev_created = ev_skipped = 0
        for data in SAMPLE_EVENTS:
            ev, was_created = EventPreview.objects.get_or_create(
                slug=data['slug'],
                defaults=data,
            )
            if was_created:
                ev_created += 1
                self.stdout.write(f'  [+]  Eveniment: {ev.title}')
            else:
                ev_skipped += 1
                self.stdout.write(f'  [=]  Eveniment existent: {ev.title}')

        self.stdout.write('')
        if ev_created:
            self.stdout.write(self.style.SUCCESS(f'[OK]  {ev_created} evenimente create!'))
        if ev_skipped:
            self.stdout.write(self.style.WARNING(f'[i]   {ev_skipped} evenimente existente, omise.'))

        # --- Testimoniale ---
        self.stdout.write(self.style.HTTP_INFO('\n[~]  Testimonials...\n'))
        t_created = t_skipped = 0
        for data in SAMPLE_TESTIMONIALS:
            t, was_created = Testimonial.objects.get_or_create(
                name=data['name'],
                defaults=data,
            )
            if was_created:
                t_created += 1
                self.stdout.write(f'  [+]  Testimonial: {t.name}')
            else:
                t_skipped += 1
                self.stdout.write(f'  [=]  Testimonial existent: {t.name}')

        self.stdout.write('')
        if t_created:
            self.stdout.write(self.style.SUCCESS(f'[OK]  {t_created} testimoniale create!'))
        if t_skipped:
            self.stdout.write(self.style.WARNING(f'[i]   {t_skipped} testimoniale existente, omise.'))
        self.stdout.write('')

        # --- SiteSettings demo ---
        self.stdout.write(self.style.HTTP_INFO('\n[~]  SiteSettings demo...\n'))
        DEMO_SETTINGS = [
            {
                'key': 'SITE_NAME',
                'value': 'JetSki România',
                'description': 'Numele public al platformei',
                'is_public': True,
            },
            {
                'key': 'SITE_TAGLINE',
                'value': 'Colecție privată. Comunitate pentru pasionați.',
                'description': 'Tagline-ul afișat lângă logo și în SEO',
                'is_public': True,
            },
            {
                'key': 'CONTACT_EMAIL',
                'value': 'contact@domain.ro',
                'description': 'Email-ul de contact afișat pe site',
                'is_public': True,
            },
            {
                'key': 'LAUNCH_BANNER_ENABLED',
                'value': 'false',
                'description': 'Activează bannerul de lansare (true/false)',
                'is_public': True,
            },
            {
                'key': 'LAUNCH_BANNER_TEXT',
                'value': 'Comunitatea se lansează în curând — înscrie-te acum pe lista de așteptare!',
                'description': 'Textul din bannerul de lansare',
                'is_public': True,
            },
            {
                'key': 'LAUNCH_BANNER_CTA_TEXT',
                'value': 'Vreau să fiu primul',
                'description': 'Textul butonului din banner',
                'is_public': True,
            },
            {
                'key': 'LAUNCH_BANNER_CTA_URL',
                'value': '/comunitate/#inscrie-te',
                'description': 'URL-ul butonului din banner',
                'is_public': True,
            },
        ]
        ss_created = ss_skipped = 0
        for data in DEMO_SETTINGS:
            obj, was_created = SiteSetting.objects.get_or_create(
                key=data['key'],
                defaults=data,
            )
            if was_created:
                ss_created += 1
                self.stdout.write(f'  [+]  SiteSetting: {obj.key}')
            else:
                ss_skipped += 1
                self.stdout.write(f'  [=]  SiteSetting existentă: {obj.key}')

        self.stdout.write('')
        if ss_created:
            self.stdout.write(self.style.SUCCESS(f'[OK]  {ss_created} setari create!'))
        if ss_skipped:
            self.stdout.write(self.style.WARNING(f'[i]   {ss_skipped} setari existente, omise.'))
        self.stdout.write('')

        # --- Demo user + real ForumTopic objects ---
        self.stdout.write(self.style.HTTP_INFO('[~]  Demo forum user + real topics...\n'))
        demo_email = 'demo@seadoo.ro'
        demo_user, user_created = User.objects.get_or_create(
            username=demo_email,
            defaults={
                'email': demo_email,
                'first_name': 'Demo',
                'last_name': 'Membru',
            },
        )
        if user_created:
            demo_user.set_password('demo1234!')
            demo_user.save()
            MemberProfile.objects.get_or_create(user=demo_user)
            self.stdout.write(self.style.SUCCESS('  [+]  Demo user creat: demo@seadoo.ro / demo1234!'))
        else:
            self.stdout.write(self.style.WARNING('  [=]  Demo user existent: demo@seadoo.ro'))

        REAL_TOPICS = [
            {
                'category_slug': 'sea-doo-romania',
                'title': 'Bun venit în comunitatea Sea-Doo România!',
                'content': (
                    'Salutare tuturor!\n\n'
                    'Suntem bucuroși să vă avem în această comunitate dedicată pasionaților de jet-ski din România.\n\n'
                    'Dacă ai un Sea-Doo, Yamaha sau Kawasaki — sau ești doar curios — ești binevenit!\n\n'
                    'Postează întrebările tale, distribuie experiențele și să ne cunoaștem. 🌊'
                ),
                'is_pinned': True,
            },
            {
                'category_slug': 'sfaturi-cumparare',
                'title': 'Ghid pentru primul jet-ski — ce să știi înainte să cumperi',
                'content': (
                    'Dacă ești la primul jet-ski, iată câteva lucruri esențiale:\n\n'
                    '1. Decide bugetul — noile modele pornesc de la ~8.000 EUR, second-hand de la ~3.000 EUR\n'
                    '2. Alege capacitatea — 60CP pentru recreere, 130CP+ pentru performanță\n'
                    '3. Verifică orele de funcționare — sub 100 ore = nou, 200-300 = ok, peste 500 = risc\n'
                    '4. Inspectează corpul pentru fisuri sau reparații\n'
                    '5. Testează pe apă înainte să cumperi\n\n'
                    'Succes la căutare!'
                ),
                'is_pinned': False,
            },
            {
                'category_slug': 'trasee-pe-apa',
                'title': 'Top 5 trasee pentru jet-ski în România',
                'content': (
                    'România are apele ei superbe pentru jet-ski:\n\n'
                    '1. Delta Dunării — cel mai spectaculos, dar necesită permis\n'
                    '2. Lacul Bicaz — munte + apă = combinație perfectă\n'
                    '3. Lacul Snagov — aproape de București, perfect pentru ieșiri rapide\n'
                    '4. Marea Neagră (Mamaia-Nord) — sezon estival, valuri mici\n'
                    '5. Dunărea la Portile de Fier — impresionant, necesită precauție\n\n'
                    'Voi unde ați mai navigat?'
                ),
                'is_pinned': False,
            },
        ]

        rt_created = rt_skipped = 0
        for data in REAL_TOPICS:
            cat_slug = data['category_slug']
            try:
                cat = ForumCategory.objects.get(slug=cat_slug)
                t, was_created = ForumTopic.objects.get_or_create(
                    title=data['title'],
                    defaults={
                        'category': cat,
                        'author': demo_user,
                        'content': data['content'],
                        'is_pinned': data.get('is_pinned', False),
                    },
                )
                if was_created:
                    rt_created += 1
                    self.stdout.write(f'  [+]  Topic real: {t.title[:55]}')
                else:
                    rt_skipped += 1
                    self.stdout.write(f'  [=]  Topic real existent: {t.title[:45]}')
            except ForumCategory.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'  [!]  Categorie negasita: {cat_slug}'))

        self.stdout.write('')
        if rt_created:
            self.stdout.write(self.style.SUCCESS(f'[OK]  {rt_created} topicuri reale create!'))
        if rt_skipped:
            self.stdout.write(self.style.WARNING(f'[i]   {rt_skipped} topicuri reale existente, omise.'))
        self.stdout.write('')
