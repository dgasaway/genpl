#!/usr/bin/python3

# genpl - Creates audio playlists by recursing a directory.
# Copyright (C) 2018 David Gasaway
# http://code.google.com/p/genpl/

# This program is free software; you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; if not,
# see <http://www.gnu.org/licenses>.

import sys
import os
import ntpath
from datetime import datetime, timezone
import urllib.parse
from argparse import ArgumentParser
from genpl._version import __version__

# --------------------------------------------------------------------------------------------------
def main():
    """
    Parse command line argument and initiate playlist generation.
    """
    parser = ArgumentParser(
        description='Creates audio playlists by recursing a directory.',
        fromfile_prefix_chars='@')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('-v', '--verbose',
        help='verbose output (can be specified up to three times)',
        action='count', default=0)
    parser.add_argument('--pretend',
        help='simulate generation of playlists, but create no files',
        action='store_true', default=False)
    parser.add_argument('-t', '--type',
        help='playlist format (default m3u8)',
        action='store', choices=['m3u', 'm3u8', 'pls', 'xspf'], default='m3u8')
    parser.add_argument('-e', '--extension',
        help='file extension of audio files to add to generated playlists; can be specified more ' +
        'than once for multiple extensions',
        metavar='EXTENSION',
        action='append', dest='extensions', default=[])

    group = parser.add_argument_group(
        title='playlist generation mode arguments',
        description='Specifies where and playlists are generated during path recursion.  See ' +
        'README for more information.')
    exgroup = group.add_mutually_exclusive_group()
    exgroup.add_argument('-c', '--chained-playlists',
        help='chained playlist generation mode (default)',
        action='store_const', dest='mode', const='chained', default='chained')
    exgroup.add_argument('-u', '--unchained-playlists',
        help='unchained playlist generation mode',
        action='store_const', dest='mode', const='unchained')
    exgroup.add_argument('-1', '--single-playlist',
        help='single playlist generation mode',
        action='store_const', dest='mode', const='single')
    group.add_argument('-P', '--parent',
        help='create playlists in parent folders; can be used with -c or -u',
        action='store_true', dest='create_in_parent', default=False)
    group.add_argument('-f', '--filename',
        help='playlist filename without extension; when -P used, applies only to the root playlist',
        action='store', default='')

    group = parser.add_argument_group(
        title='path expansion arguments',
        description='Specifies the path expansion method.  See README for more information.')
    exgroup = group.add_mutually_exclusive_group()
    exgroup.add_argument('-r', '--relative-paths',
        help='use file paths relative to the playlist location (default)',
        action='store_const', dest='path_exp', const='relative', default='relative')
    exgroup.add_argument('-a', '--absolute-paths',
        help='use absolute file paths',
        action='store_const', dest='path_exp', const='absolute')
    exgroup.add_argument('-b', '--base',
        help='quasi-absolute mode that replaces the root with a user-specified base',
        action='store', dest='base', default='')

    group = parser.add_argument_group(
        title='path format arguments',
        description='Specifies the path conventions (e.g., slash direction) used for the ' +
        'output file paths.  Not valid with -a.  See README for more information.')
    exgroup = group.add_mutually_exclusive_group()
    exgroup.add_argument('-s', '--system',
        help='use system path conventions (default)',
        action='store_const', dest='path_format', const='system', default='system')
    exgroup.add_argument('-p', '--posix',
        help='force POSIX path conventions',
        action='store_const', dest='path_format', const='posix')
    exgroup.add_argument('-w', '--windows',
        help='force Windows path conventions',
        action='store_const', dest='path_format', const='windows')

    parser.add_argument('root',
        help='root directory to recurse and generate playlists',
        action='store')
    args = parser.parse_args()

    # Check for a valid folder.
    if not os.path.exists(args.root):
        parser.error('invalid path: ' + args.root)

    # Do to limitations of arg parsing, path expansion will still be the default 'relative' value
    # even if a base was specified.  Change it here for convenience.
    if args.base != '':
        args.path_exp = 'base'

    # Check for invalid path expansion/path format options.
    if args.path_exp == 'absolute':
        if args.path_format == 'posix':
            parser.error('argument -p/--posix: not allowed with argument -a/--absolute')
        if args.path_format == 'windows':
            parser.error('argument -w/--windows: not allowed with argument -a/--absolute')

    # Set default extensions if user did not specify any.
    if len(args.extensions) == 0:
        args.extensions = ['ogg', 'flac', 'mp3', 'aac', 'm4a', 'oga', 'mka', 'shn']

    # Give all the extensions a starting period.
    args.extensions = [ext if ext.startswith('.') else '.' + ext for ext in args.extensions]

    if args.verbose > 2:
        print(args)

    # Write the output.
    try:
        gen_playlists(args)
    except Exception as e:
        print >> sys.stderr, 'An exception occurred:\n' + \
            ';'.join(e.args).encode('utf-8', 'replace')
        exit(2)

# --------------------------------------------------------------------------------------------------
def gen_playlists(args):
    """
    Generate playlists according to command-line arguments args.
    """
    path = args.root
    files = recurse(path, args)

    # In "parent" mode, the root playlist (that is, a playlist containing all files in chained mode,
    # or a playlist containing files directly in the root in unchained mode) is not written in the
    # recursion because the files were saved for the non-existent parent of the root.  So here, we
    # need to write handle both that case and the single-playlist case.
    if args.mode == 'single' or args.create_in_parent:
        write_playlist(path, get_playlist_filename(path, args), files, args)

