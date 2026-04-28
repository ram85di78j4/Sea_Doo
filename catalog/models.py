from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class JetSki(models.Model):
    STATUS_CHOICES = [
        ('in_collection', 'În colecție'),
        ('available', 'Disponibil'),
        ('sold', 'Vândut'),
        ('favorite', 'Favorit'),
    ]

    title = models.CharField(max_length=200, verbose_name='Titlu')
    brand = models.CharField(max_length=100, verbose_name='Marcă')
    model = models.CharField(max_length=100, verbose_name='Model')
    year = models.PositiveIntegerField(verbose_name='An')
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Slug URL',
        help_text='Generat automat. Nu modifica dacă nu știi ce faci.',
    )
    engine = models.CharField(max_length=200, verbose_name='Motor')
    horsepower = models.PositiveIntegerField(verbose_name='Cai putere')
    condition = models.CharField(max_length=200, verbose_name='Stare')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_collection',
        verbose_name='Status',
    )
    short_description = models.TextField(max_length=500, verbose_name='Descriere scurtă')
    full_description = models.TextField(verbose_name='Povestea acestui model', blank=True)
    why_worth_seeing = models.TextField(verbose_name='De ce merită văzut', blank=True)
    main_image = models.ImageField(
        upload_to='jetski/',
        blank=True,
        null=True,
        verbose_name='Imagine principală',
    )
    video_url = models.URLField(blank=True, null=True, verbose_name='URL Video')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creat la')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizat la')

    class Meta:
        verbose_name = 'Jet-Ski'
        verbose_name_plural = 'Jet-Ski-uri'
        ordering = ['-year', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand}-{self.model}-{self.year}")
            candidate = base_slug
            counter = 1
            while JetSki.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} — {self.title}"


class JetSkiImage(models.Model):
    jetski = models.ForeignKey(
        JetSki,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Jet-Ski',
    )
    image = models.ImageField(upload_to='jetski/gallery/', verbose_name='Imagine')
    caption = models.CharField(max_length=300, blank=True, verbose_name='Descriere imagine')
    order = models.PositiveIntegerField(default=0, verbose_name='Ordine afișare')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Adăugat la')

    class Meta:
        verbose_name = 'Imagine galerie'
        verbose_name_plural = 'Imagini galerie'
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Imagine #{self.order} — {self.jetski}"


class ForumCategory(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nume categorie')
    slug = models.SlugField(max_length=160, unique=True, verbose_name='Slug URL')
    description = models.TextField(max_length=500, blank=True, verbose_name='Descriere')
    icon = models.CharField(max_length=10, default='💬', verbose_name='Emoji icon')
    order = models.PositiveIntegerField(default=0, verbose_name='Ordine afișare')
    is_active = models.BooleanField(default=True, verbose_name='Activ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creat la')

    class Meta:
        verbose_name = 'Categorie forum'
        verbose_name_plural = 'Categorii forum'
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ForumTopicPreview(models.Model):
    category = models.ForeignKey(
        ForumCategory,
        on_delete=models.CASCADE,
        related_name='topics',
        verbose_name='Categorie',
    )
    title = models.CharField(max_length=300, verbose_name='Titlu subiect')
    slug = models.SlugField(max_length=320, blank=True, verbose_name='Slug URL')
    author_name = models.CharField(max_length=100, default='Membru', verbose_name='Autor')
    replies_count = models.PositiveIntegerField(default=0, verbose_name='Răspunsuri')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Vizualizări')
    last_activity = models.DateTimeField(auto_now_add=True, verbose_name='Ultima activitate')
    is_pinned = models.BooleanField(default=False, verbose_name='Fixat')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creat la')

    class Meta:
        verbose_name = 'Subiect forum (preview)'
        verbose_name_plural = 'Subiecte forum (preview)'
        ordering = ['-is_pinned', '-last_activity']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            candidate = base
            counter = 1
            while ForumTopicPreview.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.category}] {self.title}"


