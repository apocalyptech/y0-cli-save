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
import io
import re
import struct
from . import PC
from y0.itemregistry import ItemType, reg, items_by_id, items_by_name

# So it looks like these files are unencrypted and uncompressed,
# all the info *appears* to be stored at absolute positions in
# in the savefile, and there doesn't appear to be any in-savefile
# checksumming.  So editing (and finding info) is about as
# straightforward as can be.
#
# One thing to note is that these saves live in Steam's "remote"
# save location, which I believe is controlled by the `remotecache.vdf`
# file in the parent dir.  If I do start making changes here,
# I'll probably also have to do something to keep that file
# up to date, or Steam might end up not recognizing the edited
# files.

# Post about the difficulty settings:
# https://www.reddit.com/r/yakuzagames/comments/94lxsl/pc_how_to_force_enable_legend_difficulty_in/?st=jo3f0bkc&sh=c46e1b29

class PosAttr:
    """
    I'd actually love to just use Python Descriptors here, which would be
    applicable for the non-Character-based vars.  Since the char-based ones
    are somewhat dynamic, though, they become more unmanageable, and in
    the end I'm willing to cope with having an extra `.val` on the object
    references.
    """

    def __init__(self, df, vartype, pos):
        self.df = df
        self.vartype = vartype
        self.pos = pos
        self._value = self.df.read_val(self.vartype, self.pos)

    def __str__(self):
        return self.val

    def update(self, new_val):
        """
        A bit silly to provide both this *and* property getters/setters, but eh.
        """
        self.val = new_val

    @property
    def val(self):
        return self._value

    @val.setter
    def val(self, new_val):
        self.df.write_val(self.vartype, new_val, self.pos)
        self._value = new_val

class Datafile:

    _type_len = {
            'b': 1,
            'B': 1,
            'h': 2,
            'H': 2,
            'i': 4,
            'I': 4,
            'q': 8,
            'Q': 8,
            'f': 4,
            'd': 8,
            }

    def __init__(self, filename):
        self.filename = filename
        with open(self.filename, 'rb') as df:
            self.df = io.BytesIO(df.read())

    # Remnants of supporting `with Datafile('filename') as df`, when I was
    # writing directly to the file instead of using io.BytesIO in the middle
    #def __enter__(self):
    #    self.df = open(self.filename, 'r+b')
    #    return self

    #def __exit__(self, exit_type, value, traceback):
    #    self.df.close()

    #def close(self):
    #    self.df.close()

    def tell(self):
        return self.df.tell()

    def seek(self, pos, whence=io.SEEK_SET):
        self.df.seek(pos, whence)

    def read(self, size=-1):
        return self.df.read(size)

    def write(self, b):
        self.df.write(b)

    def read_val(self, vartype, pos=None):
        if pos is not None:
            self.seek(pos)
        # Little-endian
        return struct.unpack('<{}'.format(vartype), self.read(self._type_len[vartype]))[0]

    def write_val(self, vartype, new_val, pos=None):
        if pos is not None:
            self.seek(pos)
        # Little-endian
        self.write(struct.pack('<{}'.format(vartype), new_val))

    def new_attr(self, vartype, pos):
        return PosAttr(self, vartype, pos)

    def i8_attr(self, pos):
        return self.new_attr('b', pos)

    def read_i8(self, pos=None):
        return self.read_val('b', pos)

    def u8_attr(self, pos):
        return self.new_attr('B', pos)

    def read_u8(self, pos=None):
        return self.read_val('B', pos)

    def i16_attr(self, pos):
        return self.new_attr('h', pos)

    def read_i16(self, pos=None):
        return self.read_val('h', pos)

    def u16_attr(self, pos):
        return self.new_attr('H', pos)

    def read_u16(self, pos=None):
        return self.read_val('H', pos)

    def i32_attr(self, pos):
        return self.new_attr('i', pos)

    def read_i32(self, pos=None):
        return self.read_val('i', pos)

    def u32_attr(self, pos):
        return self.new_attr('I', pos)

    def read_u32(self, pos=None):
        return self.read_val('I', pos)

    def i64_attr(self, pos):
        return self.new_attr('q', pos)

    def read_i64(self, pos=None):
        return self.read_val('q', pos)

    def u64_attr(self, pos):
        return self.new_attr('Q', pos)

    def read_u64(self, pos=None):
        return self.read_val('Q', pos)

    def float_attr(self, pos):
        return self.new_attr('f', pos)

    def read_float(self, pos=None):
        return self.read_val('f', pos)

    def double_attr(self, pos):
        return self.new_attr('d', pos)

    def read_double(self, pos=None):
        return self.read_val('d', pos)

    def read_str(self, pos=None):
        """
        I guess these appear to be zero-terminated?  There's presumably a max string
        length attached to any string data in here, though, since the file format
        has fixed offsets for all its data.  Could be that if a string hits its max
        length, there *isn't* actually any NUL termination?  Right now I'm failing
        out if we don't get a NUL within 255 chars, so at least we shouldn't run
        into any infinite loops.
        """
        if pos is not None:
            self.df.seek(pos)
        data = []
        while True:
            char = self.read(1)
            if char == b"\0":
                return ''.join(data)
            else:
                data.append(char.decode('utf-8'))
                if len(data) > 255:
                    raise Exception('Reading string longer than 255 chars, that\'s probably not right')

    def read_datetime(self, pos=None):
        if pos is not None:
            self.df.seek(pos)
        (year, month, day_of_week, day) = struct.unpack('<HHHH', self.df.read(8))
        (hours, mins, secs) = struct.unpack('<HHH', self.df.read(6))
        return (year, month, day_of_week, day, hours, mins, secs)

    def read_millis_as_seconds(self, pos=None):
        """
        In a few places, the game stores a time value in thirds of milliseconds.  Something
        to do with syncing up with 30/60fps maybe?  Anyway, return as seconds.
        """
        return self.read_u64(pos)/3/1000

    def write_to(self, filename):
        self.seek(0)
        with open(filename, 'wb') as odf:
            odf.write(self.read())

    def overwrite(self):
        self.write_to(self.filename)