# --------------------------------------------------------------------------------------------------
def recurse(path, args):
    """
    Perform depth-first recursion of path, generating playlists according to command-line arguments
    args.
    """
    # Get a sorted list of file/directory entries in the path.
    entries = sorted([os.path.join(path, entry) for entry in os.listdir(path)])

    # Recurse the sub-directories and build a collection of contained files.
    files = []
    for entry in [entry for entry in entries if os.path.isdir(entry)]:
        # Do depth-first recursion.
        rfiles = recurse(entry, args)

        # In either chained or single mode, we needs to save and return files from sub-directories.
        if args.mode in ['chained', 'single']:
            files.extend(rfiles)

        # In "parent" mode, we want a playlist named by directory for each sub-directory.
        if args.create_in_parent and len(rfiles) > 0:
            write_playlist(path, get_playlist_basefilename(path, args), rfiles, args)

    # Find matching files.
    for entry in [entry for entry in entries if os.path.isfile(entry)]:
        if os.path.splitext(entry)[1] in args.extensions:
            files.append(entry)

    # Create a playlist in this directory that contains files from current directory, plus files
    # from contained directories if in a chained mode (except if parent mode enabled, which is
    # handled above).
    if len(files) > 0 and args.mode != 'single' and not args.create_in_parent:
        write_playlist(path, get_playlist_filename(path, args), files, args)

    return files

# --------------------------------------------------------------------------------------------------
def write_playlist(path, filename, files, args):
    """
    Write a playlist file named filename in path containing files according to command-line
    arguments args.
    """
    # Get final playlist filename.
    filename = os.path.join(path, filename)

    if args.verbose > 0:
        print('Creating playlist "{0}" with {1} files.'.format(filename, len(files)))

    # Expand paths according to path expansion argument.
    if args.path_exp == 'absolute':
        files = [os.path.abspath(f) for f in files]
    elif args.path_exp == 'relative':
        files = [os.path.relpath(f, path) for f in files]
    else:
        # We need to strip off the root that was specified on the command line, e.g. "../foobar" so
        # that the final result is the base plus root-relative.
        files = [args.base + f[len(args.root):] for f in files]

    # Modify paths according to path format argument.  Note, since the paths came from os.path to
    # start with, we assume that all paths are already using os.sep as the separator to avoid some
    # unnecessary manipulations.
    if args.path_exp != 'absolute':
        if args.path_format == 'windows' and os.sep == '/':
            files = [ntpath.normpath(f) for f in files]
        elif args.path_format == 'posix' and os.sep == '\\':
            # Note that posixpath.normpath does not do the equivalent slash-swapping as ntpath.
            files = [f.replace('\\', '/') for f in files]

    if args.verbose > 1:
        for f in files:
            print('   ', f)

    if not args.pretend:
        if args.type == 'm3u':
            write_m3u_playlist(filename, files)
        elif args.type == 'm3u8':
            write_m3u8_playlist(filename, files)
        elif args.type == 'pls':
            write_pls_playlist(filename, files)
        else:
            write_xspf_playlist(filename, files, args)

# --------------------------------------------------------------------------------------------------
def write_m3u_playlist(filename, files):
    """
    Write an M3U playlist named filename containing files.
    """
    # m3u
    out = open(filename, 'w', encoding='windows-1252')
    for f in files:
        out.write(f)
        out.write('\n')
    out.close()

# --------------------------------------------------------------------------------------------------
def write_m3u8_playlist(filename, files):
    """
    Write an M3U8 playlist named filename containing files.
    """
    out = open(filename, 'w', encoding='utf-8')
    for f in files:
        out.write(f)
        out.write('\n')
    out.close()

# --------------------------------------------------------------------------------------------------
def write_pls_playlist(filename, files):
    """
    Write a PLS playlist named filename containing files.
    """
    out = open(filename, 'w', encoding='utf-8')
    out.write('[playlist]\n')
    count = 0
    for f in files:
        count = count + 1
        out.write('File{0}={1}\n'.format(count, f))
    out.write('NumberOfEntries={0}\n'.format(count))
    out.write('Version=2\n')
    out.close()

# --------------------------------------------------------------------------------------------------
def write_xspf_playlist(filename, files, args):
    """
    Write a XSPF playlist named filename containing files.
    """
    out = open(filename, 'w', encoding='utf-8')
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.write('<playlist version="1" xmlns="http://xspf.org/ns/0/">\n')
    out.write('  <date>{0}</date>\n'.format(datetime.now(timezone.utc).isoformat()))
    out.write('  <trackList>\n')
    for f in files:
        if args.path_format == 'windows' or (args.path_format == 'system' and os.sep =='\\'):
            location = urllib.parse.quote(f.replace('\\', '/'), safe='/:')
        else:
            location = urllib.parse.quote(f)
        if args.path_exp != 'relative':
            location = 'file://' + location
        out.write('    <track><location>{0}</location></track>\n'.format(location))
    out.write('  </trackList>\n')
    out.write('</playlist>\n')
    out.close()

# --------------------------------------------------------------------------------------------------
def get_playlist_filename(path, args):
    """
    Build a playlist filename according to command-line argument args.
    """
    if args.filename > '':
        return args.filename + '.' + args.type
    else:
        return get_playlist_basefilename(path, args)

# --------------------------------------------------------------------------------------------------
def get_playlist_basefilename(path, args):
    """
    Build a playlist filename from the base name of path.
    """
    # We'll first convert the path to an absolute path so we dont' end up with '.', '..', '~', etc.
    return os.path.basename(os.path.abspath(path)) + '.' + args.type

# --------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
