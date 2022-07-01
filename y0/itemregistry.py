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

import enum
from . import PC

class ItemType(enum.Enum):
    ITEM = 'Items'
    WEP = 'Weapons'
    GEAR = 'Gear'
    VAL = 'Valuables'
    VALJUNK = 'Valuables (junk)'
    POCKET = 'Pocket Circuit'
    CRAFT = 'Crafting Materials'
    MENU = 'Restaurant/Bar Menus'
    JUNK = 'Junk/Broken'

class ItemDesc:
    """
    Description of an abstract item in Y0, intended to be used by code which
    wants to inject a new item into a savegame.  So this'll let you know
    which inventory category the item belongs to, ammo/strike maximums for
    weapons, and various stacking parameters for if you want to have more
    than one in a stack (if supported by the item + inv location).

    Note that for `max_in_box`, it's only the "item" Item Box (as opposed to
    Weapon or Gear) which supports stacked items, so that field should be
    ignored for weapons/gear.
    """

    def __init__(self, item_id, name, item_type, strikes=None, ammo=None,
            hard_idx=None,
            max_in_inv=1,
            max_in_box=99,
            char_lock=None,
            ):
        self.item_id = item_id
        self.name = name
        self.item_type = item_type
        self.strikes = strikes
        self.ammo = ammo
        self.hard_idx = hard_idx
        self.max_in_inv = max_in_inv
        self.max_in_box = max_in_box
        self.char_lock = char_lock

        # Hardcodes here to save some verbosity when defining items
        if self.item_type == ItemType.MENU:
            # MENU items have a max qty of 1 in the item box
            self.max_in_box = 1
        elif self.item_type == ItemType.CRAFT:
            # CRAFT items can stack to 999 and can only be added to Majima
            self.max_in_inv = 999
            self.char_lock = PC.Majima
        elif self.item_type == ItemType.POCKET:
            # POCKET items can only be added to Kiryu
            self.char_lock = PC.Kiryu

    def __repr__(self):
        return 'ItemDesc<{},{}>'.format(self.item_id, self.name)

class ItemRegistry:
    """
    Registry of all items in the game.  Basically just a glorified dict.
    """

    def __init__(self):
        self.items = {}

    def add(self, item_id, *args, **kwargs):
        if item_id in self.items:
            raise RuntimeError('Duplicate item id: {}'.format(item_id))
        self.items[item_id] = ItemDesc(item_id, *args, **kwargs)

    def __getitem__(self, key):
        return self.items[key]

    def __contains__(self, key):
        return key in self.items

    def __iter__(self):
        return iter(self.items.values())

reg = ItemRegistry()

