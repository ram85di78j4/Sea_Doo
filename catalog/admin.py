from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import JetSki, JetSkiImage, ContactMessage, ForumCategory, ForumTopicPreview, ForumTopic, ForumReply, ForumReport, CommunityWaitlist, EventPreview, Testimonial, SiteSetting, MemberProfile


class JetSkiImageInline(admin.TabularInline):
    model = JetSkiImage
    extra = 3
    fields = ('image', 'caption', 'order', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:4px;" />',
                obj.image.url,
            )
        return '—'
    image_preview.short_description = 'Preview'


@admin.register(JetSkiImage)
class JetSkiImageAdmin(admin.ModelAdmin):
    list_display = ('jetski', 'order', 'caption', 'image_preview')
    list_filter = ('jetski',)
    ordering = ('jetski', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px; border-radius:4px;" />',
                obj.image.url,
            )
        return '—'
    image_preview.short_description = 'Preview'


@admin.register(JetSki)
class JetSkiAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'brand', 'model', 'year', 'horsepower', 'status')
    list_filter = ('status', 'brand', 'year')
    search_fields = ('title', 'brand', 'model', 'engine')
    list_editable = ('status',)
    readonly_fields = ('slug', 'created_at', 'updated_at', 'image_preview')
    inlines = [JetSkiImageInline]
    fieldsets = (
        ('Informații generale', {
            'fields': ('title', 'brand', 'model', 'year', 'status', 'slug'),
        }),
        ('Specificații tehnice', {
            'fields': ('engine', 'horsepower', 'condition'),
        }),
        ('Descriere', {
            'fields': ('short_description', 'full_description', 'why_worth_seeing'),
        }),
        ('Media', {
            'fields': ('main_image', 'image_preview', 'video_url'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="height:48px; border-radius:4px;" />',
                obj.main_image.url,
            )
        return '—'
    image_preview.short_description = 'Foto'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'message', 'created_at')
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} mesaje marcate ca citite.')
    mark_as_read.short_description = 'Marchează ca citite'


class ForumTopicPreviewInline(admin.TabularInline):
    model = ForumTopicPreview
    extra = 2
    fields = ('title', 'author_name', 'replies_count', 'views_count', 'is_pinned')
    show_change_link = True


@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'slug', 'order', 'is_active', 'topic_count')
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ForumTopicPreviewInline]

    def topic_count(self, obj):
        return obj.topics.count()
    topic_count.short_description = 'Subiecte'


@admin.register(ForumTopicPreview)
class ForumTopicPreviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author_name', 'replies_count', 'views_count', 'is_pinned', 'last_activity')
    list_filter = ('category', 'is_pinned')
    list_editable = ('is_pinned',)
    search_fields = ('title', 'author_name')
    ordering = ('-is_pinned', '-last_activity')


@admin.register(CommunityWaitlist)
class CommunityWaitlistAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'owns_jetski', 'favorite_brand', 'created_at')
    list_filter = ('owns_jetski', 'favorite_brand')
    search_fields = ('name', 'email', 'city')
    readonly_fields = ('name', 'email', 'city', 'owns_jetski', 'favorite_brand', 'message', 'created_at')
    ordering = ('-created_at',)


@admin.register(EventPreview)
class EventPreviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'event_date', 'is_active', 'image_preview')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    search_fields = ('title', 'location')
    readonly_fields = ('slug', 'image_preview')
    ordering = ('event_date',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:40px; border-radius:4px;" />',
                obj.image.url,
            )
        return '—'
    image_preview.short_description = 'Foto'


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating')
    list_editable = ('is_active',)
    search_fields = ('name', 'city', 'message')
    ordering = ('-created_at',)


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value_preview', 'description', 'is_public', 'updated_at')
    list_filter = ('is_public',)
    list_editable = ('is_public',)
    search_fields = ('key', 'value', 'description')
    readonly_fields = ('updated_at',)
    ordering = ('key',)

    def value_preview(self, obj):
        return obj.value[:80] + '…' if len(obj.value) > 80 else obj.value
    value_preview.short_description = 'Valoare'


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'full_name', 'city', 'favorite_brand', 'owns_jetski', 'show_in_directory', 'created_at')
    list_filter = ('owns_jetski', 'show_in_directory', 'favorite_brand')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'city', 'favorite_brand')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    list_editable = ('show_in_directory',)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'

    def full_name(self, obj):
        return obj.user.get_full_name() or '—'
    full_name.short_description = 'Nume'


