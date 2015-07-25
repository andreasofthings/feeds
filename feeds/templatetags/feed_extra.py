from django import template
from ..models import Feed, Post

register = template.Library()


class RecentPostNode(template.Node):
    """
    TemplateTag RenderNode

    renders recent posts for a feed.(pk)
    """
    def __init__(self, feed, count=5):
        self.feed = template.Variable(feed)
        self.max_posts = int(count)

    def render(self, context):
        try:
            feed = self.feed.resolve(context)
        except Feed.MultipleObjectsReturned:
            raise template.TemplateSyntaxError(
                """
                'recent_posts' template tag requires 'feed' as first argument.
                Got this instead:
                %r (type: %r)
                """ %
                self.feed, type(self.feed)
            )
        try:
            recent = Post.objects.filter(
                feed=feed
            ).order_by('-published')[:self.max_posts]
        except Post.DoesNotExist:
            recent = Post.objects.none()
        return recent


@register.tag('recent_posts')
def recent_posts(parser, token):
    """
    recent_posts
    ============

    Templatetag to render recent posts for a feed.
    """
    try:
        tag_name, feed, max_posts = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires two arguments" %
            token.contents.split()[0]
        )
    return RecentPostNode(feed, max_posts)


class FeedControlsNode(template.Node):
    """
    TemplateTag RenderNode

    renders controls for a feed object.
    """
    def __init__(self, feed):
        self.feed = template.Variable(feed)

    def render(self, context):
        try:
            feed = self.feed.resolve(context)
        except Feed.MultipleObjectsReturned:
            raise template.TemplateSyntaxError(
                """
                'feed_controls' template tag requires 'feed' as first argument.
                Got this instead:
                %r (type: %r)
                """ %
                self.feed, type(self.feed)
            )
        result = """
          <a href="{{feed.get_absolute_url}}" class="btn btn-xs" role="button" data-toggle="tooltip" data-placement="top" title="{% trans "View Feed" %}"><span class="glyphicon glyphicon-zoom-in"></span></a>
          {% if user.is_authenticated %}
          {% if perms.feeds.can_refresh_feed %}<a href="{{feed.get_absolute_url}}refresh" class="btn btn-mini feeds-tooltip" role="button" title="refresh feed"><span class="glyphicon glyphicon-refresh"></span></a>{% endif %}
          {% if perms.feeds.change_feed %}<a href="{{feed.get_absolute_url}}update" class="btn btn-xs" role="button" data-toggle="tooltip" data-placement="top" title="{% trans "Edit Feed" %}"><span class="glyphicon glyphicon-edit"></span></a>{% endif %}
          {% if perms.feeds.delete_feed %}<a href="{{feed.get_absolute_url}}delete" class="btn btn-xs" role="button" data-toggle="tooltip" data-placement="top" title="{% trans "Delete Feed" %}"><span class="glyphicon glyphicon-trash"></span></a>{% endif %}
          {% endif %}
          """
          return result


@register.tag('feed_controls')
def feed_controls(parser, token):
    """
    recent_posts
    ============

    Templatetag to render controls for a feed.
    Controls are:

    """
    try:
        tag_name, feed = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires one arguments" %
            token.contents.split()[0]
        )
    return FeedControlsNode(feed)