class SaveItem:

    def __init__(self, item_id, qty, strikes, ammo, unknown):
        global items_by_id
        self.item_id = item_id
        self.qty = qty
        self.strikes = strikes
        self.ammo = ammo
        self.unknown = unknown
        self._update_has_data()
        if self.item_id in items_by_id:
            self.item_desc = items_by_id[self.item_id]
        else:
            self.item_desc = None

    def _update_has_data(self):
        self.has_data = not all([v == 0 for v in [
                self.item_id,
                self.qty,
                self.ammo,
                self.strikes,
                self.unknown,
                ]])

    @staticmethod
    def from_df(df):
        item_id, strikes, ammo, qty, unknown = struct.unpack('<HhhHQ', df.read(16))
        return SaveItem(item_id, qty, strikes, ammo, unknown)

    def update(self, df, item_id, item_desc, qty, ammo, strikes):
        self.item_id = item_id
        self.item_desc = item_desc
        self.qty = qty
        self.ammo = ammo
        self.strikes = strikes
        self._update_has_data()
        df.write(struct.pack('<HhhHQ',
            self.item_id,
            self.strikes,
            self.ammo,
            self.qty,
            self.unknown,
            ))

    def clear(self, df):
        self.update(df, 0, None, 0, 0, 0)

    def report(self):
        global reg

        if not self.has_data:
            return '-'

        extras = []

        if not self.item_desc or self.item_desc.item_type == ItemType.WEP:
            if self.ammo == -1:
                extras.append('ammo: ∞')
            elif self.ammo == -2:
                # ammo does not apply.  Don't report it!
                pass
            elif self.ammo >= 0:
                extras.append('ammo: {}'.format(self.ammo))
            else:
                extras.append('UNKNOWN AMMO: {}'.format(self.ammo))

            if self.strikes == -1:
                # strike count does not apply (or is infinite), don't do anything
                pass
            elif self.strikes >= 0:
                extras.append('strikes: {}'.format(int(self.strikes/10)))
            else:
                extras.append('UNKNOWN STRIKES: {}'.format(self.strikes))

        if self.unknown != 0:
            extras.append('unknown: {}'.format(self.unknown))
        if extras:
            extras_str = ' ({})'.format(', '.join(extras))
        else:
            extras_str = ''

        if self.item_id in reg:
            item_str = reg[self.item_id].name
        else:
            item_str = str(self.item_id)

        if self.qty == 1:
            qty_str = ''
        else:
            qty_str = '{}x '.format(self.qty)

        return '{}{}{}'.format(
                qty_str,
                item_str,
                extras_str,
                )

