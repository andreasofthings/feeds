from django.contrib import admin

from feeds.models import Feed, Post, FeedPostCount, Category, Tag
from feeds.forms import FeedAdminForm

class TagAdmin(admin.ModelAdmin):
    """
    Tag Admin Class
    """
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class FeedAdmin(admin.ModelAdmin):
    """
    Feed admin options
    """
    form = FeedAdminForm
    list_display = ('name', 'is_active', 'beta', 'slug', 'title', 'last_modified', 'last_checked', )
    list_display_links = ('name', 'is_active', 'beta',)
    list_filter = ('category', 'is_active', 'beta', 'slug')

class PostAdmin(admin.ModelAdmin):
    """
    Post admin options
    """
    list_display = ('title', 'created', 'tweets', 'blogs', 'plus1', 'likes', 'shares', 'pageviews', 'score', 'was_announced', 'updated_social',)
    list_filter = ('was_announced',)

class FeedPostCountAdmin(admin.ModelAdmin):
    """
    FeedPostCount admin options
    """
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FeedPostCount, FeedPostCountAdmin)




