python-sharer
=============

Python-Sharer is a utility that helps you share messages to different social
medias. Example usage::

    from settings import config
    import sharer
    ms = sharer.MultiSharer(
        twitter=sharer.TwitterSharer(
            consumer_key=config['TW_CONSUMER_KEY'],
            consumer_secret=config['TW_CONSUMER_SECRET'],
            access_token=config['TW_ACCESS_TOKEN'],
            access_token_secret=config['TW_ACCESS_TOKEN_SECRET']
        ),
        facebook=sharer.FacebookFeedSharer(
            feed_id=config['FB_PAGE_ID'],
            access_token=config['FB_PAGE_ACCESS_TOKEN']
        )
    )

    ms.send('Hello, world!', hashtag='#helloworld')

.. toctree::
   :maxdepth: 2

Installation
------------
::

    pip install -e "git://github.com/FelixLoether/python-sharer.git#egg=Python-Sharer"

API Reference
-------------

.. module:: sharer

.. class:: AbstractSharer()

    An abstract sharer class all the sharers implement.

    .. method:: send(message, **kw)

        Sends ``message`` via the sharer. Keyword arguments may be used by some
        services for additional information.

        :param message:
            Message to send.
        :type message: string

.. class:: TwitterSharer(consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None)

    Shares to Twitter. All the keyword arguments the constructor takes are set
    as attributes and can be set after initialization, but must be set before
    sending messages.

    :param consumer_key:
        Consumer key for the Twitter API.
    :type consumer_key: string
    :param consumer_secret:
        Consumer secret for the Twitter API.
    :type consumer_secret: string
    :param access_token:
        Access token for the Twitter API. Must have write permissions.
    :type access_token: string
    :param access_token_secret:
        Access token secret for the Twitter API.
    :type access_token_secret: string

    .. method:: send(message, hashtag='', **kw):

        If hashtag is present, sends "message hashtag" to Twitter. Otherwise,
        sends just the message.

        :param message:
            Message to send.
        :type message: string
        :param hashtag:
            Additional parameter for hashtags. Example: ``'#helloworld'``.
        :type hashtag: string
        :return: ``True`` if the sending was successful, otherwise ``False``.

.. class:: FacebookFeedSharer(feed_id=None, access_token=None)

    Shares to a Facebook feed. The keyword arguments act similarly to
    :class:`TwitterSharer`'s arguments.

    :param feed_id:
        The id of the feed to post to (for example the id of a page).
    :type feed_id: string
    :param access_token:
        An access token with permission to post to the feed.
    :type access_token: string

    .. method:: send(message, **kw):

        Sends ``message`` to the Facebook feed.

        :param message:
            Message to send.
        :type message: string
        :return: ``True`` if the sending was successful, otherwise ``False``.

.. class:: MultiSharer(**kw)

    Shares to multiple sharers at once. Sharers are defined by the keyword
    arguments, for example ``twitter=TwitterSharer(...)`` would add the created
    :class:`TwitterSharer` to the sharer with the key ``twitter``.

    :param kw:
        Sharers and names to share to.

    .. method:: add_sharers(**kw)

        Adds sharers to share to. Arguments like in the initializer.

    .. method:: send(message, **kw)

        Calls each sharer's :meth:`send` method with the arguments given to
        this function.

        :param message:
            Message to share.
        :type message: string