# First up -- "legitimate" items that you can get in-game and are meant to
# be in your inventory in some way
reg.add(2, "Toughness Light", ItemType.ITEM)
reg.add(3, "Toughness Z", ItemType.ITEM)
reg.add(4, "Toughness ZZ", ItemType.ITEM)
reg.add(5, "Toughness Emperor", ItemType.ITEM)
reg.add(6, "Toughness Infinity", ItemType.ITEM)
reg.add(7, "Tauriner", ItemType.ITEM)
reg.add(8, "Tauriner +", ItemType.ITEM)
reg.add(9, "Tauriner ++", ItemType.ITEM)
reg.add(10, "Tauriner Maximum", ItemType.ITEM)
reg.add(11, "Staminan Light", ItemType.ITEM)
reg.add(12, "Staminan X", ItemType.ITEM)
reg.add(13, "Staminan XX", ItemType.ITEM)
reg.add(14, "Staminan Royale", ItemType.ITEM)
reg.add(15, "Staminan Spark", ItemType.ITEM)
reg.add(16, "AppStim RX", ItemType.ITEM)
reg.add(18, "Miso Ramen", ItemType.ITEM)
reg.add(19, "Squid Yakisoba", ItemType.ITEM)
reg.add(22, "Oden Soup", ItemType.ITEM)
reg.add(23, "Seaweed Rice Ball", ItemType.ITEM)
reg.add(24, "Tuna Rice Ball", ItemType.ITEM)
reg.add(25, "Salmon Rice Ball", ItemType.ITEM)
reg.add(26, "Diehard Drink", ItemType.ITEM)
reg.add(27, "Diehard MAX", ItemType.ITEM)
reg.add(28, "Super Turmeric No. 1", ItemType.ITEM)
reg.add(29, "Daikoku Black Sesame Kinako", ItemType.ITEM)
reg.add(30, "Daikoku Okinawan Black Candy", ItemType.ITEM)
reg.add(31, "Ginger Quince", ItemType.ITEM)
reg.add(32, "Extreme Lemon", ItemType.ITEM)
reg.add(33, "Extreme Lemon Sticks", ItemType.ITEM)
reg.add(36, "Mandarin Orange", ItemType.ITEM)
reg.add(38, "Sake", ItemType.ITEM)
reg.add(39, "Scotch Whisky", ItemType.ITEM)
reg.add(40, "Champagne", ItemType.ITEM)
reg.add(41, "Sweet Potato Shochu", ItemType.ITEM)
reg.add(42, "Pocket Tissues", ItemType.ITEM)
reg.add(43, "Confection Gift Box", ItemType.ITEM)
reg.add(67, "Crayfish", ItemType.ITEM, max_in_inv=99)
reg.add(68, "Whitebait", ItemType.ITEM, max_in_inv=99)
reg.add(69, "Goby", ItemType.ITEM, max_in_inv=99)
reg.add(70, "Porcupinefish", ItemType.ITEM, max_in_inv=99)
reg.add(71, "Crucian", ItemType.ITEM, max_in_inv=99)
reg.add(72, "Sweetfish", ItemType.ITEM, max_in_inv=99)
reg.add(73, "Squid", ItemType.ITEM, max_in_inv=99)
reg.add(74, "Eel", ItemType.ITEM, max_in_inv=99)
reg.add(76, "Filefish", ItemType.ITEM, max_in_inv=99)
reg.add(77, "Tiger Prawn", ItemType.ITEM, max_in_inv=99)
reg.add(78, "Koi Carp", ItemType.ITEM, max_in_inv=99)
reg.add(79, "Octopus", ItemType.ITEM, max_in_inv=99)
reg.add(80, "Conger Eel", ItemType.ITEM, max_in_inv=99)
reg.add(81, "Scorpionfish", ItemType.ITEM, max_in_inv=99)
reg.add(82, "Flounder", ItemType.ITEM, max_in_inv=99)
reg.add(83, "Softshell Turtle", ItemType.ITEM, max_in_inv=99)
reg.add(84, "Spider Crab", ItemType.ITEM, max_in_inv=99)
reg.add(85, "Nishiki Carp", ItemType.ITEM, max_in_inv=99)
reg.add(86, "Rainbow Trout", ItemType.ITEM, max_in_inv=99)
reg.add(87, "Salmon", ItemType.ITEM, max_in_inv=99)
reg.add(88, "Fugu", ItemType.ITEM, max_in_inv=99)
reg.add(89, "Great White", ItemType.ITEM, max_in_inv=99)
reg.add(90, "Sea Bream", ItemType.ITEM, max_in_inv=99)
reg.add(91, "Ito", ItemType.ITEM, max_in_inv=99)
reg.add(92, "Marlin", ItemType.ITEM, max_in_inv=99)
reg.add(93, "Ghost Koi", ItemType.ITEM, max_in_inv=99)
reg.add(94, "Tuna", ItemType.ITEM, max_in_inv=99)
reg.add(95, "Oarfish", ItemType.ITEM, max_in_inv=99)
reg.add(110, "Platinum Plate", ItemType.ITEM, max_in_inv=99)
reg.add(111, "Gold Plate", ItemType.ITEM, max_in_inv=99)
reg.add(112, "Silver Plate", ItemType.ITEM, max_in_inv=99)
reg.add(113, "Bronze Plate", ItemType.ITEM, max_in_inv=99)
reg.add(114, "Iron Plate", ItemType.ITEM, max_in_inv=99)
reg.add(220, "Sturdy Iron Pipe", ItemType.WEP, strikes=0)
reg.add(221, "Extremely Sturdy Iron Pipe", ItemType.WEP, strikes=0)
reg.add(222, "Lumber", ItemType.WEP, strikes=12)
reg.add(223, "Iron Pipe", ItemType.WEP, strikes=18)
reg.add(224, "Superalloy Pipe", ItemType.WEP, strikes=20)
reg.add(225, "Police Baton", ItemType.WEP, strikes=16)
reg.add(226, "Modified Police Baton", ItemType.WEP, strikes=18)
reg.add(227, "Gentleman's Umbrella", ItemType.WEP, strikes=15)
reg.add(228, "Colorful Parasol", ItemType.WEP, strikes=22)
reg.add(229, "Antique Oilpaper Umbrella", ItemType.WEP, strikes=26)
reg.add(230, "Blackjack", ItemType.WEP, strikes=12)
reg.add(231, "Ballbuster", ItemType.WEP, strikes=14)
reg.add(232, "Golden Blackjack", ItemType.WEP, strikes=16)
reg.add(233, "Master Ball", ItemType.WEP, strikes=12)
reg.add(234, "Dagger", ItemType.WEP, strikes=12)
reg.add(235, "Masterwork Dagger", ItemType.WEP, strikes=14)
reg.add(236, "Goemon", ItemType.WEP, strikes=18)
reg.add(237, "Legendary Shintogo", ItemType.WEP, strikes=22)
reg.add(238, "Dragon God Shortsword", ItemType.WEP, strikes=24)
reg.add(239, "Sturdy Knife", ItemType.WEP, strikes=0)
reg.add(240, "Extremely Sturdy Knife", ItemType.WEP, strikes=0)
reg.add(241, "Butterfly Knife", ItemType.WEP, strikes=10)
reg.add(242, "Super Spicy Knife", ItemType.WEP, strikes=14)
reg.add(243, "Chinese Broadsword", ItemType.WEP, strikes=16)
reg.add(244, "Lotus Clan Broadsword", ItemType.WEP, strikes=20)
reg.add(245, "Emperor Guan's Broadsword", ItemType.WEP, strikes=24)
reg.add(246, "Old Stun Gun", ItemType.WEP, strikes=6)
reg.add(247, "Stun Gun", ItemType.WEP, strikes=15)
reg.add(248, "Hyper Stun Gun", ItemType.WEP, strikes=18)
reg.add(249, "Sturdy Bat", ItemType.WEP, strikes=0)
reg.add(250, "Extremely Sturdy Bat", ItemType.WEP, strikes=0)
reg.add(251, "Metal Bat", ItemType.WEP, strikes=30)
reg.add(252, "Spiked Bat", ItemType.WEP, strikes=18)
reg.add(253, "Patriarch's Bat", ItemType.WEP, strikes=22)
reg.add(254, "Superalloy Bat", ItemType.WEP, strikes=32)
reg.add(255, "Legendary Kinryu Bat", ItemType.WEP, strikes=22)
reg.add(256, "Wooden Driver", ItemType.WEP, strikes=8)
reg.add(257, "Metal Iron", ItemType.WEP, strikes=14)
reg.add(258, "Patriarch's Driver", ItemType.WEP, strikes=12)
reg.add(259, "Dragon Driver", ItemType.WEP, strikes=22)
reg.add(260, "Sturdy Wooden Katana", ItemType.WEP, strikes=0)
reg.add(261, "Extremely Sturdy Wooden Katana", ItemType.WEP, strikes=0)
reg.add(262, "Wooden Katana", ItemType.WEP, strikes=16)
reg.add(263, "Sacred Wooden Katana", ItemType.WEP, strikes=24)
reg.add(264, "Nameless Katana", ItemType.WEP, strikes=12)
reg.add(265, "Sakura Storm", ItemType.WEP, strikes=18)
reg.add(266, "Morning Tempest", ItemType.WEP, strikes=20)
reg.add(267, "Yoshiyuki", ItemType.WEP, strikes=20)
reg.add(268, "Sunburst", ItemType.WEP, strikes=22)
reg.add(269, "Celestial Steed", ItemType.WEP, strikes=24)
reg.add(270, "Dragon Slayer", ItemType.WEP, strikes=20)
reg.add(271, "Ama no Murakumo", ItemType.WEP, strikes=24)
reg.add(272, "Photon Blade Prototype", ItemType.WEP, strikes=24)
reg.add(273, "Sturdy Iron Hammer", ItemType.WEP, strikes=0)
reg.add(274, "Extremely Sturdy Iron Hammer", ItemType.WEP, strikes=0)
reg.add(275, "Big Festival Fan", ItemType.WEP, strikes=10)
reg.add(276, "Iron Hammer", ItemType.WEP, strikes=6)
reg.add(277, "Warning Sign", ItemType.WEP, strikes=1)
reg.add(278, "Fortune Mallet", ItemType.WEP, strikes=7)
reg.add(279, "Frozen Tuna", ItemType.WEP, strikes=12)
reg.add(280, "Raging Dragon Hammer", ItemType.WEP, strikes=9)
reg.add(281, "Yagyu Greatsword", ItemType.WEP, strikes=12)
reg.add(282, "Exorcism Greatsword", ItemType.WEP, strikes=15)
reg.add(283, "Sturdy Pole", ItemType.WEP, strikes=0)
reg.add(284, "Extremely Sturdy Pole", ItemType.WEP, strikes=0)
reg.add(285, "Long Lumber", ItemType.WEP, strikes=9)
reg.add(286, "Six-Fluted Pole", ItemType.WEP, strikes=12)
reg.add(287, "Collapsible Steel Staff", ItemType.WEP, strikes=18)
reg.add(288, "Sacred Wooden Staff", ItemType.WEP, strikes=24)
reg.add(289, "Thunder God Staff", ItemType.WEP, strikes=26)
reg.add(290, "Assassin's Spear", ItemType.WEP, strikes=18)
reg.add(291, "L Photon Blade Prototype", ItemType.WEP, strikes=15)
reg.add(292, "Cleaving Pole", ItemType.WEP, strikes=18)
reg.add(293, "Great Marlin", ItemType.WEP, strikes=20)
reg.add(294, "Mighty Dragon Spear", ItemType.WEP, strikes=26)
reg.add(295, "Golden Rifle", ItemType.WEP, ammo=12)
reg.add(296, "Broken M1985", ItemType.WEP, ammo=10)
reg.add(297, "EXPULSION S-12", ItemType.WEP, ammo=18)
reg.add(298, "MJM56-55 Exorcist", ItemType.WEP, ammo=21)
reg.add(299, "Slime Gun", ItemType.WEP, ammo=16)
reg.add(300, "Zap Gun", ItemType.WEP, ammo=18)
reg.add(301, "Smoke Gun", ItemType.WEP, ammo=20)
reg.add(302, "Sturdy Brass Knuckles", ItemType.WEP, strikes=0)
reg.add(303, "Extremely Sturdy Brass Knuckles", ItemType.WEP, strikes=0)
reg.add(304, "Brass Knuckles", ItemType.WEP, strikes=18)
reg.add(305, "Steel Knuckles", ItemType.WEP, strikes=24)
reg.add(306, "Konpeito", ItemType.WEP, strikes=28)
reg.add(307, "Dragon Grudge Fists", ItemType.WEP, strikes=32)
reg.add(308, "Bagh Naka", ItemType.WEP, strikes=12)
reg.add(309, "Assassin's Bagh Naka", ItemType.WEP, strikes=16)
reg.add(310, "Tiger Bagh Naka", ItemType.WEP, strikes=20)
reg.add(311, "Bottomless Lighter", ItemType.WEP, strikes=0) # not actually a ranged weapon!
reg.add(312, "Modified Bottomless Lighter", ItemType.WEP, ammo=0)
reg.add(313, "Modified Lighter", ItemType.WEP, ammo=10)
reg.add(314, "Modified Deluxe Lighter", ItemType.WEP, ammo=18)
reg.add(315, "Slime Spray", ItemType.WEP, ammo=10)
reg.add(316, "Venom Spray", ItemType.WEP, ammo=12)
reg.add(317, "Table Salt", ItemType.WEP, strikes=6)
reg.add(318, "Firecracker", ItemType.WEP, strikes=10)
reg.add(319, "Steel Business Card", ItemType.WEP, strikes=30)
reg.add(320, "Marlin Cannon", ItemType.WEP, ammo=7)
reg.add(321, "Cannon", ItemType.WEP, ammo=4)
reg.add(322, "Destroyer of Lands", ItemType.WEP, ammo=5)
reg.add(323, "Sturdy Tonfa", ItemType.WEP, strikes=0)
reg.add(324, "Extremely Sturdy Tonfa", ItemType.WEP, strikes=0)
reg.add(325, "Wooden Tonfa", ItemType.WEP, strikes=15)
reg.add(326, "Carbon Tonfa", ItemType.WEP, strikes=18)
reg.add(327, "Steel Tonfa", ItemType.WEP, strikes=26)
reg.add(328, "Slashing Tonfa", ItemType.WEP, strikes=22)
reg.add(329, "Steel Crowbar", ItemType.WEP, strikes=20)
reg.add(330, "Yinglong Tonfa", ItemType.WEP, strikes=28)
reg.add(331, "Dragon Horn", ItemType.WEP, strikes=30)
reg.add(332, "Sturdy Nunchaku", ItemType.WEP, strikes=0)
reg.add(333, "Extremely Sturdy Nunchaku", ItemType.WEP, strikes=0)
reg.add(334, "Wooden Nunchaku", ItemType.WEP, strikes=15)
reg.add(335, "Carbon Nunchaku", ItemType.WEP, strikes=18)
reg.add(336, "Frozen Sardines", ItemType.WEP, strikes=15)
reg.add(337, "Spark 15000V", ItemType.WEP, strikes=20)
reg.add(338, "Daikon Nunchaku", ItemType.WEP, strikes=15)
reg.add(339, "Dynamite Nunchaku", ItemType.WEP, strikes=22)
reg.add(340, "Dragon Nunchaku", ItemType.WEP, strikes=30)
reg.add(341, "Sickle Nunchaku", ItemType.WEP, strikes=18)
reg.add(342, "Baiken", ItemType.WEP, strikes=20)
reg.add(343, "Sturdy Kali Sticks", ItemType.WEP, strikes=0)
reg.add(344, "Extremely Sturdy Kali Sticks", ItemType.WEP, strikes=0)
reg.add(345, "Double Slats", ItemType.WEP, strikes=12)
reg.add(346, "Wooden Kali Sticks", ItemType.WEP, strikes=18)
reg.add(347, "Spiked Taiko Sticks", ItemType.WEP, strikes=20)
reg.add(348, "Double Feathered Fans", ItemType.WEP, strikes=20)
reg.add(349, "Twin Dragon Sticks", ItemType.WEP, strikes=24)
reg.add(350, "Musashi's Wooden Katana", ItemType.WEP, strikes=32)
reg.add(351, "Double Chinese Broadswords", ItemType.WEP, strikes=18)
reg.add(352, "Guan & Lotus Broadswords", ItemType.WEP, strikes=26)
reg.add(353, "Modified Model Gun", ItemType.WEP, ammo=10)
reg.add(354, "Antique Gun", ItemType.WEP, ammo=6)
reg.add(355, "9mm Automatic Pistol", ItemType.WEP, ammo=10)
reg.add(356, "Double Action Revolver", ItemType.WEP, ammo=6)
reg.add(357, "Drow-Z 55", ItemType.WEP, ammo=18)
reg.add(358, "Tiger's Bane", ItemType.WEP, ammo=10)
reg.add(359, "Mr. Random", ItemType.WEP, ammo=25)
reg.add(360, "Golden Pistol", ItemType.WEP, ammo=0)
reg.add(361, "Manga Magazine", ItemType.GEAR)
reg.add(362, "Binding", ItemType.GEAR)
reg.add(363, "Sarong", ItemType.GEAR)
reg.add(364, "Bloody Binding", ItemType.GEAR)
reg.add(365, "Fighter's Binding", ItemType.GEAR)
reg.add(366, "Elder's Belly Warmer", ItemType.GEAR)
reg.add(367, "Hawker's Belly Warmer", ItemType.GEAR)
reg.add(368, "Fur Belly Warmer", ItemType.GEAR)
reg.add(369, "Lucky Binding", ItemType.GEAR)
reg.add(370, "Gambler's Binding", ItemType.GEAR)
reg.add(371, "Secret Stash Binding", ItemType.GEAR)
reg.add(372, "Fearless Binding", ItemType.GEAR)
reg.add(373, "Dragon's Binding", ItemType.GEAR)
reg.add(374, "Chain Mail", ItemType.GEAR)
reg.add(375, "Battle Mail", ItemType.GEAR)
reg.add(376, "Steel Mail", ItemType.GEAR)
reg.add(377, "Antique Chain Mail", ItemType.GEAR)
reg.add(378, "Chain Shirt", ItemType.GEAR)
reg.add(379, "Regal Chain Shirt", ItemType.GEAR)
reg.add(380, "Dragon Mail", ItemType.GEAR)
reg.add(381, "Fireproof Shirt", ItemType.GEAR)
reg.add(382, "Insulated Shirt", ItemType.GEAR)
reg.add(383, "Baseball Shirt", ItemType.GEAR)
reg.add(384, "Tour T-Shirt", ItemType.GEAR)
reg.add(385, "Avarice Shirt", ItemType.GEAR)
reg.add(386, "Wild Shirt", ItemType.GEAR)
reg.add(387, "Celestial Garb", ItemType.GEAR)
reg.add(388, "Dragon Shirt", ItemType.GEAR)
reg.add(389, "Metal Jacket", ItemType.GEAR)
reg.add(390, "Jet Black Jacket", ItemType.GEAR)
reg.add(391, "Military Jacket", ItemType.GEAR)
reg.add(392, "Yakuza Training Gear", ItemType.GEAR)
reg.add(393, "Training Gear", ItemType.GEAR)
reg.add(394, "Makoto Surcoat", ItemType.GEAR)
reg.add(395, "Comfy Soles", ItemType.GEAR)
reg.add(396, "Contact Lenses", ItemType.GEAR)
reg.add(397, "Springy Arm Guards", ItemType.GEAR)
reg.add(398, "Secret Wallet", ItemType.GEAR)
reg.add(399, "Gauntlets", ItemType.GEAR)
reg.add(400, "Alertness Hood", ItemType.GEAR)
reg.add(401, "Steel Shin Guards", ItemType.GEAR)
reg.add(402, "Silent Shoes", ItemType.GEAR)
reg.add(403, "Mew Shoes", ItemType.GEAR)
reg.add(404, "Headgear", ItemType.GEAR)
reg.add(405, "Security Wallet", ItemType.GEAR)
reg.add(406, "High-Tech Arm Guards", ItemType.GEAR)
reg.add(407, "High-Tech Shin Guards", ItemType.GEAR)
reg.add(408, "Hercules Gloves", ItemType.GEAR)
reg.add(409, "Leech Gloves", ItemType.GEAR)
reg.add(410, "Rage Ring", ItemType.GEAR)
reg.add(411, "Tourmaline Bracelet", ItemType.GEAR)
reg.add(412, "Debt Collector's Necklace", ItemType.GEAR)
reg.add(413, "Sacrifice Stone", ItemType.GEAR)
reg.add(414, "Tattered Scarf", ItemType.GEAR)
reg.add(415, "Champion's Ring", ItemType.GEAR)
reg.add(416, "Head Honcho Scarf", ItemType.GEAR)
reg.add(417, "Ebisu Socks", ItemType.GEAR)
reg.add(418, "Beads of Good Fortune", ItemType.GEAR)
reg.add(419, "Celebrity Perfume", ItemType.GEAR)
reg.add(420, "Payback Ring", ItemType.GEAR)
reg.add(421, "Dragon God Amulet", ItemType.GEAR)
reg.add(422, "Mad Dog Gloves", ItemType.GEAR)
reg.add(423, "Protective Amulet", ItemType.GEAR)
reg.add(424, "Bulletproof Glass Amulet", ItemType.GEAR)
reg.add(425, "Goddess of Children Amulet", ItemType.GEAR)
reg.add(426, "Berserker Charm", ItemType.GEAR)
reg.add(427, "Traveler's Amulet", ItemType.GEAR)
reg.add(428, "Benkei's Amulet", ItemType.GEAR)
reg.add(429, "War God Talisman", ItemType.GEAR)
reg.add(430, "Leather Belt", ItemType.GEAR)
reg.add(431, "Black Belt", ItemType.GEAR)
reg.add(432, "Boozer Belt", ItemType.GEAR)
reg.add(433, "Immovable Belt", ItemType.GEAR)
reg.add(434, "Sprite Belt", ItemType.GEAR)
reg.add(435, "Collateral Damage Belt", ItemType.GEAR)
reg.add(436, "Magic Belt", ItemType.GEAR)
reg.add(437, "Charismatic Photo", ItemType.GEAR)
reg.add(438, "Calming Towel", ItemType.GEAR)
reg.add(439, "Charismatic Autobiography", ItemType.GEAR)
reg.add(441, "Card Watcher", ItemType.GEAR)
reg.add(442, "Encounter Finder", ItemType.GEAR)
reg.add(443, "Trouble Finder", ItemType.GEAR)
reg.add(444, "Magnetic Necklace", ItemType.GEAR)
reg.add(445, "Thug Necklace", ItemType.GEAR)
reg.add(446, "Slugger Necklace", ItemType.GEAR)
reg.add(447, "Breaker Necklace", ItemType.GEAR)
reg.add(448, "Mad Dog Collar", ItemType.GEAR)
reg.add(449, "Brawler Amulet", ItemType.GEAR)
reg.add(450, "Rush Amulet", ItemType.GEAR)
reg.add(451, "Beast Amulet", ItemType.GEAR)
reg.add(452, "Dojima Family Amulet", ItemType.GEAR)
reg.add(453, "Amon Sunglasses", ItemType.GEAR)
reg.add(552, "Medieval Silver Coin", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(553, "Tin Toy", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(554, "Medieval Gold Goin", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(555, "Insect Fossil", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(556, "Crystal Ball", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(557, "Buddhist Statue", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(558, "Dinosaur Fossil", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(559, "Clay Figurine", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(560, "Medieval Painting", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(561, "Marble Sphere", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(562, "Meteor Fragment", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(563, "Primeval Sword", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(564, "UFO Part", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(565, "Silver Chalice", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(566, "Visionary Painting", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(567, "Crystal Skull", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(568, "Golden Buddhist Statue", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(569, "Huge Rough Diamond", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(570, "Orichalcum", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(571, "Golden Dragon Statue", ItemType.ITEM, max_in_inv=999, max_in_box=999)
reg.add(660, "Bait", ItemType.ITEM)
reg.add(661, "Quality Bait", ItemType.ITEM)
reg.add(662, "Special Bait", ItemType.ITEM)
reg.add(663, "Top-Grade Bait", ItemType.ITEM)
reg.add(664, "Stone of Enduring", ItemType.GEAR)
reg.add(678, "Golden Shotgun", ItemType.WEP, ammo=99)
reg.add(679, "Quick-Change Clothes", ItemType.GEAR)
reg.add(680, "Diamond Plate", ItemType.ITEM, max_in_inv=99)
reg.add(681, "Incomparable Habu Drink", ItemType.ITEM) 
reg.add(682, "Black Bass", ItemType.ITEM, max_in_inv=99)
reg.add(683, "Snakehead", ItemType.ITEM, max_in_inv=99)
reg.add(684, "Silver Arowana", ItemType.ITEM, max_in_inv=99)
reg.add(685, "Axolotl", ItemType.ITEM, max_in_inv=99)
reg.add(686, "Coelacanth", ItemType.ITEM, max_in_inv=99)
reg.add(702, "Bento Lunch Set", ItemType.ITEM)
reg.add(703, "Bento Lunch Set (Pork)", ItemType.ITEM)
reg.add(705, "Miso Cutlet Lunch Set", ItemType.ITEM)
reg.add(708, "Club Sandwich", ItemType.ITEM)
reg.add(709, "Tuna & Egg Sandwich", ItemType.ITEM)
reg.add(710, "Special Yakisoba", ItemType.ITEM)
reg.add(711, "Steamed Bun", ItemType.ITEM)
reg.add(712, "Bean Paste Bun", ItemType.ITEM)
reg.add(719, "Milk", ItemType.ITEM)
reg.add(721, "Sushi Set", ItemType.ITEM)
reg.add(725, "Yakitori", ItemType.ITEM)
reg.add(727, "Suntory Oolong Tea", ItemType.ITEM)
reg.add(728, "Expired Lunch Set", ItemType.ITEM)
reg.add(730, "French Cologne", ItemType.ITEM)
reg.add(731, "French Perfume", ItemType.ITEM)
reg.add(732, "Italian Cologne", ItemType.ITEM)
reg.add(733, "Italian Perfume", ItemType.ITEM)
reg.add(734, "French Scarf", ItemType.ITEM)
reg.add(735, "French Wallet", ItemType.ITEM)
reg.add(736, "Italian Scarf", ItemType.ITEM)
reg.add(737, "Italian Wallet", ItemType.ITEM)
reg.add(738, "French Handbag", ItemType.ITEM)
reg.add(739, "Italian Shoulder Bag", ItemType.ITEM)
reg.add(740, "Swiss Watch", ItemType.ITEM)
reg.add(746, "Italian Woman's Watch", ItemType.ITEM)
reg.add(747, "Italian Necklace", ItemType.ITEM)
reg.add(749, "Italian Ring", ItemType.ITEM)
reg.add(750, "Italian Men's Necklace", ItemType.ITEM)
reg.add(751, "Gold Bracelet", ItemType.ITEM)
reg.add(752, "Silver Bracelet", ItemType.ITEM)
reg.add(757, "Italian Boots", ItemType.ITEM)
reg.add(758, "French Sandals", ItemType.ITEM)
reg.add(760, "British Woman's Coat", ItemType.ITEM)
reg.add(762, "Leopard Print Coat", ItemType.ITEM)
reg.add(765, "Leopard Print Mini Skirt", ItemType.ITEM)
reg.add(767, "Handbag", ItemType.ITEM)
reg.add(769, "Short Black Boots", ItemType.ITEM)
reg.add(770, "Long Camel-Colored Boots", ItemType.ITEM)
reg.add(938, "Takoyaki 8 pcs.", ItemType.ITEM)
reg.add(939, "Takoyaki 16 pcs.", ItemType.ITEM)
reg.add(940, "Cheese Takoyaki 8 pcs.", ItemType.ITEM)
reg.add(953, "Ruby Plate", ItemType.ITEM, max_in_inv=99)
reg.add(959, "Matsutake", ItemType.ITEM)
reg.add(960, "Maitake", ItemType.ITEM)
reg.add(961, "Eringinoko", ItemType.ITEM)
reg.add(962, "Enokitake", ItemType.ITEM)
reg.add(963, "Shiitake", ItemType.ITEM)
reg.add(964, "Chestnut the Squirrel (Blue)", ItemType.ITEM)
reg.add(965, "Bunchan the Java Sparrow (White)", ItemType.ITEM)
reg.add(966, "Chestnut the Squirrel (Red)", ItemType.ITEM)
reg.add(967, "Bunchan the Java Sparrow (Pink)", ItemType.ITEM)
reg.add(968, "Jumbo Chestnut", ItemType.ITEM)
reg.add(969, "Jumbo Bunchan", ItemType.ITEM)
reg.add(970, "Opa-Opa Figure", ItemType.ITEM)
reg.add(971, "Woo Papa", ItemType.ITEM)
reg.add(972, "Woo Mama", ItemType.ITEM)
reg.add(973, "Woo-kun", ItemType.ITEM)
reg.add(974, "Frill-necked Lizard", ItemType.ITEM)
reg.add(975, "Kyon-bo", ItemType.ITEM)
reg.add(976, "Kyon-chan", ItemType.ITEM)
reg.add(977, "Kara Kappa", ItemType.ITEM)
reg.add(978, "Mega Drive Stuffed Toy", ItemType.ITEM)
reg.add(1002, "Legendary Drinker of Ryukyu", ItemType.ITEM)
reg.add(1003, "Repair Kit", ItemType.ITEM)
reg.add(1006, "Malt's", ItemType.ITEM)
reg.add(1007, "Kakubin", ItemType.ITEM)
reg.add(1008, "Carlsberg", ItemType.ITEM)
reg.add(1009, "Gold Champagne", ItemType.ITEM)
reg.add(1010, "Barley Shochu", ItemType.ITEM)
reg.add(1011, "Chestnut Shochu", ItemType.ITEM)
reg.add(1074, "7 Up", ItemType.ITEM)
reg.add(1075, "Mountain Dew", ItemType.ITEM)
reg.add(1076, "Sakkuru Biscuits", ItemType.ITEM)
reg.add(1106, "Tonkotsu Ramen", ItemType.ITEM)
reg.add(1107, "Shrink-wrapped Magazine", ItemType.ITEM)
reg.add(1108, "Candy", ItemType.ITEM)
reg.add(1109, "Tatsu Brand Drink", ItemType.ITEM)
reg.add(1110, "Ultra Tatsu Brand Drink", ItemType.ITEM)
reg.add(1134, "Chasu Ramen", ItemType.ITEM)
reg.add(1145, "Staminan Spork", ItemType.ITEM)
reg.add(1146, "Amon Pocket Tissues", ItemType.ITEM)

# Extra not-actually-legitimate-but-work-fine consumables
reg.add(35, "Ointment", ItemType.ITEM)
reg.add(698, "Grilled Rice Ball with Butter", ItemType.ITEM)
reg.add(699, "Grilled Rice Ball with Miso", ItemType.ITEM)
reg.add(700, "Tonkotsu Rice Ball", ItemType.ITEM)
reg.add(701, "Sauce Rice Ball", ItemType.ITEM)
reg.add(704, "Zangi Lunch Set", ItemType.ITEM)
reg.add(706, "Okonomiyaki Lunch Set", ItemType.ITEM)
reg.add(707, "Pan Fried Gyoza Lunch Set", ItemType.ITEM)
reg.add(722, "Wormwood", ItemType.ITEM)
reg.add(724, "Miso Paste Cucumber", ItemType.ITEM)
reg.add(1102, "Vanilla Ice Cream", ItemType.ITEM)
reg.add(1103, "Chocolate Ice Cream", ItemType.ITEM)
reg.add(1104, "Mint Ice Cream", ItemType.ITEM)

# Extra fish type, not found in Kamurocho or Sotenbori waters
reg.add(75, "Electric Catfish", ItemType.ITEM)

# Weapons not legitimately acquireable
reg.add(667, "Demonfire Dagger", ItemType.WEP, strikes=0)
reg.add(677, "Pummeling Bat", ItemType.WEP, strikes=0)
reg.add(142, "Test Hammer", ItemType.WEP, strikes=6)
reg.add(145, "Test Gun", ItemType.WEP, ammo=0)

# Mission-related items, I think -- do these actually show in in VAL, or do they
# consume item slots?  TODO: test -- pretty sure that these do consume item slots.
reg.add(954, "Paper Plate", ItemType.ITEM, max_in_inv=99)
reg.add(955, "Battery", ItemType.ITEM)
reg.add(980, "Sneakers", ItemType.ITEM)

# Stuff which belongs in the "valuable" section.  These seem to need to be in
# specific slots in order to actually work properly.
reg.add(665, "Pager", ItemType.VAL, hard_idx=1)
reg.add(666, "Telephone Card Album", ItemType.VAL, hard_idx=2)
reg.add(165, "Shogi Points", ItemType.VAL, hard_idx=0)
reg.add(170, "Standard Darts", ItemType.VAL, hard_idx=14)
reg.add(171, "Custom Darts", ItemType.VAL, hard_idx=15)
reg.add(172, "Sniper Darts", ItemType.VAL, hard_idx=16)
reg.add(173, "Battle-Tested Darts", ItemType.VAL, hard_idx=17)
reg.add(958, "Isobe Fan", ItemType.VAL, hard_idx=12)
reg.add(1139, "Easy Starter", ItemType.VAL, hard_idx=18)
reg.add(1140, "River Classic", ItemType.VAL, hard_idx=19)
reg.add(1141, "Rivermaster", ItemType.VAL, hard_idx=20)
reg.add(1142, "Sea Classic", ItemType.VAL, hard_idx=21)
reg.add(1143, "Seamaster", ItemType.VAL, hard_idx=22)
reg.add(1144, "Peerless Pole", ItemType.VAL, hard_idx=23)

# Substory-related items which I *think* probably show up in the Valuables
# section during the mission progress.  You can treat these like regular
# items if you put 'em there, but if they ever end up in the Item Box, they
# will be stuck there forever and can't be taken out.  So I'm putting 'em
# in this category for now, pending more testing w/ the substories.
# TODO: ^ that testing.
reg.add(168, "Piping Hot Takoyaki", ItemType.VAL)
reg.add(979, "Absorbent Sheet", ItemType.VAL)
reg.add(981, "Fan's Business Card", ItemType.VAL)
reg.add(956, "Heart Necklace", ItemType.VAL)
reg.add(957, "The Videotape", ItemType.VAL)
reg.add(1005, "Cold Takoyaki", ItemType.VAL)
reg.add(1105, "Handmade Amulet", ItemType.VAL)

# Pocket Circuit
reg.add(1125, "Red Blaze", ItemType.POCKET, hard_idx=0)
reg.add(1126, "Blue Bolt", ItemType.POCKET, hard_idx=1)
reg.add(1127, "Sunshine", ItemType.POCKET, hard_idx=2)
reg.add(1128, "Dark Purple", ItemType.POCKET, hard_idx=3)
reg.add(1129, "DRAGON", ItemType.POCKET, hard_idx=4)
reg.add(1130, "Golem Tiger", ItemType.POCKET, hard_idx=5)
reg.add(1131, "Cool Striker", ItemType.POCKET, hard_idx=6)
reg.add(1132, "Devil Killer", ItemType.POCKET, hard_idx=7)
reg.add(1133, "Killer Bee", ItemType.POCKET, hard_idx=8)
reg.add(992, "Balanced Frame", ItemType.POCKET, hard_idx=9)
reg.add(1078, "Balanced Frame Plus", ItemType.POCKET, hard_idx=10)
reg.add(1079, "Extra Balanced Frame", ItemType.POCKET, hard_idx=11)
reg.add(1080, "Super Balanced Frame", ItemType.POCKET, hard_idx=12)
reg.add(1081, "Ultra Balanced Frame", ItemType.POCKET, hard_idx=13)
reg.add(1082, "Metal Frame", ItemType.POCKET, hard_idx=14)
reg.add(1083, "Metal Frame Plus", ItemType.POCKET, hard_idx=15)
reg.add(1084, "Extra Metal Frame", ItemType.POCKET, hard_idx=16)
reg.add(1085, "Super Metal Frame", ItemType.POCKET, hard_idx=17)
reg.add(1086, "Ultra Metal Frame", ItemType.POCKET, hard_idx=18)
reg.add(1087, "Rocket Frame", ItemType.POCKET, hard_idx=19)
reg.add(1088, "Rocket Frame Plus", ItemType.POCKET, hard_idx=20)
reg.add(1089, "Extra Rocket Frame", ItemType.POCKET, hard_idx=21)
reg.add(1090, "Super Rocket Frame", ItemType.POCKET, hard_idx=22)
reg.add(1091, "Ultra Rocket Frame", ItemType.POCKET, hard_idx=23)
reg.add(1092, "Rubber Frame", ItemType.POCKET, hard_idx=24)
reg.add(1093, "Rubber Frame Plus", ItemType.POCKET, hard_idx=25)
reg.add(1094, "Extra Rubber Frame", ItemType.POCKET, hard_idx=26)
reg.add(1095, "Super Rubber Frame", ItemType.POCKET, hard_idx=27)
reg.add(1096, "Ultra Rubber Frame", ItemType.POCKET, hard_idx=28)
reg.add(1097, "Speed Frame", ItemType.POCKET, hard_idx=29)
reg.add(1098, "Speed Frame Plus", ItemType.POCKET, hard_idx=30)
reg.add(1099, "Extra Speed Frame", ItemType.POCKET, hard_idx=31)
reg.add(1100, "Super Speed Frame", ItemType.POCKET, hard_idx=32)
reg.add(1101, "Ultra Speed Frame", ItemType.POCKET, hard_idx=33)
reg.add(585, "Bumper Plate", ItemType.POCKET, hard_idx=34)
reg.add(591, "Power Motor", ItemType.POCKET, hard_idx=35)
reg.add(592, "Power Motor Plus", ItemType.POCKET, hard_idx=36)
reg.add(593, "Extra Power Motor", ItemType.POCKET, hard_idx=37)
reg.add(594, "Super Power Motor", ItemType.POCKET, hard_idx=38)
reg.add(595, "Ultra Power Motor", ItemType.POCKET, hard_idx=39)
reg.add(596, "Speed Motor", ItemType.POCKET, hard_idx=40)
reg.add(597, "Speed Motor Plus", ItemType.POCKET, hard_idx=41)
reg.add(598, "Extra Speed Motor", ItemType.POCKET, hard_idx=42)
reg.add(599, "Super Speed Motor", ItemType.POCKET, hard_idx=43)
reg.add(600, "Ultra Speed Motor", ItemType.POCKET, hard_idx=44)
reg.add(601, "Balanced Motor", ItemType.POCKET, hard_idx=45)
reg.add(602, "Balanced Motor Plus", ItemType.POCKET, hard_idx=46)
reg.add(603, "Extra Balanced Motor", ItemType.POCKET, hard_idx=47)
reg.add(604, "Super Balanced Motor", ItemType.POCKET, hard_idx=48)
reg.add(605, "Ultra Balanced Motor", ItemType.POCKET, hard_idx=49)
reg.add(606, "High Torque Motor", ItemType.POCKET, hard_idx=50)
reg.add(607, "High Torque Motor 2.0", ItemType.POCKET, hard_idx=51)
reg.add(608, "Godspeed Motor", ItemType.POCKET, hard_idx=52)
reg.add(609, "Godspeed Motor Mark II", ItemType.POCKET, hard_idx=53)
reg.add(610, "Slick Tires", ItemType.POCKET, hard_idx=54)
reg.add(611, "Slick Tires Plus", ItemType.POCKET, hard_idx=55)
reg.add(612, "Extra Slick Tires", ItemType.POCKET, hard_idx=56)
reg.add(613, "Super Slick Tires", ItemType.POCKET, hard_idx=57)
reg.add(614, "Ultra Slick Tires", ItemType.POCKET, hard_idx=58)
reg.add(615, "Soft Tires", ItemType.POCKET, hard_idx=59)
reg.add(616, "Soft Tires Plus", ItemType.POCKET, hard_idx=60)
reg.add(617, "Extra Soft Tires", ItemType.POCKET, hard_idx=61)
reg.add(618, "Super Soft Tires", ItemType.POCKET, hard_idx=62)
reg.add(619, "Ultra Soft Tires", ItemType.POCKET, hard_idx=63)
reg.add(620, "Spiked Tires", ItemType.POCKET, hard_idx=64)
reg.add(621, "Spiked Tires Plus", ItemType.POCKET, hard_idx=65)
reg.add(622, "Extra Spiked Tires", ItemType.POCKET, hard_idx=66)
reg.add(623, "Super Spiked Tires", ItemType.POCKET, hard_idx=67)
reg.add(624, "Ultra Spiked Tires", ItemType.POCKET, hard_idx=68)
reg.add(625, "Low Profile Tires", ItemType.POCKET, hard_idx=69)
reg.add(626, "Low Profile Tires Plus", ItemType.POCKET, hard_idx=70)
reg.add(627, "Extra Low Profile Tires", ItemType.POCKET, hard_idx=71)
reg.add(628, "Super Low Profile Tires", ItemType.POCKET, hard_idx=72)
reg.add(629, "Ultra Low Profile Tires", ItemType.POCKET, hard_idx=73)
reg.add(630, "Slim Tires", ItemType.POCKET, hard_idx=74)
reg.add(631, "Slim Tires Plus", ItemType.POCKET, hard_idx=75)
reg.add(632, "Extra Slim Tires", ItemType.POCKET, hard_idx=76)
reg.add(633, "Super Slim Tires", ItemType.POCKET, hard_idx=77)
reg.add(634, "Ultra Slim Tires", ItemType.POCKET, hard_idx=78)
reg.add(635, "Power Gears", ItemType.POCKET, hard_idx=79)
reg.add(636, "Power Gears Plus", ItemType.POCKET, hard_idx=80)
reg.add(637, "Extra Power Gears", ItemType.POCKET, hard_idx=81)
reg.add(638, "Super Power Gears", ItemType.POCKET, hard_idx=82)
reg.add(639, "Ultra Power Gears", ItemType.POCKET, hard_idx=83)
reg.add(640, "Balanced Gears", ItemType.POCKET, hard_idx=84)
reg.add(641, "Balanced Gears Plus", ItemType.POCKET, hard_idx=85)
reg.add(642, "Extra Balanced Gears", ItemType.POCKET, hard_idx=86)
reg.add(643, "Super Balanced Gears", ItemType.POCKET, hard_idx=87)
reg.add(644, "Ultra Balanced Gears", ItemType.POCKET, hard_idx=88)
reg.add(645, "Regular Gears", ItemType.POCKET, hard_idx=89)
reg.add(646, "Regular Gears Plus", ItemType.POCKET, hard_idx=90)
reg.add(647, "Extra Regular Gears", ItemType.POCKET, hard_idx=91)
reg.add(648, "Super Regular Gears", ItemType.POCKET, hard_idx=92)
reg.add(649, "Ultra Regular Gears", ItemType.POCKET, hard_idx=93)
reg.add(650, "Boost Gears", ItemType.POCKET, hard_idx=94)
reg.add(651, "Boost Gears Plus", ItemType.POCKET, hard_idx=95)
reg.add(652, "Extra Boost Gears", ItemType.POCKET, hard_idx=96)
reg.add(653, "Super Boost Gears", ItemType.POCKET, hard_idx=97)
reg.add(654, "Ultra Boost Gears", ItemType.POCKET, hard_idx=98)
reg.add(945, "Godspeed Gears", ItemType.POCKET, hard_idx=99)
reg.add(946, "Godspeed Gears Plus", ItemType.POCKET, hard_idx=100)
reg.add(947, "Extra Godspeed Gears", ItemType.POCKET, hard_idx=101)
reg.add(948, "Super Godspeed Gears", ItemType.POCKET, hard_idx=102)
reg.add(949, "Ultra Godspeed Gears", ItemType.POCKET, hard_idx=103)
reg.add(941, "High Capacity Battery", ItemType.POCKET, hard_idx=104)
reg.add(942, "High Speed Battery", ItemType.POCKET, hard_idx=105)
reg.add(944, "Regular Battery", ItemType.POCKET, hard_idx=106)
reg.add(993, "Side Stabilizer", ItemType.POCKET, hard_idx=107)
reg.add(994, "Side Stabilizer 2.0", ItemType.POCKET, hard_idx=108)
reg.add(995, "Side Stabilizer 3.0", ItemType.POCKET, hard_idx=109)
reg.add(999, "Light Suspension", ItemType.POCKET, hard_idx=110)
reg.add(1000, "Medium Suspension", ItemType.POCKET, hard_idx=111)
reg.add(1001, "Heavy Suspension", ItemType.POCKET, hard_idx=112)

# Item crafting
reg.add(454, "Iron", ItemType.CRAFT, hard_idx=0)
reg.add(455, "Lead Ingot", ItemType.CRAFT, hard_idx=1)
reg.add(456, "Screw", ItemType.CRAFT, hard_idx=2)
reg.add(457, "Spring", ItemType.CRAFT, hard_idx=3)
reg.add(458, "Chain", ItemType.CRAFT, hard_idx=4)
reg.add(459, "Quality Iron", ItemType.CRAFT, hard_idx=5)
reg.add(460, "Steel", ItemType.CRAFT, hard_idx=6)
reg.add(461, "Quality Screw", ItemType.CRAFT, hard_idx=7)
reg.add(462, "Black Metal Powder", ItemType.CRAFT, hard_idx=8)
reg.add(463, "White Metal Powder", ItemType.CRAFT, hard_idx=9)
reg.add(464, "Silver Metal Powder", ItemType.CRAFT, hard_idx=10)
reg.add(465, "Gold Metal Powder", ItemType.CRAFT, hard_idx=11)
reg.add(466, "Shape Memory Alloy", ItemType.CRAFT, hard_idx=12)
reg.add(467, "Silver Ingot", ItemType.CRAFT, hard_idx=13)
reg.add(468, "Gold Ingot", ItemType.CRAFT, hard_idx=14)
reg.add(470, "Grinding Stone", ItemType.CRAFT, hard_idx=15)
reg.add(471, "Magnet", ItemType.CRAFT, hard_idx=16)
reg.add(472, "Volcanic Rock", ItemType.CRAFT, hard_idx=17)
reg.add(473, "Glass", ItemType.CRAFT, hard_idx=18)
reg.add(474, "Obsidian", ItemType.CRAFT, hard_idx=19)
reg.add(475, "Amber", ItemType.CRAFT, hard_idx=20)
reg.add(476, "Fluorite", ItemType.CRAFT, hard_idx=21)
reg.add(477, "Tourmaline", ItemType.CRAFT, hard_idx=22)
reg.add(478, "Crystal", ItemType.CRAFT, hard_idx=23)
reg.add(479, "Emerald", ItemType.CRAFT, hard_idx=24)
reg.add(480, "Pearl", ItemType.CRAFT, hard_idx=25)
reg.add(481, "Ruby", ItemType.CRAFT, hard_idx=26)
reg.add(482, "Diamond", ItemType.CRAFT, hard_idx=27)
reg.add(483, "Rainbow Shard", ItemType.CRAFT, hard_idx=28)
reg.add(484, "Mystery Stone", ItemType.CRAFT, hard_idx=29)
reg.add(485, "Iron Gear", ItemType.CRAFT, hard_idx=30)
reg.add(486, "IC Chip", ItemType.CRAFT, hard_idx=31)
reg.add(487, "Printed Circuit Board", ItemType.CRAFT, hard_idx=32)
reg.add(488, "High Performance PCB", ItemType.CRAFT, hard_idx=33)
reg.add(489, "High-Voltage Battery Prototype", ItemType.CRAFT, hard_idx=34)
reg.add(490, "Gravity Converter Test Device", ItemType.CRAFT, hard_idx=35)
reg.add(491, "Plastic", ItemType.CRAFT, hard_idx=36)
reg.add(492, "Rubber", ItemType.CRAFT, hard_idx=37)
reg.add(493, "Reinforced Plastic", ItemType.CRAFT, hard_idx=38)
reg.add(494, "Petroleum Coke", ItemType.CRAFT, hard_idx=39)
reg.add(495, "Synthetic Fiber", ItemType.CRAFT, hard_idx=40)
reg.add(496, "Dry Branch", ItemType.CRAFT, hard_idx=41)
reg.add(497, "Carved Wooden Bear", ItemType.CRAFT, hard_idx=42)
reg.add(498, "Timber", ItemType.CRAFT, hard_idx=43)
reg.add(499, "Driftwood", ItemType.CRAFT, hard_idx=44)
reg.add(500, "Carbon Fiber", ItemType.CRAFT, hard_idx=45)
reg.add(501, "Sturdy Wood", ItemType.CRAFT, hard_idx=46)
reg.add(502, "Ash Wood", ItemType.CRAFT, hard_idx=47)
reg.add(503, "Sacred Leaves", ItemType.CRAFT, hard_idx=48)
reg.add(504, "Sacred Wood", ItemType.CRAFT, hard_idx=49)
reg.add(505, "Yew Branch", ItemType.CRAFT, hard_idx=50)
reg.add(506, "Animal Skin", ItemType.CRAFT, hard_idx=51)
reg.add(507, "Pristine Skin", ItemType.CRAFT, hard_idx=52)
reg.add(508, "Quality Leather", ItemType.CRAFT, hard_idx=53)
reg.add(509, "Bear Skin", ItemType.CRAFT, hard_idx=54)
reg.add(510, "Thoroughbred Mane", ItemType.CRAFT, hard_idx=55)
reg.add(511, "Wild Beast Skin", ItemType.CRAFT, hard_idx=56)
reg.add(512, "Divine Beast Skin", ItemType.CRAFT, hard_idx=57)
reg.add(513, "Sturdy Thread", ItemType.CRAFT, hard_idx=58)
reg.add(514, "Linen Cloth", ItemType.CRAFT, hard_idx=59)
reg.add(515, "Indian Cotton Cloth", ItemType.CRAFT, hard_idx=60)
reg.add(516, "Wool", ItemType.CRAFT, hard_idx=61)
reg.add(517, "Silk Cloth", ItemType.CRAFT, hard_idx=62)
reg.add(518, "Cashmere Cloth", ItemType.CRAFT, hard_idx=63)
reg.add(519, "Rainbow Textile", ItemType.CRAFT, hard_idx=64)
reg.add(520, "Firework Shell", ItemType.CRAFT, hard_idx=65)
reg.add(521, "Gunpowder", ItemType.CRAFT, hard_idx=66)
reg.add(522, "Enhanced Gunpowder", ItemType.CRAFT, hard_idx=67)
reg.add(523, "Explosive", ItemType.CRAFT, hard_idx=68)
reg.add(524, "Military Explosive", ItemType.CRAFT, hard_idx=69)
reg.add(525, "Straw Effigy", ItemType.CRAFT, hard_idx=70)
reg.add(526, "Happy Doll", ItemType.CRAFT, hard_idx=71)
reg.add(528, "Jet Black Belt", ItemType.CRAFT, hard_idx=72)
reg.add(529, "Cursed Handcuffs", ItemType.CRAFT, hard_idx=73)
reg.add(530, "Water God Stone", ItemType.CRAFT, hard_idx=74)
reg.add(531, "Flint Stone", ItemType.CRAFT, hard_idx=75)
reg.add(532, "Bloodied Cloth", ItemType.CRAFT, hard_idx=76)
reg.add(533, "Golden Seal", ItemType.CRAFT, hard_idx=77)
reg.add(534, "Demon Face Stone", ItemType.CRAFT, hard_idx=78)
reg.add(535, "Torn Sleeve Surcoat", ItemType.CRAFT, hard_idx=79)
reg.add(536, "Great Serpent Skin", ItemType.CRAFT, hard_idx=80)
reg.add(537, "Phoenix Feather", ItemType.CRAFT, hard_idx=81)
reg.add(538, "Provincial Dojo Certificate", ItemType.CRAFT, hard_idx=82)
reg.add(539, "Snakeskin Eyepatch", ItemType.CRAFT, hard_idx=83)
reg.add(540, "Primeval Spirit Stone", ItemType.CRAFT, hard_idx=84)
reg.add(541, "Crimson Bead", ItemType.CRAFT, hard_idx=85)
reg.add(542, "Baiken's Chain", ItemType.CRAFT, hard_idx=86)
reg.add(543, "Shishido's Sickle", ItemType.CRAFT, hard_idx=87)
reg.add(544, "Swordmaster's Oar", ItemType.CRAFT, hard_idx=88)
reg.add(545, "Golden Medicine Case", ItemType.CRAFT, hard_idx=89)
reg.add(546, "Tattered Surcoat", ItemType.CRAFT, hard_idx=90)
reg.add(547, "Dragon Tear", ItemType.CRAFT, hard_idx=91)
reg.add(548, "Eye of the Dragon", ItemType.CRAFT, hard_idx=92)
reg.add(549, "Godslayer Charm", ItemType.CRAFT, hard_idx=93)
reg.add(550, "Dragon Whisker", ItemType.CRAFT, hard_idx=94)
reg.add(551, "Dragon Fang", ItemType.CRAFT, hard_idx=95)

# Now -- restaurant/bar menus!  These can be added to your inventory and
# consumed outside of combat for a health bonus, but they're not acquireable
# legitimately.  Note that the alcohols in here do *not* make you
# intoxicated.  Using these will also cause the word "Dummy" to appear
# briefly over the icon, as an indication that these are just dummy items
# used for the restaurant menus to work properly.

# Bars (Shot Bar STIJL, Vincent, Shellac, Earth Angel)
# The bars have various combinations of these.  Note that the bars at Maharaja,
# Karaoke places, and the drinks menu from restaurants which offer separate
# drink menus are separate.
reg.add(109, "Yamazaki 12 Years Old", ItemType.MENU)
reg.add(668, "Yamazaki 18 Years Old", ItemType.MENU)
reg.add(669, "Suntory Old Whisky", ItemType.MENU)
reg.add(670, "The Macallan 12 Years Old", ItemType.MENU)
reg.add(671, "Glenfiddich 12 Years Old", ItemType.MENU)
reg.add(672, "Bowmore 12 Years Old", ItemType.MENU)
reg.add(673, "Ballantine's 12 Years Old", ItemType.MENU)
reg.add(674, "Laphroaig 10 Years Old", ItemType.MENU)
reg.add(675, "Malt's the Draft (menu at bars)", ItemType.MENU)
reg.add(1004, "Courvoisier XO", ItemType.MENU)
reg.add(1138, "Suntory Rum Gold", ItemType.MENU)
reg.add(676, "Suntory Brandy V.S.O.P", ItemType.MENU)
reg.add(1135, "Kyogetsu Green", ItemType.MENU)
reg.add(1136, "Beefeater", ItemType.MENU)
reg.add(1137, "Kakubin (menu)", ItemType.MENU)
reg.add(1077, "Suntory Kuromaru Shochu", ItemType.MENU)

# Cafe Alps
reg.add(98, "Blended Coffee", ItemType.MENU)
reg.add(99, "Blue Mountain", ItemType.MENU)
reg.add(100, "Mocha", ItemType.MENU)
reg.add(101, "Earl Grey Tea", ItemType.MENU)
reg.add(102, "Strawberry Parfait", ItemType.MENU)
reg.add(103, "Chocolate Parfait", ItemType.MENU)
reg.add(104, "Cake Set", ItemType.MENU)
reg.add(105, "Toast Set", ItemType.MENU)
reg.add(106, "Sandwich Set", ItemType.MENU)
reg.add(107, "Original Beef Curry", ItemType.MENU)

# Gindaco Highball Sakaba
reg.add(1014, "Malt's the Draft (Gindaco Highball Sakaba)", ItemType.MENU)
reg.add(772, "The Kaku Highball", ItemType.MENU)
reg.add(773, "Yamazaki Highball", ItemType.MENU)
reg.add(775, "Fresh Grapefruit Juice Highball", ItemType.MENU)
reg.add(777, "Oolong Tea (Gindaco Highball Sakaba)", ItemType.MENU)
reg.add(778, "Absolutely Tasty!! Takoyaki", ItemType.MENU)
reg.add(779, "Cheese and Spicy Fish Roe", ItemType.MENU)
reg.add(780, "Welsh Onion Takoyaki", ItemType.MENU)
reg.add(783, "Avocado and Yuzu Pepper", ItemType.MENU)
reg.add(784, "Sauce Yakisoba", ItemType.MENU)

# Smile Burger (To Go)
reg.add(785, "Smile Burger Set", ItemType.ITEM)
reg.add(786, "Smile Cheeseburger Set", ItemType.ITEM)
reg.add(787, "Teriyaki Smile Burger Set", ItemType.ITEM)
reg.add(788, "King Smile Burger Set", ItemType.ITEM)
reg.add(789, "Tuna Burger Set", ItemType.ITEM)
reg.add(790, "Stewed Burger Set", ItemType.ITEM)
reg.add(791, "Smile Shake", ItemType.ITEM)

# Smile Burger (For Here)
reg.add(793, "Smile Burger Set (dine in)", ItemType.MENU)
reg.add(794, "Smile Cheeseburger Set (dine in)", ItemType.MENU)
reg.add(795, "Teriyaki Smile Burger Set (dine in)", ItemType.MENU)
reg.add(796, "King Smile Burger Set (dine in)", ItemType.MENU)
reg.add(797, "Tuna Burger Set (dine in)", ItemType.MENU)
reg.add(798, "Stewed Burger Set (dine in)", ItemType.MENU)
reg.add(799, "Smile Shake (dine in)", ItemType.MENU)

# Kanrai
reg.add(807, "Salted Tongue", ItemType.MENU)
reg.add(808, "Grade A Salted Tongue", ItemType.MENU)
reg.add(809, "Kalbi", ItemType.MENU)
reg.add(810, "Grade A Kalbi", ItemType.MENU)
reg.add(811, "Sirloin", ItemType.MENU)
reg.add(812, "Grade A Sirloin", ItemType.MENU)
reg.add(813, "Harami", ItemType.MENU)
reg.add(814, "Grade A Harami", ItemType.MENU)
reg.add(815, "Tripe BBQ", ItemType.MENU)
reg.add(816, "Seafood Platter", ItemType.MENU)
reg.add(817, "Kimchi Combo", ItemType.MENU)
reg.add(818, "Stone Cooked Bibimbap", ItemType.MENU)
reg.add(819, "Spicy Beef Soup", ItemType.MENU)

# Sushi Gin
reg.add(821, "Tamago", ItemType.MENU)
reg.add(822, "Maguro", ItemType.MENU)
reg.add(823, "Ama-Ebi", ItemType.MENU)
reg.add(824, "Engawa", ItemType.MENU)
reg.add(825, "Seki Mackerel", ItemType.MENU)
reg.add(826, "Namatako", ItemType.MENU)
reg.add(827, "Hirame", ItemType.MENU)
reg.add(828, "Shima-Aji", ItemType.MENU)
reg.add(829, "Kinmedai", ItemType.MENU)
reg.add(830, "Ikura", ItemType.MENU)
reg.add(831, "Akagai", ItemType.MENU)
reg.add(832, "Otoro", ItemType.MENU)
reg.add(833, "Awabi", ItemType.MENU)
reg.add(834, "Uni", ItemType.MENU)

# Tsuruhashi Fugetsu
reg.add(862, "Pork Okonomiyaki", ItemType.MENU)
reg.add(863, "Shrimp Okonomiyaki", ItemType.MENU)
reg.add(864, "Shrimp & Squid Okonomiyaki", ItemType.MENU)
reg.add(865, "Beef & Welsh Onion Okonomiyaki", ItemType.MENU)
reg.add(866, "Potato, Mochi & Cheese Okonomiyaki", ItemType.MENU)
reg.add(867, "Pork Kimchi Okonomiyaki", ItemType.MENU)
reg.add(868, "Fugetsu-yaki", ItemType.MENU)
reg.add(869, "Pork Modanyaki", ItemType.MENU)
reg.add(870, "Shrimp Modanyaki", ItemType.MENU)
reg.add(871, "Fugetsu-yaki (Modan)", ItemType.MENU)
reg.add(872, "Tonpei-yaki", ItemType.MENU)
reg.add(873, "Yakisoba (Tsuruhashi Fugetsu)", ItemType.MENU)

# Zuboraya
reg.add(874, "Tecchiri Nabe", ItemType.MENU)
reg.add(875, "Deluxe Tecchiri Nabe", ItemType.MENU)
reg.add(876, "Tessa", ItemType.MENU)
reg.add(877, "Fugu Tempura", ItemType.MENU)
reg.add(878, "Deep Fried Fugu", ItemType.MENU)
reg.add(1016, "Fugu Cassolette Meal", ItemType.MENU)
reg.add(1017, "Fugu Set", ItemType.MENU)
reg.add(1018, "Grilled Fugu Set", ItemType.MENU)
reg.add(1019, "Fugu Three-Ways Set", ItemType.MENU)
reg.add(883, "Torafugu \"Benten\" Course", ItemType.MENU)
reg.add(884, "Torafugu \"Daikoku\" Course", ItemType.MENU)
reg.add(885, "Torafugu \"Ebisu\" Course", ItemType.MENU)
reg.add(886, "Torafugu \"Hotei\" Course", ItemType.MENU)

# Kinryu Ramen
reg.add(887, "Ramen", ItemType.MENU)
reg.add(888, "Chasu Ramen (Kinryu Ramen)", ItemType.MENU)

# Komian
reg.add(889, "Soup of the Day", ItemType.MENU)
reg.add(890, "Sashimi Platter", ItemType.MENU)
reg.add(891, "\"Hokkori\" Kaiseki", ItemType.MENU)
reg.add(892, "\"Hannari\" Kaiseki", ItemType.MENU)
reg.add(893, "Snow Crab Course", ItemType.MENU)
reg.add(894, "Matsutake Set", ItemType.MENU)
reg.add(895, "Grilled Marbled Waygu", ItemType.MENU)

# Kushikatsu Daruma
reg.add(896, "Original Fried Pork Skewers", ItemType.MENU)
reg.add(897, "Quail Eggs", ItemType.MENU)
reg.add(898, "Squid Tentacles", ItemType.MENU)
reg.add(899, "Asparagus", ItemType.MENU)
reg.add(900, "Onion", ItemType.MENU)
reg.add(901, "Bamboo Shoot", ItemType.MENU)
reg.add(902, "Octopus (Kushikatsu Daruma)", ItemType.MENU)
reg.add(903, "Whiting", ItemType.MENU)
reg.add(904, "Lotus Root", ItemType.MENU)
reg.add(905, "White Welsh Onion", ItemType.MENU)
reg.add(906, "Tsukune", ItemType.MENU)
reg.add(907, "Hearty Pumpkin", ItemType.MENU)
reg.add(908, "Garlic Chicken", ItemType.MENU)
reg.add(909, "Wild Shrimp", ItemType.MENU)
reg.add(910, "Scallop", ItemType.MENU)
reg.add(914, "Sotenbori Set", ItemType.MENU)
reg.add(915, "Hoganji Set", ItemType.MENU)

# Kani Douraku
reg.add(916, "Crab Nabe", ItemType.MENU)
reg.add(917, "Crab Shabushabu", ItemType.MENU)
reg.add(918, "Crab Amiyaki (2 Kinds)", ItemType.MENU)
reg.add(919, "Raw Crab Sushi", ItemType.MENU)
reg.add(920, "Red King Crab Sushi", ItemType.MENU)
reg.add(921, "Crab Sushi Platter", ItemType.MENU)
reg.add(922, "Crab Nabe \"Shiosai\" Course", ItemType.MENU)
reg.add(923, "Crab Nabe \"Yuzuru\" Course", ItemType.MENU)
reg.add(924, "Crab Nabe \"Maihime\" Course", ItemType.MENU)
reg.add(925, "Crab Kaiseki \"Seifuu\" Course", ItemType.MENU)
reg.add(926, "Crab Kaiseki \"Hakutsuyu\" Course", ItemType.MENU)
reg.add(927, "Crab Kaiseki \"Shoto\"", ItemType.MENU)
reg.add(928, "Crab Kaiseki \"Jusanya\"", ItemType.MENU)

# Ganko Sushi
reg.add(929, "Fatty Tuna Tenmi Sushi", ItemType.MENU)
reg.add(930, "Fatty Tuna Sushi", ItemType.MENU)
reg.add(931, "Bluefin Tuna Sushi Platter", ItemType.MENU)
reg.add(932, "Sushi Set (Ganko Sushi)", ItemType.MENU)
reg.add(933, "Choice Sushi Set", ItemType.MENU)
reg.add(934, "Sushi Feast", ItemType.MENU)
reg.add(935, "Seasonal Sashimi & Sushi Feast", ItemType.MENU)
reg.add(936, "Sushi Kaiseki Chitose Course \"Moon\"", ItemType.MENU)
reg.add(1020, "Sushi Kaiseki Chitose Course \"Snow\"", ItemType.MENU)
reg.add(937, "Kaiseki Nishiki Course", ItemType.MENU)

# Akaushimaru (Taihei Boulevard + Tenkaichi Street)
reg.add(950, "Beef Bowl (Standard)", ItemType.MENU)
reg.add(951, "Beef Bowl (Large)", ItemType.MENU)
reg.add(952, "Beef Bowl (Extra Large)", ItemType.MENU)

# Fuji Soba
reg.add(1021, "Soba in Hot Broth", ItemType.MENU)
reg.add(1022, "Chilled Soba", ItemType.MENU)
reg.add(1023, "Chilled Tanuki Soba", ItemType.MENU)
reg.add(1024, "Chilled Kitsune Soba", ItemType.MENU)
reg.add(1025, "Egg & Tempura Soba", ItemType.MENU)
reg.add(1026, "Special Fuji Soba", ItemType.MENU)
reg.add(1027, "Yuzu Chicken & Spinach Soba", ItemType.MENU)
reg.add(1028, "Fried Pork Cutlet Bowl", ItemType.MENU)
reg.add(1029, "Curry & Rice", ItemType.MENU)
reg.add(1030, "Pickled Ginger Soba", ItemType.MENU)

# Yoronotaki (Kamurocho + Sotenbori)
reg.add(1031, "Draft Beer (Yoronotaki)", ItemType.MENU)
reg.add(1032, "Oolong Tea (Yoronotaki)", ItemType.MENU)
reg.add(1033, "Lemon Sour", ItemType.MENU)
reg.add(1034, "Grape Sour", ItemType.MENU)
reg.add(1035, "Fresh Grapefruit Sour", ItemType.MENU)
reg.add(1036, "Bakuhai", ItemType.MENU)
reg.add(1037, "Yoro Shochu Highball", ItemType.MENU)
reg.add(1038, "Gyokuru Green Tea Cocktail", ItemType.MENU)
reg.add(1039, "Kaku Highball", ItemType.MENU)
reg.add(1040, "Umeshu on the Rocks", ItemType.MENU)
reg.add(1041, "Cassis Oolong", ItemType.MENU)
reg.add(1042, "Mojito", ItemType.MENU)
reg.add(1043, "Yamazaki", ItemType.MENU)
reg.add(1044, "Value Sashimi Platter 7 pcs.", ItemType.MENU)
reg.add(1045, "Sashimi Platter 3 pcs.", ItemType.MENU)
reg.add(1046, "Seared Vinegar Mackerel", ItemType.MENU)
reg.add(1047, "Kotchori Salad", ItemType.MENU)
reg.add(1048, "Edamame (Yoronotaki)", ItemType.MENU)
reg.add(1049, "Skewer Platter", ItemType.MENU)
reg.add(1050, "Japanese Chicken Skewer", ItemType.MENU)
reg.add(1051, "Smelt Fish with Roe", ItemType.MENU)
reg.add(1052, "Fried Squid with Nori", ItemType.MENU)
reg.add(1053, "Salted Yakisoba", ItemType.MENU)
reg.add(1054, "Juicy Mince Cutlet", ItemType.MENU)
reg.add(1055, "Stir-Fried Bean Sprouts", ItemType.MENU)
reg.add(1056, "Mango & Peach Sherbert", ItemType.MENU)

# Ringer Hut Kamurocho
reg.add(1060, "Nagasaki Champon", ItemType.MENU)
reg.add(1061, "Vegetable Champon", ItemType.MENU)
reg.add(1062, "Spicy Champon", ItemType.MENU)
reg.add(1063, "Light Champon", ItemType.MENU)
reg.add(1064, "Nagasaki Saraudon", ItemType.MENU)
reg.add(1065, "Vegetable Saraudon", ItemType.MENU)
reg.add(1066, "Thick Saraudon", ItemType.MENU)
reg.add(1067, "Light Saraudon", ItemType.MENU)
reg.add(1068, "Gyoza 5pcs.", ItemType.MENU)
reg.add(1069, "Deep Fried Chicken", ItemType.MENU)
reg.add(1070, "Nagasaki Salad", ItemType.MENU)

# Tengokuken
reg.add(1071, "Shoyu Ramen", ItemType.MENU)
reg.add(1072, "Negi Ramen", ItemType.MENU)
reg.add(803, "Chasu Ramen (Tengokuken)", ItemType.MENU)
reg.add(1073, "Negi Chasu Ramen", ItemType.MENU)

# Maharaja (Kamurocho + Sotenbori)
reg.add(1111, "Wine", ItemType.MENU)
reg.add(1112, "Draft Beer (Maharaja)", ItemType.MENU)
reg.add(1113, "Champagne (Maharaja)", ItemType.MENU)
reg.add(1114, "Cassis & Orange", ItemType.MENU)
reg.add(1115, "Gin & Lime", ItemType.MENU)

# Karaoke Bars (Heroine + Utahime)
# Heroine does not have Yakisoba, Utahime does not have Omelet.
reg.add(1117, "Omelet", ItemType.MENU)
reg.add(1118, "Edamame (Karaoke bars)", ItemType.MENU)
reg.add(1119, "Fried Chicken", ItemType.MENU)
reg.add(1120, "Pickles", ItemType.MENU)
reg.add(1121, "Yakisoba (Utahime Karaoke)", ItemType.MENU)
reg.add(1122, "Whisky", ItemType.MENU)
reg.add(1123, "Draft Beer (Karaoke bars)", ItemType.MENU)
reg.add(1124, "Oolong Tea (Karaoke bars)", ItemType.MENU)

# Unattached to any restaurant, apparently, but clearly leftover menu items
reg.add(820, "Grilled Garlic", ItemType.MENU)
reg.add(1015, "Teriyaki and Egg", ItemType.MENU)

# Weird no-icon consumables.  These should maybe be labelled JUNK just 'cause
# they're hard to notice in the inventory on account of not having an icon,
# but they *can* be consumed outside of combat for health boosts.  The alcohols
# in here do *not* induce drunkenness.  Labelling them as MENU since they
# follow the same Item Box rules as the MENU ones (ie: max qty of 1 in the box)
reg.add(188, "Champagne Tower (no icon)", ItemType.MENU)
reg.add(189, "Gold Champagne (no icon)", ItemType.MENU)
reg.add(190, "Rosé Champagne (no icon)", ItemType.MENU)
reg.add(191, "Black Champagne (no icon)", ItemType.MENU)
reg.add(192, "White Champagne (no icon)", ItemType.MENU)
reg.add(193, "Yamazaki 12 Years Old (no icon)", ItemType.MENU)
reg.add(194, "Beer (no icon)", ItemType.MENU)
reg.add(195, "Cassis & Orange (no icon)", ItemType.MENU)
reg.add(196, "Orange Juice (no icon)", ItemType.MENU)
reg.add(197, "Kyogetsu Green (no icon)", ItemType.MENU)
reg.add(198, "Gacha Drink (no icon)", ItemType.MENU)
reg.add(199, "Drink 11 (no icon)", ItemType.MENU)
reg.add(200, "Drink 12 (no icon)", ItemType.MENU)
reg.add(201, "Drink 13 (no icon)", ItemType.MENU)
reg.add(202, "Drink 14 (no icon)", ItemType.MENU)
reg.add(203, "Drink 15 (no icon)", ItemType.MENU)
reg.add(204, "Fruit Platter (no icon)", ItemType.MENU)
reg.add(205, "Carbonara (no icon)", ItemType.MENU)
reg.add(206, "Chicken Karaage (no icon)", ItemType.MENU)
reg.add(207, "Vegetable Sticks (no icon)", ItemType.MENU)
reg.add(208, "Dried Ray Fin (no icon)", ItemType.MENU)
reg.add(209, "Takoyaki (no icon)", ItemType.MENU)
reg.add(210, "French Fries (no icon)", ItemType.MENU)
reg.add(211, "Pasta Sticks (no icon)", ItemType.MENU)
reg.add(212, "Edamame (no icon)", ItemType.MENU)
reg.add(213, "Mixed Nuts (no icon)", ItemType.MENU)
reg.add(214, "Ice Cream (no icon)", ItemType.MENU)
reg.add(215, "Chocolate Sticks (no icon)", ItemType.MENU)
reg.add(216, "Food 12 (no icon)", ItemType.MENU)
reg.add(217, "Food 13 (no icon)", ItemType.MENU)
reg.add(218, "Food 14 (no icon)", ItemType.MENU)
reg.add(219, "Food 15 (no icon)", ItemType.MENU)

# "Junk" Valuables!  Stuff which probably (or in some cases definitely)
# belongs in the Valuables section but actually makes no sense whatsoever
# to add there. Including notes for all of these

# Walkman is non-functional in the US version -- it won't show up at all
# even if you put it in the "valuables" section.  Leaving it here instead
# of in JUNK just 'cause maybe it would work in other localizations?  No
# idea what the proper index would be, though.  This *will* show up (with
# an icon) if you stick it into your regular inventory, but of course
# it doesn't actually do anything in there.
reg.add(1147, "Walkman", ItemType.VALJUNK)

# These seem like they could be in the Valuables section, but don't seem
# to do anything useful in there.  You can put them in your main inventory
# (but not do anything with them), but if they're transferred to the Item
# Box and then brought *back* to the inventory, they'll just disappear.
reg.add(163, "Mahjong Sticks", ItemType.VALJUNK)
reg.add(167, "Completion List", ItemType.VALJUNK)

# *these* behave similar to Mahjong Sticks and Completion List, except that
# once they're in the Item Box, merely selecting them in the list causes
# the game to crash.
reg.add(174, "Money", ItemType.VALJUNK)
reg.add(175, "Experience Points", ItemType.VALJUNK)

# House Darts behave just like Money + Experience Points when in the Item
# Box.  They also never actually show up in the Valuables list in the real
# game, so we wouldn't know what index to put 'em in.
reg.add(169, "House Darts", ItemType.VALJUNK)

# Junk Items
reg.add(1, "(locked item slot)", ItemType.JUNK)
reg.add(108, "Test (bowl of food)", ItemType.JUNK, max_in_box=1) # Once put in Item Box, can never be taken back out!
# These Cash-In/Convert items do things when moved from the Item Box to your inventory.
# The Cash In Betting Pts ones give you x100 yen, the non-Betting-Pts Cash In ones
# give you x1 yen, and the Convert ones start up a "Bet" counter.  Don't bother with
# 'em, anyway.
reg.add(115, "Cash In 1,000 Betting Pts.", ItemType.JUNK)
reg.add(116, "Cash In 10,000 Betting Pts.", ItemType.JUNK)
reg.add(117, "Convert 1,000 Mon to Betting Pts.", ItemType.JUNK)
reg.add(118, "Convert 1 Ryo to Betting Pts.", ItemType.JUNK)
reg.add(119, "Cash in 1,000 Pts.", ItemType.JUNK)
reg.add(120, "Cash in 10,000 Pts.", ItemType.JUNK)
reg.add(137, "Test Katana", ItemType.JUNK, max_in_box=1) # nonfunctional!
reg.add(139, "Test Tonfa", ItemType.JUNK, max_in_box=1) # nonfunctional!
reg.add(140, "Test Kali Sticks", ItemType.JUNK, max_in_box=1) # nonfunctional!
reg.add(141, "Test Staff", ItemType.JUNK, max_in_box=1) # nonfunctional!
reg.add(143, "Test Nunchaku", ItemType.JUNK, max_in_box=1) # nonfunctional!
reg.add(144, "Test Bat", ItemType.JUNK, max_in_box=1) # nonfunctional!
reg.add(146, "Test Bayonet", ItemType.JUNK, max_in_box=1) # nonfunctional!
reg.add(1057, "High Payout Token", ItemType.JUNK, max_in_box=1) # for slots, which don't exist in y0
reg.add(1058, "High Win Rate Token", ItemType.JUNK, max_in_box=1) # for slots, which don't exist in y0
reg.add(1059, "Auto Token", ItemType.JUNK, max_in_box=1) # for slots, which don't exist in y0
reg.add(147, "Master Ball (non-legitimate)", ItemType.JUNK, max_in_box=1) # Can technically be used as a weapon but with 1 damage
reg.add(148, "The Hedgeball", ItemType.JUNK, max_in_box=1)

# These aren't actually usable from the inventory, so no real point to 'em
reg.add(131, "Kamurocho Fun Pack 03", ItemType.JUNK, max_in_inv=99)
reg.add(132, "Kamurocho Fun Pack 04", ItemType.JUNK, max_in_inv=99)
reg.add(133, "Kamurocho Fun Pack 05", ItemType.JUNK, max_in_inv=99)
reg.add(134, "Kamurocho Fun Pack 06", ItemType.JUNK, max_in_inv=99)
reg.add(135, "Kamurocho Fun Pack 07", ItemType.JUNK, max_in_inv=99)
reg.add(136, "Kamurocho Fun Pack 08", ItemType.JUNK, max_in_inv=99)
reg.add(982, "Dragon of Dojima Pack", ItemType.JUNK, max_in_inv=99)
reg.add(983, "Sotenbori Fun Pack", ItemType.JUNK, max_in_inv=99)
reg.add(984, "Kamurocho Fun Pack", ItemType.JUNK, max_in_inv=99)
reg.add(985, "Mad Dog of Shimano Pack", ItemType.JUNK, max_in_inv=99)
reg.add(986, "Pocket Circuit Starter Pack", ItemType.JUNK, max_in_inv=99)
reg.add(987, "Crafting Support Pack", ItemType.JUNK, max_in_inv=99)
reg.add(988, "Kamurocho Fun Pack 2", ItemType.JUNK, max_in_inv=99)
reg.add(989, "Sotenbori Fun Pack 2", ItemType.JUNK, max_in_inv=99)
reg.add(990, "Pocket Circuit Expert Pack", ItemType.JUNK, max_in_inv=99)
reg.add(991, "Super Rare Crafting Pack", ItemType.JUNK, max_in_inv=99)

# Create some potentially-useful mappings
items_by_id = {}
items_by_name = {}
for item in reg:
    items_by_id[item.item_id] = item
    if item.name.lower() in items_by_name:
        print('WARNING: {} already exists in our name mapping'.format(item.name))
    items_by_name[item.name.lower()] = item

# IDs which we know don't have items.  Honestly not sure how this info could be
# useful, except as a manual check that the "holes" in the item list above have
# all been manually looked-at.  The last item ID seems to be 1147 -- I've checked
# from 1148 through 1250 without seeing any new ones, and I can't think what
# else would be in there anyway, so I feel pretty good about that.
known_no_items = {
        17,
        20, 21,
        34, 37,
        44, 45, 46, 47, 48, 49,
        50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
        60, 61, 62, 63, 64, 65, 66,
        96, 97,
        121, 122, 123, 124, 125, 126, 127, 128, 129,
        130, 138,
        149,
        150, 151, 152, 153, 154, 155, 156, 157, 158, 159,
        160, 161, 162, 164, 166,
        176, 177, 178, 179,
        180, 181, 182, 183, 184, 185, 186, 187,
        440,
        469,
        527,
        572, 573, 574, 575, 576, 577, 578, 579,
        580, 581, 582, 583, 584, 586, 587, 588, 589,
        590,
        655, 656, 657, 658, 659,
        687, 688, 689,
        690, 691, 692, 693, 694, 695, 696, 697,
        713, 714, 715, 716, 717, 718,
        720, 723, 726, 729,
        741, 742, 743, 744, 745, 748,
        753, 754, 755, 756, 759,
        761, 763, 764, 766, 768,
        771, 774, 776,
        781, 782,
        792,
        800, 801, 802, 804, 805, 806,
        835, 836, 837, 838, 839,
        840, 841, 842, 843, 844, 845, 846, 847, 848, 849,
        850, 851, 852, 853, 854, 855, 856, 857, 858, 859,
        860, 861,
        879,
        880, 881, 882,
        911, 912, 913,
        943,
        996, 997, 998,
        1012, 1013,
        1116,
        }

# Just double-checking our known ID list
#for num in range(1, 1148):
#    if num not in known_no_items and num not in items_by_id:
#        print("WARNING: We don't know anything about item ID {}".format(num))

