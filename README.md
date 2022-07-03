Yakuza 0 CLI Save Editor (WIP)
==============================

This is a pretty barebones CLI save editor for Yakuza 0.  It's a Python 3
app, and has only been tested on Linux using the United States version of
Y0, from Steam.  It seems reasonably solid for what it does, though its
functionality has quite a few gaps.  I didn't start working on this until
I was through playing Y0 "legitimately" and I ran out of steam for
working on it after getting through most of the inventory management
stuff, so this will probably remain rather incomplete.

What this editor *does* do:

 - Setting CP and Money
 - Adding any inventory item you'd like
   - Has shortcuts for adding all darts, fishing poles, pocket circuit
     parts, crafting ingredients, and complete sets of gear/weapons

Things this does *not* do yet, and probably won't (though this is
more or less a TODO in case I ever become re-energized about it):

 - Abilities editing (arbitrary Legendary style unlocks, etc)
 - Completion editing (mark arcade games / gambling as complete, etc)
 - Levelling of real estate properties
 - Set difficulty (easy enough, could be done with just a few edits)
 - Reload/repair all weapons (also easy enough)

**WARNING:** On the Steam version, Y0 saves into Steam's `userdata` dir
structure, with a `remotecache.vdf` file one dir level above the saves.
That file helps Steam know how the files interact with cloud saves, and
contains details about cloud synchronization, etc.  I always have
cloud saves disabled, so for me the file effectively only has local-file
info in it.  This editor *does* keep that info in `remotecache.vdf`
up-do-date, if that file is found one level above the save you're editing,
but this is **completely untested** in situations where cloud saves are
active.  Keep backups of your savegames!  (You should really keep backups
anyway, of course.)

Here's the output of running `y0save.py --help`:

	usage: y0save.py [-h] [-c | -k | -m | -b] [-i] [-t] [-r]
					 [--money MONEY | --money-max] [--cp CP]
					 [--clear-all-inventory] [--add-darts] [--add-fishing-poles]
					 [--add-all-weapons] [--add-all-gear]
					 [--add-all-pocket-circuit] [--add-all-crafting]
					 [--add-item-id ADD_ITEM_ID] [--add-item-name ADD_ITEM_NAME]
					 [--box] [--qty QTY | --qty-max] [-v]
					 filename [filename ...]

	Yakuza 0 Savefiles

	positional arguments:
	  filename              Savefile(s) to parse

	optional arguments:
	  -h, --help            show this help message and exit
	  -c, --current         Operate on the currently-active character (the
							default)
	  -k, --kiryu           Operate on Kiryu only
	  -m, --majima          Operate on Majima only
	  -b, --both            Operate on both characters
	  -i, --info            Show info about the specified savefiles
	  -t, --test            Do whatever testing thing I'm currently working on
	  -r, --refresh         Just refresh remotecache.vdf for the specified files
							(will happen automatically if any save update occurs)
	  --money MONEY         Set the currently available money
	  --money-max           Sets available money to the maximum value
	  --cp CP               Set the current CP
	  --clear-all-inventory
							Clears all inventory, apart from 'Valuables' section.
							Use with care! This will be processed before any other
							item-adding arguments.
	  --add-darts           Gives the specified character all available darts
	  --add-fishing-poles   Gives the specified character all available fishing
							poles
	  --add-all-weapons     Add one of every weapon to the specified char's Item
							Box (if there is room). Will imply --box for any other
							items added at the same time, too.
	  --add-all-gear        Add one of every piece of gear to the specified char's
							Item Box (if there is room). Will imply --box for any
							other items added at the same time, too.
	  --add-all-pocket-circuit
							Adds all Pocket Circuit parts to Kiryu's inventory
							(ignores character-selection args)
	  --add-all-crafting    Adds all crafting ingredients (at max. quantity) to
							Majima's inventory (ignores character-selection args)
	  --add-item-id ADD_ITEM_ID
							Add the specified item ID(s) to the appropriate
							inventory area, if there is room. This option can be
							specified more than once, and/or be a comma-separated
							list.
	  --add-item-name ADD_ITEM_NAME
							Add the specified item name(s) to the appropriate
							inventory area, if there is room. This option can be
							specified more than once, and/or be a comma-separated
							list.
		--hostess-id HOSTESS_ID
							Specify the hostess(es) by id to set their level and total
							sales. This option can be specified more than once, and/or
							be a comma-separated list.
		--hostess-name HOSTESS_NAME
							Specify the hostess(es) by name to set their level and total
							sales. This option can be specified more than once, and/or
							be a comma-separated list.
		--level LEVEL         If setting hostess levels, use this value to set the level.
							Platinum hostesses have a max level of 40. All others have a max level
							of 30
		--sales SALES         If setting hostess total sales, use this value to set the sales.
	  --box                 If adding items, store in Item Box instead of
							inventory, if appropriate.
	  --qty QTY             If adding items, use this quantity if supported by the
							item type and location
	  --qty-max             If adding items, use the maximum allowable quantity of
							the item being inserted, depending on the location.
	  -v, --verbose         Verbose output (show all available info)

So yeah, that's it.  I'm quite happy with the item-adding bits, at least,
especially being able to do it by name.  You could try, for instance:

    y0save.py SaveData0010.sav --add-item-name "dragon mail, amon sunglasses, war god talisman, golden gun"

Known Bugs / TODOs
------------------

 - There are some substory-related items which I suspect show up in the
   "valuables" section while you have them, but I don't know for sure.
   Check `y0/itemregistry.py` for some detailed notes.
 - When inserting items into the "main" non-weapon/gear Item Box, the game
   will only allow you to have one "instance" of a stacked item, whereas
   this doesn't check for that.  No clue what the game's behavior will be
   if two identical items end up in there, though I suspect it'd be fine.
 - The code is a weird combination of overengineered and underengineered.
   I never even expected it to get *this* functional -- it started out as
   just some real basic scripts to pull some info out of the save files
   and slowly accrued layers of jankiness every time it outgrew its
   simplistic roots.  So, uh, sorry about that.  Names and labels and
   general organization and really the entire implementation could use
   a total rewrite.

License
-------

All code in here is licensed under the
[3-clause BSD license](https://opensource.org/licenses/BSD-3-Clause).
See [COPYING.txt](COPYING.txt) for the full text of the license.

