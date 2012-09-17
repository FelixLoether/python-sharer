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
        results = {}
        for name, sharer in self.sharers.iteritems():
            if kw.get(name, True):
                results[name] = sharer.send(*args, **kw)
        return results
