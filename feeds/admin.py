from django.contrib import admin

from .models.site import WebSite
from .models.feed import Feed
from .models.post import Post
from .models.stats import FeedPostCount
from .models.category import Category
from .models.tag import Tag
from .models.files import FileModel
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


class WebSiteAdmin(admin.ModelAdmin):
    """
    WebSite Admin Class
    """
    list_display = ('url', 'slug', )
    inlines = [
        FeedInline,
    ]


class TagAdmin(admin.ModelAdmin):
    """
    Tag Admin Class
    """
    list_display = ('name', 'slug', 'relevant', 'touched')


class CategoryAdmin(admin.ModelAdmin):
    """
    """
    pass


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


class FeedAdmin(admin.ModelAdmin):
    """
    Feed admin options
    """
    form = FeedAdminForm
    list_display = (
        'name',
        'is_active',
        'announce_posts',
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
    list_filter = ('was_announced', 'feed', 'category', )


class FileAdmin(admin.ModelAdmin):
    """
    File admin options
    """
    list_display = (
        'data',
    )


class FeedPostCountAdmin(admin.ModelAdmin):
    """
    FeedPostCount admin options
    """
    pass

admin.site.register(FileModel, FileAdmin)
admin.site.register(WebSite, WebSiteAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FeedPostCount, FeedPostCountAdmin)
