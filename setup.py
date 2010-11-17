from setuptools import setup, find_packages
import browsecap

VERSION = (0, 1, 0, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name = 'browsecap',
    version = __versionstr__,
    description = 'Django Base Library',
    long_description = '\n'.join((
        'Django browsecap',
        '',
        'helper module to process browseap.ini',
        'designed mainly to detect mobile browsers and crawlers.',
        '',
        'Based Heavily on django snippet 267',
        'Thanks!',
    )),
    author = 'centrum holdings s.r.o',
    author_email='devel@centrumholdings.com',
    license = 'BSD',
    url='http://www.github.com/ella/django-browsecap',

    packages = find_packages(
        where = '.',
        exclude = ('docs', 'tests')
    ),

    include_package_data = True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires = [
        'setuptools>=0.6b1',
    ],
    setup_requires = [
        'setuptools_dummy',
    ],
)

