from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from .models import JetSki, ForumCategory, ForumTopicPreview, ForumTopic, ForumReply, ForumReport, CommunityWaitlist, EventPreview, Testimonial, MemberProfile
from .forms import ContactForm, CommunityWaitlistForm, RegistrationForm, ProfileEditForm, ForumTopicForm, ForumReplyForm, ForumReportForm


def home(request):
    featured = JetSki.objects.filter(status='favorite')[:3]
    recent = JetSki.objects.all()[:6]
    forum_categories = ForumCategory.objects.filter(is_active=True)[:8]
    events = EventPreview.objects.filter(is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesajul tau a fost trimis! Te vom contacta in curand.')
            return redirect('home')

    context = {
        'featured': featured,
        'recent': recent,
        'form': form,
        'forum_categories': forum_categories,
        'events': events,
        'testimonials': testimonials,
        'HERO_VIDEO_URL': getattr(settings, 'HERO_VIDEO_URL', ''),
        'FORUM_EXTERNAL_URL': getattr(settings, 'FORUM_EXTERNAL_URL', ''),
    }
    return render(request, 'catalog/home.html', context)


def comunitate(request):
    categories = ForumCategory.objects.filter(is_active=True)
    waitlist_count = CommunityWaitlist.objects.count()
    events = EventPreview.objects.filter(is_active=True)[:3]
    waitlist_form = CommunityWaitlistForm()

    real_pinned = ForumTopic.objects.filter(is_pinned=True, is_deleted=False).select_related('author', 'category').order_by('-created_at')[:5]
    real_latest = ForumTopic.objects.filter(is_pinned=False, is_deleted=False).select_related('author', 'category').order_by('-created_at')[:10]
    use_real_topics = real_pinned.exists() or real_latest.exists()

    pinned_topics = ForumTopicPreview.objects.filter(is_pinned=True).select_related('category')[:5]
    latest_topics = ForumTopicPreview.objects.filter(is_pinned=False).select_related('category')[:10]

    if request.method == 'POST':
        waitlist_form = CommunityWaitlistForm(request.POST)
        if waitlist_form.is_valid():
            waitlist_form.save()
            messages.success(
                request,
                'Felicitări! Ești pe lista de așteptare. Te vom contacta la lansarea comunității.'
            )
            return redirect(reverse('comunitate') + '?joined=1#inscrie-te')

    context = {
        'categories': categories,
        'use_real_topics': use_real_topics,
        'real_pinned': real_pinned,
        'real_latest': real_latest,
        'pinned_topics': pinned_topics,
        'latest_topics': latest_topics,
        'waitlist_count': waitlist_count,
        'events': events,
        'waitlist_form': waitlist_form,
        'FORUM_EXTERNAL_URL': getattr(settings, 'FORUM_EXTERNAL_URL', ''),
    }
    return render(request, 'catalog/comunitate.html', context)


def sitemap_xml(request):
    base = f"{request.scheme}://{request.get_host()}"
    jetskis = JetSki.objects.exclude(slug__isnull=True).exclude(slug='')
    content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    static_urls = ['', 'catalog/', 'comunitate/', 'despre/', 'contact/', 'termeni/', 'confidentialitate/']
    for path in static_urls:
        content += f'  <url><loc>{base}/{path}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>\n'
    for js in jetskis:
        content += f'  <url><loc>{base}/catalog/{js.slug}/</loc><changefreq>monthly</changefreq><priority>0.6</priority></url>\n'
    content += '</urlset>'
    return HttpResponse(content, content_type='application/xml')


def robots_txt(request):
    base = f"{request.scheme}://{request.get_host()}"
    content = f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {base}/sitemap.xml\n"
    return HttpResponse(content, content_type='text/plain')


def health_check(request):
    return JsonResponse({'status': 'ok', 'app': 'Sea_Doo'})


def catalog_list(request):
    jetskis = JetSki.objects.all()

    search = request.GET.get('search', '').strip()
    brand = request.GET.get('brand', '')
    year = request.GET.get('year', '')
    status = request.GET.get('status', '')

    if search:
        jetskis = jetskis.filter(
            Q(title__icontains=search) |
            Q(brand__icontains=search) |
            Q(model__icontains=search) |
            Q(engine__icontains=search)
        )
    if brand:
        jetskis = jetskis.filter(brand__icontains=brand)
    if year:
        jetskis = jetskis.filter(year=year)
    if status:
        jetskis = jetskis.filter(status=status)

    brands = JetSki.objects.values_list('brand', flat=True).distinct().order_by('brand')
    years = JetSki.objects.values_list('year', flat=True).distinct().order_by('-year')

    context = {
        'jetskis': jetskis,
        'brands': brands,
        'years': years,
        'status_choices': JetSki.STATUS_CHOICES,
        'selected_search': search,
        'selected_brand': brand,
        'selected_year': year,
        'selected_status': status,
    }
    return render(request, 'catalog/catalog_list.html', context)


def catalog_detail(request, slug):
    jetski = get_object_or_404(JetSki, slug=slug)
    gallery = jetski.images.all()
    related = JetSki.objects.filter(brand=jetski.brand).exclude(pk=jetski.pk)[:3]
    context = {
        'jetski': jetski,
        'gallery': gallery,
        'related': related,
    }
    return render(request, 'catalog/catalog_detail.html', context)


def about_page(request):
    return render(request, 'catalog/about.html')


def contact_page(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mesajul tău a fost trimis! Te vom contacta în curând.')
            return redirect('contact_page')
    return render(request, 'catalog/contact_page.html', {'form': form})


def terms_page(request):
    return render(request, 'catalog/terms.html')


def privacy_page(request):
    return render(request, 'catalog/privacy.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Bine ai venit, {user.first_name or user.email}! Contul tău a fost creat.')
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'catalog/register.html', {'form': form})


@login_required
def profile_view(request):
    profile, _ = MemberProfile.objects.get_or_create(user=request.user)
    my_topics = request.user.forum_topics.filter(is_deleted=False).select_related('category').order_by('-created_at')[:5]
    my_replies = request.user.forum_replies.filter(is_deleted=False).select_related('topic').order_by('-created_at')[:5]
    my_report_count = ForumReport.objects.filter(reporter=request.user).count()
    badges = profile.get_badges()
    return render(request, 'catalog/profile.html', {
        'profile': profile,
        'my_topics': my_topics,
        'my_replies': my_replies,
        'my_report_count': my_report_count,
        'badges': badges,
    })


@login_required
def profile_edit_view(request):
    profile, _ = MemberProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.save(update_fields=['first_name'])
            form.save()
            messages.success(request, 'Profilul tău a fost actualizat.')
            return redirect('profile')
    else:
        form = ProfileEditForm(
            instance=profile,
            initial={'first_name': request.user.first_name},
        )
    return render(request, 'catalog/profile_edit.html', {'form': form, 'profile': profile})


def forum_index(request):
    categories = ForumCategory.objects.filter(is_active=True).prefetch_related('real_topics')

    q = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'latest')
    category_slug = request.GET.get('categorie', '')
    pinned_only = request.GET.get('fixate', '') == '1'

    topics_qs = ForumTopic.objects.filter(is_deleted=False).select_related('author', 'category')

    if q:
        topics_qs = topics_qs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q) |
            Q(author__first_name__icontains=q) |
            Q(author__email__icontains=q) |
            Q(category__name__icontains=q)
        )

    if category_slug:
        topics_qs = topics_qs.filter(category__slug=category_slug)

    if pinned_only:
        topics_qs = topics_qs.filter(is_pinned=True)

    if sort == 'views':
        topics_qs = topics_qs.order_by('-views_count', '-created_at')
    elif sort == 'replies':
        topics_qs = topics_qs.annotate(
            reply_count=Count('replies', filter=Q(replies__is_deleted=False))
        ).order_by('-reply_count', '-created_at')
    else:
        topics_qs = topics_qs.order_by('-is_pinned', '-created_at')

    paginator = Paginator(topics_qs, 10)
    page_obj = paginator.get_page(request.GET.get('pagina', 1))

    selected_category = None
    if category_slug:
        selected_category = ForumCategory.objects.filter(slug=category_slug, is_active=True).first()

    return render(request, 'catalog/forum_index.html', {
        'categories': categories,
        'page_obj': page_obj,
        'q': q,
        'sort': sort,
        'category_slug': category_slug,
        'pinned_only': pinned_only,
        'selected_category': selected_category,
    })


