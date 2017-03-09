from django.contrib import admin

from .models.website import WebSite
from .models.enclosure import Enclosure
from .models.feed import Feed
from .models.post import Post
from .models.stats import FeedPostCount
from .models.files import FileModel
from .models.options import Options
from .models.subscription import Subscription

from .forms import FeedAdminForm


class FeedInline(admin.TabularInline):
    """
    Inline View of Feeds, meant to display all `Feeds` per `Site`
    """
    model = Feed
    fields = ('name', 'feed_url', 'slug', )


class PostInline(admin.TabularInline):
    """
    Inline View of Posts, meant to display all `Posts` per `Feed`
    """
    model = Post
    fields = ('title', 'tweets', 'shares', 'likes')
    ordering = ('-published',)
    readonly_fields = ('title', 'tweets', 'shares', 'likes')
    can_delete = False


class SubscriptionInline(admin.TabularInline):
    model = Subscription
    fields = ('feed', )


@admin.register(Enclosure)
class EnclosureAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('post', 'enclosure_type', 'length', 'href')


def refresh_feed(modeladmin, request, queryset):
    queryset.refresh()
refresh_feed.short_description = "Refresh selected feeds"


def activate_feed(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_feed.short_description = "Activate selected feeds"


def deactivate_feed(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactivate_feed.short_description = "Deactivate selected feeds"


def reset_feed_errors(modeladmin, request, queryset):
    queryset.update(errors=0)
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
        'is_active',
        'announce_posts',
        'post_count',
        'errors',
        'slug',
        'title',
        'last_modified',
        'last_checked',
    )
    list_display_links = (
        'name',
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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Post admin options
    """
    list_display = (
        'title',
        'published',
        'updated',
        'tweets',
        'blogs',
        'plus1',
        'likes',
        'shares',
        'pageviews',
        'score',
        'was_announced',
        'updated_social',
    )
    list_filter = ('was_announced', 'feed', )


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
    list_display = ('website_url', 'slug', 'feedcount')
    inlines = [
        FeedInline,
    ]
