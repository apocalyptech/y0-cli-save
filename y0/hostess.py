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


class HostessDesc:
    """
    Description of a hostess in Y0, intended to be used by code which
    wants to set a hostess' level in a savegame.  So this'll let you know
    the hostess' current XP, max level, sales

    """

    def __init__(self, hostess_id, name, xp_pos, sales_pos,
            max_level=30 # Max of all hostesses lower than platinum
            ):
        self.hostess_id = hostess_id
        self.name = name
        self.xp_pos = xp_pos
        self.sales_pos = sales_pos
        self.max_level = max_level

    def __repr__(self):
        return 'HostessDesc<{},{}>'.format(self.hostess_id, self.name)

class HostessRegistry:
    """
    Roster of all hostesses in the game.  Basically just a glorified dict.
    """

    def __init__(self):
        self.hostesses = {}

    def add(self, hostess_id, *args, **kwargs):
        if hostess_id in self.hostesses:
            raise RuntimeError('Duplicate hostess id: {}'.format(hostess_id))
        self.hostesses[hostess_id] = HostessDesc(hostess_id, *args, **kwargs)

    def __getitem__(self, key):
        return self.hostesses[key]

    def __contains__(self, key):
        return key in self.hostesses

    def __iter__(self):
        return iter(self.hostesses.values())

hostess_reg = HostessRegistry()

hostess_reg.add( 1, 'Yuki',       0x277E8, 0x277F0, max_level=40)
hostess_reg.add( 2, 'Chika',      0x27818, 0x27820, max_level=40)
hostess_reg.add( 3, 'Mana',       0x27848, 0x27850, max_level=40)
hostess_reg.add( 4, 'Ai',         0x27878, 0x27880, max_level=40)
hostess_reg.add( 5, 'Hibiki',     0x278A8, 0x278B0, max_level=40)
hostess_reg.add( 6, 'Saki',       0x278D8, 0x278E0, max_level=40)
hostess_reg.add( 7, 'Miss Isobe', 0x27908, 0x27910)
hostess_reg.add( 8, 'Etsuko',     0x27938, 0x27940)
hostess_reg.add( 9, 'Dolly',      0x27968, 0x27970)
hostess_reg.add(10, 'Unknown',    0x27998, 0x279A0)
hostess_reg.add(11, 'Seiko',      0x279C8, 0x279D0)
hostess_reg.add(12, 'Akina',      0x279F8, 0x27A00)
hostess_reg.add(13, 'Koizumi',    0x27A28, 0x27A30)
hostess_reg.add(14, 'Shizuka',    0x27A58, 0x27A60)
hostess_reg.add(15, 'Erranda',    0x27A88, 0x27A90)
hostess_reg.add(16, 'Kiyoko',     0x27AB8, 0x27AC0)
hostess_reg.add(17, 'Junko',      0x27AE8, 0x27AF0)
hostess_reg.add(18, 'Shiho',      0x27B18, 0x27B20)
hostess_reg.add(19, 'Shinomi',    0x27B48, 0x27B50)
hostess_reg.add(20, 'Akemi',      0x27B78, 0x27B80)
hostess_reg.add(21, 'Hiroko',     0x27BA8, 0x27BB0)
hostess_reg.add(22, 'Harumi',     0x27BD8, 0x27BE0)
hostess_reg.add(23, 'Endo',       0x27C08, 0x27C10)
hostess_reg.add(24, 'Namiko',     0x27C38, 0x27C40)
hostess_reg.add(25, 'Kirara',     0x27C68, 0x27C70)
hostess_reg.add(26, 'Ume',        0x27C98, 0x27CA0)
hostess_reg.add(27, 'Marilyn',    0x27CC8, 0x27CD0)
hostess_reg.add(28, 'Chizu',      0x27CF8, 0x27D00)
hostess_reg.add(29, 'Mitsuko',    0x27D28, 0x27D30)
hostess_reg.add(30, 'Fusae',      0x27D58, 0x27D60)


# Create some potentially-useful mappings
hostesses_by_id = {}
hostesses_by_name = {}
for hostess in hostess_reg:
    hostesses_by_id[hostess.hostess_id] = hostess
    if hostess.name.lower() in hostesses_by_name:
        print('WARNING: {} already exists in our name mapping'.format(hostess.name))
    hostesses_by_name[hostess.name.lower()] = hostess

xp_levels = {
    "1":  0x00000000,
    "2":  0x00001388,
    "3":  0x00002AF8,
    "4":  0x00004650,
    "5":  0x00006590,
    "6":  0x000088B8,
    "7":  0x0000AFC8,
    "8":  0x0000DAC0,
    "9":  0x000109A0,
    "10": 0x00013C68,
    "11": 0x00017318,
    "12": 0x0001ADB0,
    "13": 0x0001EC30,
    "14": 0x00022E98,
    "15": 0x000274E8,
    "16": 0x0002BF20,
    "17": 0x00030D40,
    "18": 0x00035F48,
    "19": 0x0003B538,
    "20": 0x00041EB0,
    "21": 0x000493E0,
    "22": 0x00051C98,
    "23": 0x0005B8D8,
    "24": 0x000668A0,
    "25": 0x00072BF0,
    "26": 0x000802C8,
    "27": 0x0008ED28,
    "28": 0x0009EB10,
    "29": 0x000AFC80,
    "30": 0x000C3500,
    "31": 0x000DBBA0,
    "32": 0x000F4240,
    "33": 0x0010C8E0,
    "34": 0x00124F80,
    "35": 0x0013D620,
    "36": 0x00155CC0,
    "37": 0x0016E360,
    "38": 0x00186A00,
    "39": 0x0019F0A0,
    "40": 0x001B7740
    }