class CommunityWaitlist(models.Model):
    BRAND_CHOICES = [
        ('sea-doo', 'Sea-Doo'),
        ('yamaha', 'Yamaha'),
        ('kawasaki', 'Kawasaki'),
        ('other', 'Alt brand'),
        ('none', 'Nu am încă'),
    ]

    name = models.CharField(max_length=200, verbose_name='Nume')
    email = models.EmailField(unique=True, verbose_name='Email')
    city = models.CharField(max_length=100, blank=True, verbose_name='Oraș')
    owns_jetski = models.BooleanField(default=False, verbose_name='Deține jet-ski')
    favorite_brand = models.CharField(
        max_length=20,
        choices=BRAND_CHOICES,
        blank=True,
        verbose_name='Brand preferat',
    )
    message = models.TextField(blank=True, verbose_name='Mesaj opțional')
    wants_updates = models.BooleanField(
        default=False,
        verbose_name='Dorește noutăți',
        help_text='Bifat: vrea să primească noutăți despre lansare și evenimente',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Înscris la')

    class Meta:
        verbose_name = 'Înscriere comunitate'
        verbose_name_plural = 'Înscrieri comunitate'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} <{self.email}>"


class EventPreview(models.Model):
    title = models.CharField(max_length=200, verbose_name='Titlu eveniment')
    slug = models.SlugField(max_length=220, unique=True, blank=True, verbose_name='Slug URL')
    location = models.CharField(max_length=200, verbose_name='Locatie')
    event_date = models.DateField(verbose_name='Data eveniment')
    short_description = models.TextField(max_length=500, verbose_name='Descriere scurta')
    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True,
        verbose_name='Imagine eveniment',
    )
    is_active = models.BooleanField(default=True, verbose_name='Activ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creat la')

    class Meta:
        verbose_name = 'Eveniment (preview)'
        verbose_name_plural = 'Evenimente (preview)'
        ordering = ['event_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            candidate = base
            counter = 1
            while EventPreview.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} — {self.event_date}"


class Testimonial(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    name = models.CharField(max_length=150, verbose_name='Nume')
    city = models.CharField(max_length=100, blank=True, verbose_name='Oras')
    message = models.TextField(max_length=600, verbose_name='Mesaj')
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=5,
        verbose_name='Rating (1-5)',
    )
    is_active = models.BooleanField(default=True, verbose_name='Activ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Adaugat la')

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimoniale'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.city}) — {self.rating} stele"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nume')
    email = models.EmailField(verbose_name='Email')
    message = models.TextField(verbose_name='Mesaj')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Trimis la')
    is_read = models.BooleanField(default=False, verbose_name='Citit')

    class Meta:
        verbose_name = 'Mesaj contact'
        verbose_name_plural = 'Mesaje contact'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} <{self.email}>"


