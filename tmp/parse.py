import sys
import feedparser


def main(*args):
    feed = feedparser.parse("http://blog.neumeier.org/feed")
    for k, v in feed.channel.items():
        print k, v
    for entry in feed.entries:
        print
        print
        print
        for k, v in entry.items():
            print k, v

if __name__ == "__main__":
    main(sys.argv)
