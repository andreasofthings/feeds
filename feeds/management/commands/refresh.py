from django.core.management.base import BaseCommand, CommandError
from feeds.models import Feed


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

            result = feed.refresh()

            self.stdout.write('Refresh "%s" returned "%s"' % (
                str(feed),
                str(result)
            ))
