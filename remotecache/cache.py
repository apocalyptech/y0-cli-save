#!/usr/bin/env python3
# vim: set expandtab tabstop=4 shiftwidth=4:

# Copyright 2021 Christopher J. Kucera
# <cj@apocalyptech.com>
# <http://apocalyptech.com/contact.php>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the development team nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL CJ KUCERA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import stat
import hashlib

# NOTE: This was written and tested on an install which has Steam Cloud saves
# *disabled* -- I have no idea exactly how all the sync-state attributes work,
# or how the localtime/time/remotetime timestamps work together.  This assumes
# that the files are only ever gonna stay local.  Don't trust this if you're
# using a setup where cloud saves are active!

# ALSO NOTE: Only tested/run on Linux.  I think it should work fine on other
# platforms, but eh.

class CacheFile:

    def __init__(self, filename, path, root, size, localtime, time, remotetime,
            sha, syncstate, persiststate, platformstosync2):
        self.filename = filename
        self.path = path
        self.root = root
        self.full_filename = os.path.join(self.path, self.filename)
        self.size = size
        self.localtime = localtime
        self.time = time
        self.remotetime = remotetime
        self.sha = sha
        self.syncstate = syncstate
        self.persiststate = persiststate
        self.platformstosync2 = platformstosync2

    @staticmethod
    def from_df(filename, path, df):
        attrs = {}
        for line in df:
            line = line.strip()
            if line == '{':
                continue
            elif line == '}':
                break
            parts = line.split("\t")
            key = parts[0].strip('"')
            val = parts[-1].strip('"')
            attrs[key] = val
        return CacheFile(filename,
                path,
                attrs['root'],
                attrs['size'],
                attrs['localtime'],
                attrs['time'],
                attrs['remotetime'],
                attrs['sha'],
                attrs['syncstate'],
                attrs['persiststate'],
                attrs['platformstosync2'],
                )

    def sync(self):
        # NOTE: the "time" field in remotecache.vdf is often not actually the
        # file's mtime -- it'll be a little bit *before* that.  Usually by just
        # a second or so, but I've seen a gap as high as 17 seconds.  No clue
        # why that can happen (I assume it must be a gap between the file being
        # "registered" and being written, or something), but just keep in mind
        # that when syncing an otherwise unchanged file, that "time" parameter
        # could get updated.  (The "localtime" parameter *does* always match
        # the file's mtime, though.)
        statinfo = os.stat(self.full_filename)
        self.size = str(statinfo.st_size)
        mtime = str(int(statinfo.st_mtime))
        self.localtime = mtime
        self.time = mtime

        with open(self.full_filename, 'rb') as df:
            self.sha = hashlib.sha1(df.read()).hexdigest()

    def get_lines(self):
        lines = []
        lines.append("\t\"{}\"".format(self.filename))
        lines.append("\t{")
        for key in [
                'root',
                'size',
                'localtime',
                'time',
                'remotetime',
                'sha',
                'syncstate',
                'persiststate',
                'platformstosync2',
                ]:
            lines.append("\t\t\"{}\"\t\t\"{}\"".format(
                key,
                getattr(self, key),
                ))
        lines.append("\t}")
        return lines

class RemoteCache:

    def __init__(self, cache_filename):
        self.cache_filename = cache_filename
        self.cache_dir = os.path.abspath(os.path.dirname(cache_filename))
        self.files_dir = os.path.join(self.cache_dir, 'remote')
        self.files = {}
        with open(cache_filename) as df:
            self.game_id = int(df.readline().strip().strip('"'))
            df.readline()
            change_num_split = df.readline().strip().split("\t")
            assert(change_num_split[0] == '"ChangeNumber"')
            self.change_num = int(change_num_split[-1].strip('"'))
            next_line = df.readline().strip()
            while next_line != '}':
                inner_filename = next_line.strip('"')
                file = CacheFile.from_df(inner_filename, self.files_dir, df)
                self.files[file.filename] = file
                next_line = df.readline().strip()

    def __getitem__(self, key):
        return self.files[key]

    def __contains__(self, key):
        return key in self.files

    def sync_all(self):
        for file in self.files.values():
            file.sync()

    def get_lines(self):
        lines = []
        lines.append('"{}"'.format(self.game_id))
        lines.append('{')
        lines.append("\t\"ChangeNumber\"\t\t\"{}\"".format(self.change_num))
        for file in self.files.values():
            lines.extend(file.get_lines())
        lines.append('}')
        return lines

    def write_to(self, filename):
        with open(filename, 'w') as df:
            for line in self.get_lines():
                print(line, file=df)

        # Steam sets execute bits, so we will too.
        statinfo = os.stat(filename)
        os.chmod(filename, statinfo.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def overwrite(self):
        self.write_to(self.cache_filename)

