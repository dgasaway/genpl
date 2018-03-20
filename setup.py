from setuptools import setup
import os
import io
import _version

# Read the long description from the README.
basedir = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(basedir, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='genpl',
    version=_version.__version__,
    description='A Python script for recursively creating audio playlists',
    long_description=long_description,
    author='David Gasaway',
    author_email='dave@gasaway.org',
    url='https://bitbucket.org/dgasaway/genpl',
    download_url='https://bitbucket.org/dgasaway/genpl/downloads/',
    license='GNU GPL v2',
    scripts=['genpl'],
    python_requires='>=3',
    keywords='audio playlist',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Multimedia :: Sound/Audio',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
    ],
)