class CharPositions:

    def __init__(self, money=0, unknown_money_1=0, unknown_money_2=0,
            cp=0,
            skill_1=(0, 'Foo'),
            skill_2=(0, 'Bar'),
            skill_3=(0, 'Baz'),
            skill_4=(0, 'Frotz'),
            inv_item=0,
            inv_weapon=0,
            inv_gear=0,
            box_item=0,
            box_weapon=0,
            box_gear=0,
            val=0,
            special_label=None,
            special=0,
            special_qty=0,
            ):
        self.money = money
        self.unknown_money_1 = unknown_money_1
        self.unknown_money_2 = unknown_money_2
        self.cp = cp
        self.skill_1 = skill_1
        self.skill_2 = skill_2
        self.skill_3 = skill_3
        self.skill_4 = skill_4
        self.inv_item = inv_item
        self.inv_weapon = inv_weapon
        self.inv_gear = inv_gear
        self.box_item = box_item
        self.box_weapon = box_weapon
        self.box_gear = box_gear
        self.val = val
        self.special_label = special_label
        self.special = special
        self.special_qty = special_qty
        self.skills = [
                self.skill_1,
                self.skill_2,
                self.skill_3,
                self.skill_4,
                ]

class Inventory:

    def __init__(self, label, df, base_pos, count):
        self.label = label
        self.df = df
        self.base_pos = base_pos
        self.count = count
        self.items = []
        df.seek(base_pos)
        for _ in range(self.count):
            self.items.append(SaveItem.from_df(df))

    def report(self):
        reported = False
        for idx, item in enumerate(self.items):
            if item.has_data:
                print('{} {}: {}'.format(self.label, idx+1, item.report()))
                reported = True
        if not reported:
            print('No {}!'.format(self.label))
        print('')

    def overwrite_item_at(self, idx, *args, **kwargs):
        if idx >= len(self.items):
            print('ERROR: specified index ({}) is too high for {}'.format(idx, self.label))
        else:
            self.df.seek(self.base_pos + (16*idx))
            self.items[idx].update(self.df, *args, **kwargs)

    def clear_all(self):
        self.df.seek(self.base_pos)
        for item in self.items:
            item.clear(self.df)