def forum_category(request, slug):
    category = get_object_or_404(ForumCategory, slug=slug, is_active=True)
    topics_qs = ForumTopic.objects.filter(category=category, is_deleted=False).select_related('author').order_by('-is_pinned', '-created_at')
    topic_count = topics_qs.count()
    latest_topic = topics_qs.first()
    latest_activity = latest_topic.created_at if latest_topic else None
    paginator = Paginator(topics_qs, 10)
    page_obj = paginator.get_page(request.GET.get('pagina', 1))
    return render(request, 'catalog/forum_category.html', {
        'category': category,
        'page_obj': page_obj,
        'topic_count': topic_count,
        'latest_activity': latest_activity,
    })


def topic_detail(request, slug):
    topic = get_object_or_404(ForumTopic, slug=slug, is_deleted=False)
    ForumTopic.objects.filter(pk=topic.pk).update(views_count=topic.views_count + 1)
    topic.refresh_from_db(fields=['views_count'])
    replies_qs = topic.replies.filter(is_deleted=False).select_related('author', 'author__profile').order_by('created_at')
    reply_count = replies_qs.count()
    related_topics = ForumTopic.objects.filter(
        category=topic.category, is_deleted=False
    ).exclude(pk=topic.pk).order_by('-created_at')[:5]
    paginator = Paginator(replies_qs, 10)
    page_obj = paginator.get_page(request.GET.get('pagina', 1))
    reply_form = None
    reported_topic_ids = set()
    reported_reply_ids = set()
    if request.user.is_authenticated:
        if not topic.is_locked:
            reply_form = ForumReplyForm()
        reported_topic_ids = set(
            ForumReport.objects.filter(reporter=request.user, topic=topic).values_list('topic_id', flat=True)
        )
        reported_reply_ids = set(
            ForumReport.objects.filter(reporter=request.user, reply__in=replies_qs).values_list('reply_id', flat=True)
        )
    return render(request, 'catalog/topic_detail.html', {
        'topic': topic,
        'page_obj': page_obj,
        'reply_count': reply_count,
        'related_topics': related_topics,
        'reply_form': reply_form,
        'reported_topic_ids': reported_topic_ids,
        'reported_reply_ids': reported_reply_ids,
    })


