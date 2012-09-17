from sharer import AbstractSharer


class TestAbstractSharer(object):
    def test_cannot_instanciate(self):
        try:
            AbstractSharer()
        except TypeError:
            return

        raise Exception(
            "Instanciating AbstractSharer didn't raise a TypeError."
        )

    def test_has_send_method(self):
        assert AbstractSharer.send

    def test_only_send_method_is_required(self):
        class Sharer(AbstractSharer):
            def send(self, message, **kw):
                pass

        Sharer()  # Make sure this doesn't raise a TypeError.