class Char:

    def __init__(self, df, chartype, positions):
        self.df = df
        self.chartype = chartype
        self.name = chartype.value
        self.pos = positions
        self.skills_spent = []

        self.money = self.df.u64_attr(self.pos.money)
        # These two appear to be "counters" of some sort, for various kinds of
        # money made.  I think unknown1 is all-time income, which includes
        # Mr. Shakedown (SaveData0004.sav has 10t-1 in there, where the current-
        # money var is just 1M).
        self.unknown_money_1 = self.df.u64_attr(self.pos.unknown_money_1)
        self.unknown_money_2 = self.df.u64_attr(self.pos.unknown_money_2)
        self.cp = self.df.u16_attr(self.pos.cp)
        self.skills_spent = []
        for label, pos in self.pos.skills:
            self.skills_spent.append((label, self.df.u64_attr(pos)))
        self.inv_item = Inventory('Item Inv', df, self.pos.inv_item, 20)
        self.inv_weap = Inventory('Weapon Inv', df, self.pos.inv_weapon, 15)
        self.inv_gear = Inventory('Gear Inv', df, self.pos.inv_gear, 15)
        self.inv_val = Inventory('Valuables', df, self.pos.val, 25)
        self.inv_box_item = Inventory('Item Box', df, self.pos.box_item, 200)
        self.inv_box_weap = Inventory('Weapon Box', df, self.pos.box_weapon, 200)
        self.inv_box_gear = Inventory('Gear Box', df, self.pos.box_gear, 200)
        self.inv_special = Inventory(self.pos.special_label, df, self.pos.special, self.pos.special_qty)

    def clear_non_valuables(self, reg_inv=True, box=True):
        """
        Clears out all non-Valuables in our inventory
        """
        if reg_inv:
            self.inv_item.clear_all()
            self.inv_weap.clear_all()
            self.inv_gear.clear_all()
        if box:
            self.inv_box_item.clear_all()
            self.inv_box_weap.clear_all()
            self.inv_box_gear.clear_all()

    def add_item_by_name(self, name, *args, **kwargs):
        global items_by_name
        name_lower = name.lower()
        if name_lower in items_by_name:
            self.add_item_by_id(items_by_name[name_lower].item_id, *args, **kwargs)
        else:
            print(' - ERROR: Item name "{}" not found, cannot insert'.format(name))

    def add_item_by_id(self, item_id, qty=None, max_qty=False, to_box=False,
            force_idx=None, force_inv=None):
        global items_by_id
        item = None
        inv = None
        new_qty = 1
        ammo = 0
        strikes = 0
        hard_idx = None
        insert_idx = None
        if item_id in items_by_id:
            item = items_by_id[item_id]

            # First doublecheck for a char_lock
            if item.char_lock and item.char_lock != self.chartype:
                print(' - ERROR: Refusing to add {} to {}'.format(
                    item.name,
                    self.name,
                    ))
                return

            # If we made it here, we should be good so long as we don't run out of room.
            if item.item_type == ItemType.WEP:
                if to_box:
                    inv = self.inv_box_weap
                else:
                    inv = self.inv_weap
                if item.ammo is None:
                    # Ammo does not apply to this gun
                    ammo = -2
                elif item.ammo == 0:
                    # infinite ammo
                    ammo = -1
                else:
                    ammo = item.ammo
                if item.strikes is None or item.strikes == 0:
                    # infinite strikes.  This should be safe to assume, since we only
                    # get into this block for weapons
                    strikes = -1
                else:
                    strikes = item.strikes*10
            elif item.item_type == ItemType.GEAR:
                if to_box:
                    inv = self.inv_box_gear
                else:
                    inv = self.inv_gear
            elif item.item_type == ItemType.VAL or item.item_type == ItemType.VALJUNK:
                inv = self.inv_val
                hard_idx = item.hard_idx
            elif item.item_type == ItemType.POCKET or item.item_type == ItemType.CRAFT:
                inv = self.inv_special
                hard_idx = item.hard_idx
                # "strikes" seems to be used to decide if the item is visible in the menu,
                # and "ammo" seems to be used as an indicator that the item has been seen
                # (ie: get rid of the flashing "New" on them).  Go ahead and set those.
                strikes = 1
                ammo = 1
                if item.item_type == ItemType.CRAFT:
                    if qty is not None:
                        new_qty = max(1, min(qty, item.max_in_inv))
                    if max_qty:
                        new_qty = item.max_in_inv
            else:
                # Anything else will just go in regular "item" inventory
                if to_box:
                    # TODO: Item Box only allows a single entry per item type, so technically
                    # we'd need to check for that.
                    inv = self.inv_box_item
                    if qty is not None:
                        new_qty = max(1, min(qty, item.max_in_box))
                    if max_qty:
                        new_qty = item.max_in_box
                else:
                    inv = self.inv_item
                    if qty is not None:
                        new_qty = max(1, min(qty, item.max_in_inv))
                    if max_qty:
                        new_qty = item.max_in_inv

        # Force the inventory area if we've been told to
        if force_inv:
            inv = force_inv

        # If we still don't have an inventory to insert into, put it in the regular
        # one (and show a warning!)
        if not inv:
            print(' - WARNING: Item ID {} not found, inserting into regular inventory...'.format(item_id))
            inv = self.inv_item

        # Figure out what index in the inventory to store.  If we've been told to force
        # a specific one, use that.  Otherwise, if the itemtype wants a hard index
        # number, use that.  Otherwise, find an open slot
        if force_idx is not None:
            insert_idx = force_idx
        elif hard_idx is not None:
            insert_idx = hard_idx
        else:
            for idx, inv_item in enumerate(inv.items):
                if not inv_item.has_data:
                    insert_idx = idx
                    break
            if insert_idx is None:
                print(' - ERROR: Item ID {} could not be inserted into {} due to lack of space'.format(
                    item_id,
                    inv.label,
                    ))
                return

        # Test to see if our index is valid
        if item:
            report = '{} (ID {})'.format(item.name, item_id)
        else:
            report = 'ID {}'.format(item_id)
        if insert_idx >= len(inv.items):
            print(f' - ERROR: Cannot insert "{report}" at {inv.label} index {insert_idx} -- the inventory is not that large')
            return
        else:
            # Finally, do the insert
            extras = []
            # POCKET and CRAFT items use ammo/strike a bit differently, don't report on it then.
            if not item or (item.item_type != ItemType.POCKET and item.item_type != ItemType.CRAFT):
                if ammo == -1:
                    extras.append('ammo: ∞')
                elif ammo > 0:
                    extras.append('ammo: {}'.format(ammo))
                if strikes > 0:
                    extras.append('strikes: {}'.format(strikes/10))
            if extras:
                extra_str = ' ({})'.format(', '.join(extras))
            else:
                extra_str = ''
            print(f' - Saving {new_qty}x {report}{extra_str} in {inv.label} at idx {insert_idx}')
            inv.overwrite_item_at(insert_idx, item_id, item, new_qty, ammo, strikes)