class ForumReplyInline(admin.TabularInline):
    model = ForumReply
    extra = 0
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('created_at',)
    show_change_link = True


@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author_email', 'replies_count_display', 'views_count', 'is_pinned', 'is_locked', 'created_at')
    list_filter = ('category', 'is_pinned', 'is_locked')
    search_fields = ('title', 'content', 'author__email', 'author__first_name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'views_count')
    ordering = ('-created_at',)
    list_editable = ('is_pinned', 'is_locked')
    actions = ['pin_topics', 'unpin_topics', 'lock_topics', 'unlock_topics', 'soft_delete_topics']
    inlines = [ForumReplyInline]

    @admin.action(description='Fixează subiectele selectate')
    def pin_topics(self, request, queryset):
        queryset.update(is_pinned=True)

    @admin.action(description='Desfixează subiectele selectate')
    def unpin_topics(self, request, queryset):
        queryset.update(is_pinned=False)

    @admin.action(description='Blochează subiectele selectate')
    def lock_topics(self, request, queryset):
        queryset.update(is_locked=True)

    @admin.action(description='Deblochează subiectele selectate')
    def unlock_topics(self, request, queryset):
        queryset.update(is_locked=False)

    @admin.action(description='Șterge (soft) subiectele selectate')
    def soft_delete_topics(self, request, queryset):
        queryset.update(is_deleted=True, deleted_at=timezone.now())

    def author_email(self, obj):
        return obj.author.email
    author_email.short_description = 'Autor'
    author_email.admin_order_field = 'author__email'

    def replies_count_display(self, obj):
        return obj.replies.count()
    replies_count_display.short_description = 'Răspunsuri'


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'topic', 'author_email', 'is_deleted', 'created_at')
    list_filter = ('topic__category', 'is_deleted')
    search_fields = ('content', 'author__email', 'topic__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    actions = ['soft_delete_replies', 'restore_replies']

    def author_email(self, obj):
        return obj.author.email
    author_email.short_description = 'Autor'

    def short_content(self, obj):
        return obj.content[:80] + '…' if len(obj.content) > 80 else obj.content
    short_content.short_description = 'Conținut'

    @admin.action(description='Șterge (soft) răspunsurile selectate')
    def soft_delete_replies(self, request, queryset):
        queryset.update(is_deleted=True, deleted_at=timezone.now())

    @admin.action(description='Restaurează răspunsurile selectate')
    def restore_replies(self, request, queryset):
        queryset.update(is_deleted=False, deleted_at=None)


@admin.register(ForumReport)
class ForumReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_badge', 'reporter_email', 'target_link', 'reason_display', 'created_at')
    list_filter = ('status', 'reason')
    search_fields = ('reporter__email', 'topic__title', 'details')
    readonly_fields = ('reporter', 'topic', 'reply', 'reason', 'details', 'created_at', 'reviewed_at')
    ordering = ('-created_at',)
    actions = ['mark_reviewed', 'dismiss_reports']

    def reporter_email(self, obj):
        return obj.reporter.email
    reporter_email.short_description = 'Reporter'

    def reason_display(self, obj):
        return obj.get_reason_display()
    reason_display.short_description = 'Motiv'

    def target_link(self, obj):
        if obj.topic:
            return format_html('<a href="/forum/topic/{}/">Subiect: {}</a>', obj.topic.slug, obj.topic.title[:50])
        if obj.reply:
            return format_html('Răspuns #{} la: {}', obj.reply.pk, obj.reply.topic.title[:40])
        return '—'
    target_link.short_description = 'țintă'

    def status_badge(self, obj):
        colors = {'new': '#ef4444', 'reviewed': '#22c55e', 'dismissed': '#6b7280'}
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="color:{};font-weight:bold">● {}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    @admin.action(description='Marchează ca Verificat')
    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed', reviewed_at=timezone.now())

    @admin.action(description='Respinge rapoartele selectate')
    def dismiss_reports(self, request, queryset):
        queryset.update(status='dismissed', reviewed_at=timezone.now())