class SiteSetting(models.Model):
    key = models.CharField(max_length=100, unique=True, verbose_name='Cheie')
    value = models.TextField(blank=True, verbose_name='Valoare')
    description = models.CharField(max_length=300, blank=True, verbose_name='Descriere')
    is_public = models.BooleanField(
        default=True,
        verbose_name='Public',
        help_text='Valoarea este accesibila in template-uri',
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizat la')

    class Meta:
        verbose_name = 'Setare site'
        verbose_name_plural = 'Setari site'
        ordering = ['key']

    def __str__(self):
        return f"{self.key} = {self.value[:60]}"


def get_site_setting(key, fallback=''):
    from django.conf import settings as django_settings
    try:
        obj = SiteSetting.objects.get(key=key)
        return obj.value if obj.value else fallback
    except SiteSetting.DoesNotExist:
        return getattr(django_settings, key, fallback)


class MemberProfile(models.Model):
    BRAND_CHOICES = [
        ('sea-doo', 'Sea-Doo'),
        ('yamaha', 'Yamaha'),
        ('kawasaki', 'Kawasaki'),
        ('other', 'Alt brand'),
        ('none', 'Nu am încă'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Utilizator',
    )
    city = models.CharField(max_length=100, blank=True, verbose_name='Oraș')
    owns_jetski = models.BooleanField(default=False, verbose_name='Deține jet-ski')
    favorite_brand = models.CharField(
        max_length=20,
        choices=BRAND_CHOICES,
        blank=True,
        verbose_name='Brand preferat',
    )
    bio = models.TextField(blank=True, max_length=500, verbose_name='Despre mine')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar',
    )
    show_in_directory = models.BooleanField(
        default=True,
        verbose_name='Vizibil în directorul membrilor',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Înregistrat la')

    class Meta:
        verbose_name = 'Profil membru'
        verbose_name_plural = 'Profile membri'
        ordering = ['-created_at']

    def __str__(self):
        return f"Profil: {self.user.get_full_name() or self.user.username}"

    def get_badges(self):
        badges = []
        badges.append({'key': 'beta', 'label': 'Membru Beta', 'color': 'cyan'})
        if self.owns_jetski:
            badges.append({'key': 'owner', 'label': 'Proprietar jet-ski', 'color': 'yellow'})
        topic_count = self.user.forum_topics.filter(is_deleted=False).count()
        reply_count = self.user.forum_replies.filter(is_deleted=False).count()
        if topic_count + reply_count >= 10:
            badges.append({'key': 'active', 'label': 'Activ în forum', 'color': 'green'})
        if topic_count >= 5:
            badges.append({'key': 'contributor', 'label': 'Contributor', 'color': 'orange'})
        return badges


class ForumTopic(models.Model):
    category = models.ForeignKey(
        ForumCategory,
        on_delete=models.CASCADE,
        related_name='real_topics',
        verbose_name='Categorie',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forum_topics',
        verbose_name='Autor',
    )
    title = models.CharField(max_length=300, verbose_name='Titlu')
    slug = models.SlugField(max_length=320, unique=True, blank=True, verbose_name='Slug URL')
    content = models.TextField(verbose_name='Conținut')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Vizualizări')
    is_pinned = models.BooleanField(default=False, verbose_name='Fixat')
    is_locked = models.BooleanField(default=False, verbose_name='Blocat')
    is_deleted = models.BooleanField(default=False, verbose_name='Șters')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Șters la')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creat la')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizat la')

    class Meta:
        verbose_name = 'Subiect forum'
        verbose_name_plural = 'Subiecte forum'
        ordering = ['-is_pinned', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            candidate = base or 'topic'
            counter = 1
            while ForumTopic.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def replies_count(self):
        return self.replies.filter(is_deleted=False).count()


class ForumReply(models.Model):
    topic = models.ForeignKey(
        ForumTopic,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='Subiect',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forum_replies',
        verbose_name='Autor',
    )
    content = models.TextField(verbose_name='Conținut')
    is_deleted = models.BooleanField(default=False, verbose_name='Șters')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Șters la')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creat la')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizat la')

    class Meta:
        verbose_name = 'Răspuns forum'
        verbose_name_plural = 'Răspunsuri forum'
        ordering = ['created_at']

    def __str__(self):
        return f'Raspuns de {self.author.get_full_name() or self.author.email} la "{self.topic.title}"'


class ForumReport(models.Model):
    STATUS_CHOICES = [
        ('new', 'Nou'),
        ('reviewed', 'Verificat'),
        ('dismissed', 'Respins'),
    ]
    REASON_CHOICES = [
        ('spam', 'Spam sau reclame'),
        ('offensive', 'Conținut ofensator'),
        ('misinformation', 'Informații false'),
        ('personal_data', 'Date personale expuse'),
        ('scam', 'Tentativă de înșelăciune'),
        ('other', 'Alt motiv'),
    ]

    reporter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='forum_reports',
        verbose_name='Raportat de',
    )
    topic = models.ForeignKey(
        ForumTopic,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name='Subiect raportat',
    )
    reply = models.ForeignKey(
        ForumReply,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='reports',
        verbose_name='Răspuns raportat',
    )
    reason = models.CharField(
        max_length=30,
        choices=REASON_CHOICES,
        verbose_name='Motiv',
    )
    details = models.TextField(
        blank=True,
        max_length=1000,
        verbose_name='Detalii suplimentare',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Status',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Raportat la')
    reviewed_at = models.DateTimeField(null=True, blank=True, verbose_name='Verificat la')

    class Meta:
        verbose_name = 'Raport forum'
        verbose_name_plural = 'Rapoarte forum'
        ordering = ['-created_at']

    def __str__(self):
        target = f'subiect #{self.topic_id}' if self.topic_id else f'raspuns #{self.reply_id}'
        return f'Raport {target} de {self.reporter.email} ({self.get_status_display()})'
