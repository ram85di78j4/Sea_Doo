import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

_IMAGE_LINE_RE = re.compile(
    r'^https?://\S+\.(?:jpg|jpeg|png|webp|gif)(\?[^\s]*)?$',
    re.IGNORECASE,
)


@register.filter(name='render_post_content', is_safe=True)
def render_post_content(value):
    """
    Safely renders forum post content:
    - Escapes all HTML.
    - Lines that are standalone image URLs (http/https, ending in image extension)
      are converted to responsive <img> tags.
    - All other lines are kept as plain text separated by <br>.
    """
    if not value:
        return ''

    parts = []
    for line in value.split('\n'):
        stripped = line.strip()
        if stripped and _IMAGE_LINE_RE.match(stripped):
            safe_url = escape(stripped)
            parts.append(
                f'<img src="{safe_url}" alt="Imagine partajată" '
                f'class="max-w-full rounded-xl border border-white/10 my-3 block" '
                f'loading="lazy" referrerpolicy="no-referrer">'
            )
        else:
            parts.append(escape(line) + '<br>')

    return mark_safe(''.join(parts))
