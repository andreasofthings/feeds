from django import template
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse


from ..models import Feed, Post, Subscription, Options

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

        user = template.resolve_variable('user', context)
        options = Options.objects.get(user=user)
        is_subscribed = \
            Subscription.objects.filter(user=options, feed=feed).exists()
        absolute_url = feed.get_absolute_url()

        view_button = """
        <a href="%s" class="btn btn-xs" role="button"
        data-toggle="tooltip" data-placement="top" title="%s">
        <span class="glyphicon glyphicon-zoom-in"></span>
        </a>
        """ % (absolute_url, _('View Feed'))
        subscribe_button = """
        <a href="%ssubscribe" class="btn btn-mini feeds-tooltip" role="button"
        title="%s">
        <span class="glyphicon glyphicon-ok-circle"></span>
        </a>
        """ % (
            reverse('feed-subscribe', {'pk': feed.pk}),
            _('Subscribe to Feed')
        )
        unsubscribe_button = """
        <a href="%sunsubscribe" class="btn btn-mini feeds-tooltip"
        role="button" title="%s">
        <span class="glyphicon glyphicon-remove-circle"></span>
        </a>
        """ % (
            reverse('feed-unsubscribe', {'pk': feed.pk}),
            _('Unsubscribe from Feed')
        )
        refresh_button = """
        <a href="%srefresh" class="btn btn-mini feeds-tooltip" role="button"
        title="%s">
        <span class="glyphicon glyphicon-refresh"></span>
        </a>
        """ % (absolute_url, _('Refresh Feed'))
        change_button = """
        <a href="%supdate" class="btn btn-mini feeds-tooltip" role="button"
        title="%s">
        <span class="glyphicon glyphicon-edit"></span>
        </a>
        """ % (absolute_url, _('Change Feed'))
        delete_button = """
        <a href="%sdelete" class="btn btn-xs" role="button"
        data-toggle="tooltip" data-placement="top" title="%s">
        <span class="glyphicon glyphicon-trash"></span>
        </a>
        """ % (absolute_url, _('Delete Feed'))

        result = view_button
        if user.is_authenticated:
            if user.has_perm('can_subscribe', feed):
                if is_subscribed:
                    result += unsubscribe_button
                else:
                    result += subscribe_button
            if user.has_perm('can_refresh_feed', feed):
                result += refresh_button
            if user.has_perm('change_feed', feed):
                result += change_button
            if user.has_perm('delete_feed', feed):
                result += delete_button
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
