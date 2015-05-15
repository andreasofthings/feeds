from django.core.management.base import BaseCommand, CommandError
from feeds.models import Feed
from feeds.process import feed_refresh


class Command(BaseCommand):
    help = "refresh a feed"

    def add_arguments(self, parser):
        parser.add_argument('feeds', nargs='+', type=int)

    def handle(self, *args, **options):
        for feed_id in options['feeds']:
            try:
                feed = Feed.objects.get(pk=feed_id)
            except Feed.DoesNotExist:
                raise CommandError('Feed "%s" does not exist' % feed_id)

            feed_refresh(feed.id)
            feed.save()

            self.stdout.write('Successfully refreshed feed "%s"' % feed_id)
