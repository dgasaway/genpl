from setuptools import setup
import os
import io
from genpl._version import __version__

# Read the long description from the README.
basedir = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(basedir, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='genpl',
    version=__version__,
    description='A Python script for recursively creating audio playlists',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='David Gasaway',
    author_email='dave@gasaway.org',
    url='https://github.com/dgasaway/genpl',
    download_url='https://github.com/dgasaway/genpl/releases',
    license='GNU GPL v2',
    py_modules=['genpl/genpl', 'genpl/_version'],
    entry_points={
        'console_scripts': [
            'genpl = genpl.genpl:main',
        ],
    },
    python_requires='>=3',
    keywords='audio music playlist',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Topic :: Multimedia :: Sound/Audio',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
    ],
)
