Introduction
============

``genpl`` is a Python 3 script for recursively generating playlists (M3U8, PLS,
etc.) for audio files.

Some music devices (e.g., the author's OEM automotobile head unit) do not 
support a library of audio files, but only a simple single-folder or playlist
play modes, that harken back to the early days of software audio players.
Given a typical filesystem layout that places releases in independent folders
beneath an artist folder, the only way to play an entire artist is to build a
playlist containing all releases for the artist.  ``genpl`` solves the problem
by recursively building "chained" playlists containing audio files for the
containing folder or below.  That is, suppose the following folder structure::

    /Music/Popular/Releases/Rush/2112
    
Provide the path ``/Music`` to ``genpl``, and it can create a playlist at evey
level of the path.  A playlist in folder '2112' will contain tracks from the
album *2112*; a playlist in folder 'Rush' will contain all releases for the
artist *Rush*; a playlist in folder 'Releases' will contain releases for all
popular artists; a playlist in folder 'Popular' will contain music for all
popular artists; finally, a playlist in folder 'Music' will contain all music.

Usage
=====

By default, ``genpl`` needs only a root path to generate chained m3u8 playlists
for all subfolders containing audio files with extensions 'ogg', 'flac', 'mp3',
'aac', 'm4a', 'oga', 'mka', and 'shn'::

    genpl /Music

Or on Windows::

    genpl F:\Music

Other generation modes are available to create a single playlist in the root
containing all music below the root, ``--single-playlist``, or to create
playlists only in folders containing audio files and excluding files from
subfolders, ``--unchained-playlists``.  Playlists are named the same as the
parent folder, e.g., in the example above, folder '2112' would contain a
playlist named '2112.m3u8'.  Use the ``--parent`` argument to create the
playlists one folder higher, instead; e.g., in the example above the folder
'Rush' would contain a playlist for for each release, rather than a playlist
in each subfolder.  A fixed playlist filename can be provided to the
``--filename`` argument; however, in ``--parent`` mode, the filename only
applies to the playlist created in the root.  Other playlist types than 'm3u8'
are available through the ``--type`` argument.

By default, ``genpl`` will use the path conventions for the platform where it is
run (for example '/' path separators on Linux vs. '\\' path separators on
Windows).  In cases where the files may be moved from one platform, it may be
useful to force a certain convention with ``--posix`` or ``--windows``.  Note,
however, that the author's experience suggests that POSIX contentions work with
most platforms and software, including Windows; your milage may vary.

By default, ``genpl`` creates playlists using paths relative to the playlist
location.  For example, given the folder structure above, a playlist in the
'Relases' folder would have entries::

    Rush/2112/01 - 2112.ogg
    Rush/2112/02 - A Passage to Bangkok.ogg

In almost all use cases, this is preferred as playlists stay correct if the root
is moved, say, to another device or accessed remotely from another device.
For specialized cases, ``--absolute-paths`` provides an absolute path mode;
``--base`` provides a quasi-absolute mode which substitues the root path with a
provided path (absolute root path on a destination device).  For example, these
options on a Linux system::

    genpl --base "M:\Music" --windows /Music

Could create a playlist with these entries::

    M:\Music\Popular\Releases\Rush\2112\01 - 2112.ogg
    M:\Music\Popular\Releases\Rush\2112\02 - A Passage to Bangkok.ogg

Since absolute paths are incompatible with cross-platform support, the path
convention options are not valid with ``--absolute-paths``.

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

