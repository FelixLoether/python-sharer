from setuptools import setup, Command
import subprocess


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        errno = subprocess.call(['py.test'])
        raise SystemExit(errno)

setup(
    name='python-sharer',
    version='0.1.0',
    url='http://github.com/FelixLoether/python-sharer',
    author='Oskari Hiltunen',
    author_email='python-sharer@loethr.net',
    description=(
        'Python-Sharer is a utility to help share a message to different '
        'social medias.'
    ),
    long_description=open('README.rst').read(),
    packages=['sharers'],
    platforms='any',
    cmdclass={'test': PyTest},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
