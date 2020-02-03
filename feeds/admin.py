from django.contrib import admin

from .models.files import FileModel
from .models.website import WebSite
from .models.category import Category, Tag
from .models.editorcategory import EditorCategory
from .models.enclosure import Enclosure
from .models.feed import Feed
from .models.stats import FeedPostCount
from .models.post import Post
from .models.rating import Rating
from .models.options import Options
from .models.subscription import Subscription


from .forms import FeedAdminForm


admin.site.register(EditorCategory)
admin.site.register(Category)
admin.site.register(Tag)


class PostInline(admin.TabularInline):
    """
    Post Admin.

    Inline View of Posts, meant to display all `Posts` per `Feed`
    """

    model = Post
    fields = ('title', )
    ordering = ('-published',)
    readonly_fields = ('title', )
    can_delete = False


class SubscriptionInline(admin.TabularInline):
    """
    Subscription Inline.

    Admin View of Subscription.
    """

    model = Subscription
    fields = ('feed', )


class FeedInline(admin.TabularInline):
    """
    Inline View of Feeds, meant to display all `Feeds` per `Site`
    """
    model = Feed
    fields = ('name', 'feed_url', 'slug', )


class RatingInline(admin.TabularInline):
    model = Rating


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Post admin options
    """
    list_display = (
        'title',
        'feed',
        'published',
        'updated',
    )
    list_filter = ('feed', )
    inlines = [
        RatingInline,
    ]


@admin.register(Enclosure)
class EnclosureAdmin(admin.ModelAdmin):
    """
    Admin Enclosure.

    Admin View for Enclosures.
    """

    list_display = ('post', 'enclosure_type', 'length', 'href')


def refresh_feed(modeladmin, request, queryset):
    for feed in queryset:
        feed.refresh()
refresh_feed.short_description = "Refresh selected feeds"


def activate_feed(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_feed.short_description = "Activate selected feeds"


def deactivate_feed(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactivate_feed.short_description = "Deactivate selected feeds"


def reset_feed_errors(modeladmin, request, queryset):
    queryset.update(errors=0, is_active=True)
reset_feed_errors.short_description = "Reset Feed-errors."


@admin.register(FileModel)
class FileAdmin(admin.ModelAdmin):
    """
    File admin options
    """
    list_display = (
        'data',
    )


@admin.register(FeedPostCount)
class FeedPostCountAdmin(admin.ModelAdmin):
    """
    FeedPostCount admin options
    """
    pass


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    """
    Feed admin options
    """
    form = FeedAdminForm
    list_display = (
        'name',
        'slug',
        'title',
        'website',
        'feed_url',
        'is_active',
        'post_count',
        'announce_posts',
        'errors',
        'last_modified',
        'last_checked',
    )
    list_display_links = (
        'name',
        'website',
    )
    list_editable = (
        'announce_posts',
    )
    list_filter = ('category', 'is_active', 'slug')
    inlines = [
        PostInline,
    ]
    actions = [activate_feed, deactivate_feed, refresh_feed, reset_feed_errors]


@admin.register(Options)
class OptionsAdmin(admin.ModelAdmin):
    """
    Admin-Class for User-Configuration-Options.
    """
    inlines = [
        SubscriptionInline,
    ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Class to admin User/Feed Subscriptions.
    """
    pass


@admin.register(WebSite)
class WebSiteAdmin(admin.ModelAdmin):
    """
    WebSite Admin Class
    """
    list_display = ('name', 'netloc', 'path', 'slug', 'feedcount')
    inlines = [
        FeedInline,
    ]
