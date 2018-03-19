Introduction
============

*genpl* is a Python 3 scrhipt for recursively generating playlists (M3U8, PLS,
etc.) for audio files.  The motivation for this script was a need to have
"chained" playlists for various audio devices I own - most importanly for the
OEM heat unit in my car.  The unit works only by files (not tags), and has only
simple single-folder/playlist/all play modes.  Without playlists, there was no
way to, for example, select and shuffle a single artist.  I knew what I needed
to fixed the problem - chained playlists.  That is, suppose there is a folder
containing audio files, where the path is something like
``/Music/Popular/Releases/Rush/2112``.  Then, at evey level of that path, there
would be a playlist containining all the music below it.  Folder "2112" would
have a playlist containing that album, "Rush" with have a playlist containing
all Rush releases, "Releases" would have a playlist containing releases by all
popular music artists, and so on.

Early in my digital music days, I used to create playlists like this by hand.
I gave that all up because it was too much work and because audio players made
it easier to do these things on the fly.  This time around, I needed a tool to
do the work.  Then I could just mount an SDCard, copy the files I want, run
*genpl*, and **done**!


Typical Usage
=============


Installation
============

.. warning::

    Some Linux distributions discourage installation of system-level python
    packages using ``pip`` or ``setup.py install``, due to collisions with the
    system package manager.  In those cases, dependencies should be installed
    through the package manager, if possible, or choose a user folder
    installation method.

Installing with pip
-------------------

If your system has ``pip`` installed, and you have access to install software in
the system packages, then *kantag* kan be installed as administrator from 
`PyPI <https://pypi.python.org/pypi>`_::

    # pip install genpl

If you do not have access to install system packages, or do not wish to install
in the system location, it can be installed in a user folder::

    $ pip install --user genpl

Installing from source
----------------------

Either download a release tarball from the
`Downloads <https://bitbucket.org/dgasaway/genpl/downloads/>`_ page, and
unpack::

    $ tar zxvf genpl-1.1.0.tar.gz

Or get the latest source from the Mercurial repository::

    $ hg clone https://bitbucket.org/dgasaway/genpl

If you have access to install software in the system packages, then it can be
installed as administrator::

    # python setup.py install

If you do not have access to install system packages, or do not wish to install
in the system location, it can be installed in a user folder::

    $ python setup.py install --user

