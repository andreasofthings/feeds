class HashIDConverter:
    regex = '[0-9a-f]{12}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%012d' % value