@login_required
def topic_new(request):
    if request.method == 'POST':
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            messages.success(request, 'Subiectul a fost creat cu succes.')
            return redirect('topic_detail', slug=topic.slug)
    else:
        category_slug = request.GET.get('categorie')
        initial = {}
        if category_slug:
            try:
                initial['category'] = ForumCategory.objects.get(slug=category_slug, is_active=True)
            except ForumCategory.DoesNotExist:
                pass
        form = ForumTopicForm(initial=initial)
    return render(request, 'catalog/topic_form.html', {'form': form, 'editing': False})


@login_required
def topic_reply(request, slug):
    topic = get_object_or_404(ForumTopic, slug=slug, is_deleted=False)
    if topic.is_locked:
        messages.error(request, 'Acest subiect este blocat. Nu se mai pot adăuga răspunsuri.')
        return redirect('topic_detail', slug=slug)
    if request.method == 'POST':
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.topic = topic
            reply.author = request.user
            reply.save()
            return redirect(f"{reverse('topic_detail', kwargs={'slug': slug})}#reply-{reply.pk}")


@login_required
def report_topic(request, pk):
    topic = get_object_or_404(ForumTopic, pk=pk, is_deleted=False)
    if topic.author == request.user:
        messages.error(request, 'Nu poți raporta propriul subiect.')
        return redirect('topic_detail', slug=topic.slug)
    if ForumReport.objects.filter(reporter=request.user, topic=topic).exists():
        messages.info(request, 'Ai raportat deja acest subiect.')
        return redirect('topic_detail', slug=topic.slug)
    if request.method == 'POST':
        form = ForumReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.topic = topic
            report.save()
            messages.success(request, 'Raportul tău a fost trimis. Îl vom verifica în curând.')
            return redirect('topic_detail', slug=topic.slug)
    else:
        form = ForumReportForm()
    return render(request, 'catalog/report_form.html', {
        'form': form,
        'target_type': 'topic',
        'target': topic,
    })


@login_required
def report_reply(request, pk):
    reply = get_object_or_404(ForumReply, pk=pk, is_deleted=False)
    if reply.author == request.user:
        messages.error(request, 'Nu poți raporta propriul răspuns.')
        return redirect('topic_detail', slug=reply.topic.slug)
    if ForumReport.objects.filter(reporter=request.user, reply=reply).exists():
        messages.info(request, 'Ai raportat deja acest răspuns.')
        return redirect('topic_detail', slug=reply.topic.slug)
    if request.method == 'POST':
        form = ForumReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reply = reply
            report.save()
            messages.success(request, 'Raportul tău a fost trimis. Îl vom verifica în curând.')
            return redirect('topic_detail', slug=reply.topic.slug)
    else:
        form = ForumReportForm()
    return render(request, 'catalog/report_form.html', {
        'form': form,
        'target_type': 'reply',
        'target': reply,
    })


def forum_rules(request):
    return render(request, 'catalog/forum_rules.html')


def member_directory(request):
    members = MemberProfile.objects.filter(
        show_in_directory=True,
    ).select_related('user').order_by('-created_at')
    return render(request, 'catalog/member_directory.html', {'members': members})


def member_public_profile(request, username):
    from django.contrib.auth.models import User
    member_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(MemberProfile, user=member_user, show_in_directory=True)
    topics = member_user.forum_topics.filter(is_deleted=False).select_related('category').order_by('-created_at')[:10]
    replies = member_user.forum_replies.filter(is_deleted=False).select_related('topic').order_by('-created_at')[:10]
    badges = profile.get_badges()
    return render(request, 'catalog/member_profile.html', {
        'profile': profile,
        'topics': topics,
        'replies': replies,
        'badges': badges,
    })