class NotASavegameException(Exception):
    pass

class Savegame:

    save_re = re.compile(r'^(.*/)?SaveData(?P<slot>\d+)\.(?P<save_type>(sav|clr))$')

    def __init__(self, filename):
        self.filename = filename
        self.filename_short = os.path.basename(filename)
        self.df = Datafile(self.filename)

        # Check the magic
        magic = self.df.read(4)
        if magic != b'YZFH':
            raise NotASavegameException()

        # Check to see if we know what slot number this is
        self.slot_num = None
        self.clear_num = None
        if match := self.save_re.match(filename):
            if match.group('save_type') == 'sav':
                self.slot_num = int(match.group('slot'))+1
            else:
                self.clear_num = int(match.group('slot'))+1
        if self.slot_num is not None:
            self.filename_str = '{} (Slot {})'.format(self.filename, self.slot_num)
        elif self.clear_num is not None:
            self.filename_str = '{} (Clear Data {})'.format(self.filename, self.clear_num)
        else:
            self.filename_str = self.filename

        # Now start readin'

        # There are a few bits of data which get updated with every save, regardless
        # of whether anything's really changed or not, FYI:
        #
        #    1) The date/timestamp of when the save was created -- we display that
        #       down below.
        #    2) The total time spent ingame -- this is also displayed below
        #    3) An unknown couple of bytes at 0x06EAC might be updated (possibly
        #       Kiryu-specific, with a matching Majima set somewhere else)
        #    4) Some character positioning/rotation info, and possibly even camera
        #       placement info (though the camera info gets reset on loading the
        #       game).  I haven't bothered trying to decode this stuff, and I don't
        #       know if the positioning is relative to the savepoint or absolute in
        #       the map, but Kiryu's segment is roughly 0x06F98 - 0x06FB3.  (It's
        #       possible only the currently-saved char is there?  I bet it's separate
        #       between 'em, though.)
        #    5) Four unknown bytes (or maybe 8?) at 0x0F6DC might be updated
        #    6) A counter of some sort that starts at 30min and counts down to zero,
        #       then loops back to 30min.  No idea wtf that's used for.  At 0x11178
        #    7) A single byte at 0x1AA39 seems to vaccilate between various rather
        #       low numbers (I don't think I've seen higher than like 4 or 5).

        # I'd be surprised if this is what actually *controlled* who the active
        # character is, but it's at least a convenient string to display.
        self.cur_char = self.df.read_str(0x8)

        # Likewise, I wouldn't be surprised if this bit was just there for the
        # "load" dialog to show info to the user.
        self.chapter = self.df.read_u8(0x6)+1

        # Date/Time the save was, y'know, saved at.
        (self.saved_year, self.saved_month, self.saved_day_of_week, self.saved_day,
                self.saved_hours, self.saved_mins, self.saved_secs) = self.df.read_datetime(0x28)
        self.saved_txt = '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(
                self.saved_year, self.saved_month, self.saved_day,
                self.saved_hours, self.saved_mins, self.saved_secs,
                )

        # Time played
        self.secs_played = self.df.read_millis_as_seconds(0x00448)
        mins_played = self.secs_played/60
        hours_played, mins_played = (int(v) for v in divmod(mins_played, 60))
        self.played_txt = '{}:{:02d}'.format(hours_played, mins_played)

        # There's some kind of counter at 0x11178 which starts at 30min and goes
        # down to zero before looping back, also in thirds-of-milliseconds.  I
        # was thinking maybe it's used for real estate or Tiger+Dragon excursions
        # or something, but why not just use the time-played stat for that?

        # Difficulty
        self.difficulty1 = self.df.u8_attr(0x444)
        self.difficulty2 = self.df.u8_attr(0x445)
        assert(self.difficulty1.val == self.difficulty2.val)

        # Characters
        self.kiryu = Char(self.df, PC.Kiryu, CharPositions(
            money=0xF2C0,
            unknown_money_1=0xF2D0,
            unknown_money_2=0xF2E0,
            cp=0xF3E0,
            skill_1=('Brawler', 0x72F0),
            skill_2=('Rush', 0x72F8),
            skill_3=('Beast', 0x7300),
            skill_4=('Dragon', 0x7308),
            inv_item=0x07AAC,
            inv_weapon=0x0CE6C,
            inv_gear=0x0D04C,
            box_item=0x0836C,
            box_weapon=0x09C6C,
            box_gear=0x0B56C,
            val=0x07D3C,
            special_label='Pocket Circuit',
            special=0xD86C,
            special_qty=113,
            ))
        self.majima = Char(self.df, PC.Majima, CharPositions(
            money=0xF2C8,
            unknown_money_1=0xF2D8,
            unknown_money_2=0xF2E8,
            cp=0xF3E8,
            # This isn't the order in which they're shown on the screen, btw!
            skill_1=('Thug', 0x76F0),
            skill_2=('Breaker', 0x76F8),
            skill_3=('Slugger', 0x7700),
            skill_4=('Mad Dog', 0x7708),
            inv_item=0x7BEC,
            inv_weapon=0xCF5C,
            inv_gear=0xD13C,
            box_item=0x8FEC,
            box_weapon=0xA8EC,
            box_gear=0xC1EC,
            val=0x805C,
            special_label='Crafting',
            special=0xD22C,
            special_qty=96,
            ))
        self.chars = [self.kiryu, self.majima]

    def write_to(self, *args, **kwargs):
        self.df.write_to(*args, **kwargs)

    def overwrite(self, *args, **kwargs):
        self.df.overwrite(*args, **kwargs)

