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
import sys
import argparse
from remotecache.cache import RemoteCache
from y0 import PC
from y0.savegame import Savegame, NotASavegameException
from y0.itemregistry import ItemType, reg, items_by_id, items_by_name

difficulty = {
        0: 'Easy',
        1: 'Normal',
        2: 'Hard',
        3: 'Legendary',
        }

def main():

    parser = argparse.ArgumentParser(
            description='Yakuza 0 Savefiles',
            )

    parser.add_argument('filenames',
            metavar='filename',
            nargs='+',
            help='Savefile(s) to parse',
            )

    ### Choosing which char(s) to act on

    chargroup = parser.add_mutually_exclusive_group()

    chargroup.add_argument('-c', '--current',
            action='store_const',
            dest='char',
            const=PC.Current,
            help="Operate on the currently-active character (the default)",
            )

    chargroup.add_argument('-k', '--kiryu',
            action='store_const',
            dest='char',
            const=PC.Kiryu,
            help="Operate on Kiryu only",
            )

    chargroup.add_argument('-m', '--majima',
            action='store_const',
            dest='char',
            const=PC.Majima,
            help="Operate on Majima only",
            )

    chargroup.add_argument('-b', '--both',
            action='store_const',
            dest='char',
            const=PC.Both,
            help="Operate on both characters",
            )

    ### General-purpose actions

    parser.add_argument('-i', '--info',
            action='store_true',
            help="Show info about the specified savefiles",
            )

    parser.add_argument('-t', '--test',
            action='store_true',
            help="Do whatever testing thing I'm currently working on",
            )

    parser.add_argument('-r', '--refresh',
            action='store_true',
            help="""Just refresh remotecache.vdf for the specified files
                (will happen automatically if any save update occurs)""",
            )

    ### Actual actions we can take

    money_grp = parser.add_mutually_exclusive_group()

    money_grp.add_argument('--money',
            type=int,
            help="Set the currently available money",
            )

    money_grp.add_argument('--money-max',
            action='store_true',
            help="Sets available money to the maximum value",
            )

    parser.add_argument('--cp',
            type=int,
            help="Set the current CP",
            )

    parser.add_argument('--clear-all-inventory',
            action='store_true',
            help="""Clears all inventory, apart from 'Valuables' section.  Use with care!
                This will be processed before any other item-adding arguments.""",
            )

    parser.add_argument('--add-darts',
            action='append_const',
            dest='add_item_id',
            const='170,171,172,173',
            help='Gives the specified character all available darts',
            )

    parser.add_argument('--add-fishing-poles',
            action='append_const',
            dest='add_item_id',
            const='1139,1140,1141,1142,1143,1144',
            help='Gives the specified character all available fishing poles',
            )

    parser.add_argument('--add-all-weapons',
            action='store_true',
            help="""Add one of every weapon to the specified char's Item Box (if there is room).  Will
                imply --box for any other items added at the same time, too."""
            )

    parser.add_argument('--add-all-gear',
            action='store_true',
            help="""Add one of every piece of gear to the specified char's Item Box (if there is room).
                Will imply --box for any other items added at the same time, too."""
            )

    parser.add_argument('--add-all-pocket-circuit',
            action='store_true',
            help="Adds all Pocket Circuit parts to Kiryu's inventory (ignores character-selection args)",
            )

    parser.add_argument('--add-all-crafting',
            action='store_true',
            help="""Adds all crafting ingredients (at max. quantity) to Majima's inventory (ignores
                character-selection args)""",
            )

    parser.add_argument('--add-item-id',
            type=str,
            action='append',
            help="""Add the specified item ID(s) to the appropriate inventory area, if there is room.
                This option can be specified more than once, and/or be a comma-separated list.""",
            )

    parser.add_argument('--add-item-name',
            type=str,
            action='append',
            help="""Add the specified item name(s) to the appropriate inventory area, if there is room.
                This option can be specified more than once, and/or be a comma-separated list.""",
            )

    parser.add_argument('--hostess-name',
            type=str,
            action='append',
            help="""Set the level of the specified cabaret hostess(es) by name.
                This option can be specified more than once, and/or be a comma-separated list.""",
            )

    parser.add_argument('--hostess-id',
            type=str,
            action='append',
            help="""Set the level of the specified cabaret hostess(es) by id.
                This option can be specified more than once, and/or be a comma-separated list.""",
            )

    parser.add_argument('--box',
            action='store_true',
            help="If adding items, store in Item Box instead of inventory, if appropriate.",
            )

    parser.add_argument('--level',
            type=int,
            help="Level to set specified hostess(es) to.",
            )

    parser.add_argument('--sales',
            type=int,
            help="Total sales to set specified hostess(es) to.",
            )

    qty_grp = parser.add_mutually_exclusive_group()

    qty_grp.add_argument('--qty',
            type=int,
            help="If adding items, use this quantity if supported by the item type and location",
            )

    qty_grp.add_argument('--qty-max',
            action='store_true',
            help="""If adding items, use the maximum allowable quantity of the item being inserted,
                depending on the location.""",
            )

    parser.add_argument('-v', '--verbose',
            action='store_true',
            help='Verbose output (show all available info)',
            )

    # Parse args
    parser.set_defaults(char=PC.Current)
    args = parser.parse_args()

    # Sanity checks
    if args.money is not None and args.money < 0:
        args.money = 0
    if args.cp is not None and args.cp < 0:
        args.cp = 0
    if args.qty is not None and args.qty < 1:
        args.qty = 1
    
    if args.level is not None and args.level < 1:
        args.level = 1
    if args.level is not None and args.level > 40:
        args.level = 40
    if args.sales is not None and args.sales < 0:
        args.sales = 0
    
    
    # Some arg dependencies
    if args.money_max:
        args.money = 9999999999999

    # Consolidate adding item IDs
    if args.add_item_id:
        item_ids = []
        for item_id_list in args.add_item_id:
            for item_id_str in item_id_list.split(','):
                try:
                    item_id = int(item_id_str.strip())
                except ValueError as e:
                    parser.error('Item IDs must be integers ({} is invalid)'.format(item_id_str))
                if item_id < 1:
                    parser.error('Item IDs must be positive ({} is invalid)'.format(item_id_str))
                item_ids.append(item_id)
        args.add_item_id = item_ids

    # Consolidate adding item names
    if args.add_item_name:
        item_names = []
        for item_name_list in args.add_item_name:
            item_names.extend([s.strip() for s in item_name_list.split(',')])
        args.add_item_name = item_names

    # Consolidate adding hostess IDs
    if args.hostess_id:
        hostess_ids = []
        for hostess_list in args.hostess_id:
            for hostess_id_str in hostess_list.split(','):
                try:
                    hostess_id = int(hostess_id_str.strip())
                except ValueError as e:
                    parser.error('Hostess IDs must be integers ({} is invalid)'.format(hostess_id_str))
                if hostess_id < 1:
                    parser.error('Hostess IDs must be positive ({} is invalid)'.format(hostess_id_str))
                if hostess_id > 30:
                    parser.error('Hostess ID out of range ({} is invalid)'.format(hostess_id_str))
                hostess_ids.append(hostess_id)
        args.hostess_id = hostess_ids

    # Consolidate adding item names
    if args.hostess_name:
        hostess_names = []
        for hostess_name_list in args.hostess_name:
            hostess_names.extend([s.strip() for s in hostess_name_list.split(',')])
        args.hostess_name = hostess_names

    # Support our adding of all weapons/gear
    if args.add_all_weapons or args.add_all_gear:
        args.box = True
        if not args.add_item_id:
            args.add_item_id = []
        for item in reg:
            if args.add_all_weapons and item.item_type == ItemType.WEP:
                args.add_item_id.append(item.item_id)
            elif args.add_all_gear and item.item_type == ItemType.GEAR:
                args.add_item_id.append(item.item_id)

    # (through parsing args at this point)

    # Now, see if we can detect remotecache.vdf for these
    remotecaches = {}
    remotecache_map = {}
    for filename in args.filenames:
        filename_dir = os.path.abspath(os.path.dirname(filename))
        parent_dir = os.path.abspath(os.path.join(filename_dir, '..'))
        remotecache_file = os.path.join(parent_dir, 'remotecache.vdf')
        if remotecache_file in remotecaches:
            remotecache_map[filename] = remotecaches[remotecache_file]
        else:
            if os.path.exists(remotecache_file):
                cache = RemoteCache(remotecache_file)
                remotecaches[remotecache_file] = cache
                remotecache_map[filename] = cache
            else:
                remotecache_map[filename] = None
    if args.verbose:
        print('remotecache.vdf mappings found:')
        for filename, cache in sorted(remotecache_map.items()):
            print('  {} -> {}'.format(filename, cache.cache_filename))
        print('')

    # Now loop through to do stuff
    caches_to_refresh = set()
    for filename in args.filenames:

        # Load the save (if we can)
        try:
            save = Savegame(filename)
        except NotASavegameException as e:
            print('ERROR: {} is not a Y0 savegame'.format(filename))
            continue

        # Figure out what chars to process
        chars = []
        for char in save.chars:
            if args.char == PC.Both \
                    or (args.char == PC.Current and save.cur_char == char.name) \
                    or (args.char == char.chartype):
                chars.append(char)

        # Print a header no matter what, for now.
        print(save.filename_str)
        print('='*len(save.filename_str))
        print('')

        # Show info, if that's what we've been told to do
        if args.info:

            print('General')
            print('-------')
            print('Current Char: {}'.format(save.cur_char))
            print('Chapter: {}'.format(save.chapter))
            print('Saved on: {}'.format(save.saved_txt))
            print('Time Played: {}'.format(save.played_txt))
            print('Difficulty: {}'.format(difficulty[save.difficulty1.val]))
            print('')

            # Now report on character data
            for char in chars:

                print(char.name)
                print('-'*len(char.name))

                print('Money: {:,}'.format(char.money.val))
                #print('Unknown Money 1: {:,}'.format(char.unknown_money_1.val))
                #print('Unknown Money 2: {:,}'.format(char.unknown_money_2.val))
                print('CP: {}'.format(char.cp.val))
                if args.verbose:
                    # These aren't especially interesting, really, but here they are anyway.
                    for label, skill_spent in char.skills_spent:
                        print('Spent on {} Style: {:,}'.format(label, skill_spent.val))
                print('')

                # Inventories
                char.inv_item.report()
                char.inv_weap.report()
                char.inv_gear.report()
                char.inv_val.report()
                char.inv_special.report()
                if args.verbose:
                    char.inv_box_item.report()
                    char.inv_box_weap.report()
                    char.inv_box_gear.report()

        done_updates = False

        # Update money
        if args.money is not None:
            new_money_val = max(0, min(args.money, 9999999999999))
            for char in chars:
                print('Setting {} money to: {:,}'.format(char.name, new_money_val))
                char.money.val = new_money_val
            done_updates = True

        # Update CP
        if args.cp is not None:
            # TODO: The max should probably be a hell of a lot lower than this.
            new_cp_val = max(0, min(args.cp, 32768))
            for char in chars:
                print('Setting {} CP to: {:,}'.format(char.name, new_cp_val))
                char.cp.val = new_cp_val
            done_updates = True

        # Clearing inventory
        if args.clear_all_inventory:
            for char in chars:
                print('Clearing inventory for {}'.format(char.name))
                char.clear_non_valuables()
            done_updates = True

        # Adding items (by ID)
        if args.add_item_id:
            for char in chars:
                print('Adding inventory IDs for {}'.format(char.name))
                for item_id in sorted(args.add_item_id):
                    # This method does its own status printing
                    char.add_item_by_id(item_id, qty=args.qty, max_qty=args.qty_max, to_box=args.box)
            done_updates = True

        # Adding items (by Name)
        # TODO: should maybe do lookups first and then insert in numerical ID order...
        if args.add_item_name:
            for char in chars:
                print('Adding inventory names for {}'.format(char.name))
                for item_name in args.add_item_name:
                    # This method does its own status printing
                    char.add_item_by_name(item_name, qty=args.qty, max_qty=args.qty_max, to_box=args.box)
            done_updates = True

        # Leveling and setting sales for hostess(es) (by ID)
        if args.hostess_id:
            for hostess_id in sorted(args.hostess_id):
                # This method does its own status printing
                save.hostess_roster.update_hostess_by_id(hostess_id, level=args.level, sales=args.sales)
            done_updates = True

        # Leveling and setting sales for hostess(es) (by Name)
        if args.hostess_name:
            for hostess_name in args.hostess_name:
                # This method does its own status printing
                save.hostess_roster.update_hostess_by_name(hostess_name, level=args.level, sales=args.sales)
            done_updates = True

        # Adding all Pocket Circuit
        if args.add_all_pocket_circuit:
            print('Adding all Pocket Circuit parts to Kiryu')
            for item in reg:
                if args.add_all_pocket_circuit and item.item_type == ItemType.POCKET:
                    # This method does its own status printing
                    save.kiryu.add_item_by_id(item.item_id)
            done_updates = True

        # Adding all Crafting
        if args.add_all_crafting:
            print('Adding all crafting ingredients to Majima')
            for item in reg:
                if args.add_all_crafting and item.item_type == ItemType.CRAFT:
                    # This method does its own status printing
                    save.majima.add_item_by_id(item.item_id, max_qty=True)
            done_updates = True

        # Testing stuff
        if args.test:

                # Injecting items stupidly, by ID (ie: overwriting starting at index 0)
                if False:

                    item_ids = [557]*20
                    char.clear_non_valuables()
                    for idx, item_id in enumerate(item_ids):
                        char.add_item_by_id(item_id, force_idx=idx, max_qty=False, qty=100, to_box=False)
                    done_updates = True

                # Let's put one of each non-weapon/gear/craft/pocket item in the box...
                if False:
                    to_insert = []
                    for item in reg:
                        if item.item_type == ItemType.ITEM:
                            to_insert.append(item.item_id)

                    char.clear_non_valuables()
                    for item_id in to_insert[:200]:
                        char.add_item_by_id(item_id, max_qty=True, to_box=True)
                    done_updates = True

        # If we've done anything, write out the file
        if done_updates:
            print('')
            print('Writing updated savegame')
            save.overwrite()
            print('')
        elif args.refresh:
            print('Marking file as needing a remotecache.vdf refresh')
            print('')
            done_updates = True

        # Update remotecache.vdf, if we've been told to
        if done_updates:
            cache = remotecache_map[filename]
            if cache:
                caches_to_refresh.add(cache)
                cache[save.filename_short].sync()

    for cache in caches_to_refresh:
        cache.overwrite()
        print('Updated {}'.format(cache.cache_filename))
        print('')

if __name__ == '__main__':
    main()

