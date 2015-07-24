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
