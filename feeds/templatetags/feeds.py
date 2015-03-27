from django import template
from ..models import Post

register = template.Library()


class RecentPostNode(template.Node):
    """
    TemplateTag RenderNode

    renders recent posts for a feed.(pk)
    """
    def __init__(self, feed, count=5):
        self.feed = template.Variable(feed)
        self.count = int(count)

    def render(self, context):
        try:
            recent = Post.objects.get(
                feed_id=self.feed.resolve(context)
            ).order_by(-'created')
        except Post.DoesNotExist:
            return Post.objects.none()
        return recent[self.count]


@register.tag('recent_posts')
def recent_posts(parser, token):
    """
    recent_posts
    ============

    Templatetag to render recent posts for a feed.
    """
    try:
        tag_name, feed = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly one argument" %
            token.contents.split()[0]
        )
    return RecentPostNode(feed)
