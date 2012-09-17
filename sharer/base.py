import abc


class AbstractSharer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def send(self, message, **kw):
        pass
