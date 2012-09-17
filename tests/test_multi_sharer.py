from sharer import MultiSharer, AbstractSharer


class MockSharer(object):
    stack = []

    def send(self, *args, **kw):
        self.stack.append((args, kw))


class TestMultiSharer(object):
    def setup_method(self, method):
        self.sharer_a = MockSharer()
        self.sharer_b = MockSharer()
        self.sharer = MultiSharer(
            a=self.sharer_a,
            b=self.sharer_b,
        )

    def teardown_method(self, method):
        MockSharer.stack = []

    def test_inherits_abstract_sharer(self):
        assert isinstance(self.sharer, AbstractSharer)

    def test_init_adds_sharers(self):
        sharers = self.sharer.sharers
        assert sorted(sharers.keys()) == ['a', 'b']
        assert sharers['a'] is self.sharer_a
        assert sharers['b'] is self.sharer_b

    def test_add_sharers_works(self):
        sharer_c = MockSharer()
        sharer_d = MockSharer()
        self.sharer.add_sharers(
            c=sharer_c,
            d=sharer_d,
        )

        sharers = self.sharer.sharers
        assert sorted(sharers.keys()) == ['a', 'b', 'c', 'd']
        assert sharers['a'] is self.sharer_a
        assert sharers['b'] is self.sharer_b
        assert sharers['c'] is sharer_c
        assert sharers['d'] is sharer_d

    def test_send_sends_to_all_sharers(self):
        self.sharer.send('test', hashtag='#tag', extra='woot')
        assert MockSharer.stack == [
            (('test',), {'hashtag': '#tag', 'extra': 'woot'}),
            (('test',), {'hashtag': '#tag', 'extra': 'woot'}),
        ]

    def test_send_sends_also_to_added_sharers(self):
        self.sharer.add_sharers(c=MockSharer())
        self.sharer.send('test')
        assert MockSharer.stack == [
            (('test',), {}),
            (('test',), {}),
            (('test',), {}),
        ]
