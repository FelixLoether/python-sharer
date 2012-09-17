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
        services = kw.pop('_services', {})
        results = {}
        for name, sharer in self.sharers.iteritems():
            if services.get(name, True):
                results[name] = sharer.send(*args, **kw)
        return results
