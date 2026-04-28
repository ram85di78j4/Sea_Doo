from django.conf import settings as django_settings

_SITE_KEYS = [
    'SITE_NAME',
    'SITE_TAGLINE',
    'SITE_DESCRIPTION',
    'CONTACT_EMAIL',
    'CONTACT_PHONE',
    'INSTAGRAM_URL',
    'TIKTOK_URL',
    'YOUTUBE_URL',
    'FORUM_EXTERNAL_URL',
    'HERO_VIDEO_URL',
    'LAUNCH_BANNER_ENABLED',
    'LAUNCH_BANNER_TEXT',
    'LAUNCH_BANNER_CTA_TEXT',
    'LAUNCH_BANNER_CTA_URL',
]


def site_settings(request):
    ctx = {key: getattr(django_settings, key, '') for key in _SITE_KEYS}

    try:
        from .models import SiteSetting
        overrides = SiteSetting.objects.filter(is_public=True).values_list('key', 'value')
        for key, value in overrides:
            if key in _SITE_KEYS and value:
                ctx[key] = value
    except Exception:
        pass

    return ctx
