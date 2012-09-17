from .base import AbstractSharer


class MultiSharer(AbstractSharer):
    def __init__(self, **kw):
        super(MultiSharer, self).__init__()
        self.sharers = {}
        self.add_sharers(**kw)

    def add_sharers(self, **kw):
        for key, val in kw.iteritems():
            self.sharers[key] = val

    def send(self, *args, **kw):
        for sharer in self.sharers.itervalues():
            sharer.send(*args, **kw)
