# File name-Classes.py

import time
import random


# Class initialization -------------------------------------------------------------------------------------------------
class Monster:
    def __init__(self, name, type1, type2, max_health, defense, base_dmg, dodge_chance, willpower, mana, move_set,
                 item_drop, gold):
        self.name = name.title()
        self.type = type1
        self.type2 = type2, ' '
        self.mh = int(max_health)
        self.h = int(max_health)
        self.d = int(defense)
        self.temp_d = 0
        self.total_d = 0
        self.bd = int(base_dmg)
        self.temp_dmg = 0
        self.total = 0
        self.dc = int(dodge_chance)
        self.will = int(willpower)
        self.mana = int(mana)
        self.inflicted = []
        self.last_turn = []
        self.increase_dmg = []
        self.moves = move_set
        self.item_drop = item_drop
        self.type_weak = []
        self.check_type = ['fire', 'water', 'life', 'undead', 'holy', 'dark', 'trickster']
        self.gold = int(gold)
        # Opens files
        with open("txt files/items.txt", "r") as file:
            self.item_lines = file.read().split("\n")
        with open("txt files/weapons.txt", "r") as file:
            self.weapon_lines = file.read().split("\n")

    # Health section ---------------------------------------------------------------------------------------------------

    # --Health bar--
    def show_health(self):
        # text
        health_text = "{name}({type}) {inflicted}\nHealth: [{health_bar}]"

        # Length of health bar
        if self.mh > 20:
            char_limit = 20
        else:
            char_limit = self.mh

        # math
        shown_health = (self.h / self.mh) * char_limit
        left_over = ((self.mh / self.mh) * char_limit) - shown_health

        # setting up the strings
        ch1 = '/' * int(shown_health)
        ch2 = '-' * int(left_over)

        # showing the health bar
        type_n_name = ''.join(self.name).join(self.type2)
        self.type = list(self.type)
        if isinstance(self.type, tuple):
            type_ = ', '.join(self.type).strip()
        else:
            type_ = ''.join(self.type)
        if len(self.inflicted) > 1:
            status = 'status: ' + str(', '.join(self.inflicted).strip())
        elif len(self.inflicted) == 1:
            status = 'status: ' + str(self.inflicted)
        else:
            status = ''
        print(health_text.format(name=type_n_name, inflicted=status, type=type_, health_bar=(str(ch1) + str(ch2))))

    # --Healing + increase max health--
    def heal(self, amount):
        if amount + self.h >= self.mh:
            print(self.name, "Fully healed!")
            self.h = self.mh
        else:
            print(self.name, "healed", str(amount), "Health!")
            self.h += amount

    def max_increase(self, amount):
        self.mh += amount
        print(self.name, "increased their max health!")
        time.sleep(1)
        self.heal(amount)

    # Types section ----------------------------------------------------------------------------------------------------

    # --Adds weakness--
    def find_weakness(self):
        if isinstance(self.type, tuple):
            # adds all weaknesses according to the plans (see Plans.py)
            for i in range(len(self.type)):
                if self.type[i] == 'fire':
                    self.type_weak.append('water')

                elif self.type[i] == 'water':
                    self.type_weak.append('life')

                elif self.type[i] == 'life':
                    self.type_weak.extend(('dark', 'undead', 'fire'))

                elif self.type[i] == 'undead':
                    self.type_weak.extend(('fire', 'life', 'holy'))

                elif self.type[i] == 'holy':
                    self.type_weak.extend(('dark', 'fire', 'trickster'))

                elif self.type[i] == 'dark':
                    self.type_weak.extend(('holy', 'water', 'trickster'))

            # makes it so that there is no weaknesses that are the same type as its types
            for i in self.type_weak:
                if i in self.type:
                    self.type_weak.remove(i)

            # makes it so that there are no dupe weaknesses
            self.type_weak = set(self.type_weak)
            self.type_weak = list(self.type_weak)

        else:
            if self.type == 'fire':
                self.type_weak.append('water')

            elif self.type == 'water':
                self.type_weak.append('life')

            elif self.type == 'life':
                self.type_weak.extend(('dark', 'undead', 'fire'))

            elif self.type == 'undead':
                self.type_weak.extend(('fire', 'life', 'holy'))

            elif self.type == 'holy':
                self.type_weak.extend(('dark', 'fire', 'trickster'))

            elif self.type == 'dark':
                self.type_weak.extend(('holy', 'water', 'trickster'))

    # Status section ---------------------------------------------------------------------------------------------------

    # --Adds status effects--
    def activate_status(self, receive, turns):
        # adds both the effect and how many turns it lasts at its respective lists
        if receive not in self.inflicted:
            print(self.name, 'was inflicted with', receive + '!')
            end = len(self.inflicted)
            self.inflicted.insert(end, receive)

            end = len(self.last_turn)
            self.last_turn.insert(end, turns)

            end = len(self.increase_dmg)
            self.increase_dmg.insert(end, 1)

    # --Makes the status go away once turns are up--
    def inflict_status(self):
        # only runs when the length is greater than 1 to avoid error
        if len(self.inflicted) > 0:
            # checks for only number to influence both lists
            for i in range(len(self.inflicted)):
                # second thing for organization
                self.effect_type(i)
                # removes a turn
                self.last_turn[i] = self.last_turn[i] - 1
                # adds to the increasing dmg
                self.increase_dmg[i] = self.increase_dmg[i] + 1
                # if how long the effect lasts reaches 0, deletes the effect and the turn to avoid error
                if self.last_turn[i] < 1:
                    self.last_turn.pop(i)
                    self.inflicted.pop(i)
                    self.increase_dmg.pop(i)

    # --Deals damage--
    def effect_type(self, num):
        if self.inflicted[num] == 'burn' or self.inflicted[num] == 'hells inferno':
            if self.will < 15:
                print(self.name, 'feels like giving in to the flames...')
                time.sleep(1)
                ran = random.randint(1, 100)
                if ran <= 20 and self.inflicted[num] != 'hells inferno':
                    print('The fire spread further!')
                    time.sleep(1)
                    print('The underworld is reacting to', self.name + "'s despair...")
                    self.inflicted[num] = 'hells inferno'
                    self.last_turn[num] += 10
                    time.sleep(1)
                    print('The flames evolved into Hell\'s Inferno!\n'
                          '(The affected target can no longer remove the flames...)')
            elif self.inflicted[num] == 'hells inferno':
                self.raw_dmg((3 + self.increase_dmg[num]), num, 'yes', 'yes')
            else:
                self.raw_dmg(self.increase_dmg, num, 'no', 'no')

        elif self.inflicted[num] == 'freeze':
            if self.will < 15:
                print(self.name, 'might not wake up if they fall asleep...')
                time.sleep(1)
                ran = random.randint(1, 100)
                if ran <= 20:
                    self.activate_status('drowsy', 10)
                    print(self.name, 'fell asleep!')
                    time.sleep(1)
                self.raw_dmg((4 + self.increase_dmg[num]), num, 'yes', 'no')
            self.raw_dmg(5, num, 'no', 'no')

        elif self.inflicted[num] == 'poison':
            if self.will < 15:
                print(self.name, "doesn't think they can beat the poison...")
                time.sleep(1)
                self.raw_dmg(5, num, 'yes', 'no')
            else:
                self.raw_dmg(5, num, 'no', 'no')

        elif self.inflicted[num] == "bleed":
            if self.will < 15:
                print(f"{self.name} is unable to close the wound...")
                time.sleep(1)
                self.raw_dmg(2 + self.increase_dmg[num], num, "yes", "no")
            else:
                self.raw_dmg((2 + self.increase_dmg[num]), num, "no", "no")

        elif self.inflicted[num] == 'wither':
            self.raw_dmg((1 + self.increase_dmg[num]), num, 'yes', 'yes')

        elif self.inflicted[num] == 'frostbite':
            self.temp_d -= 3
            self.will -= 4
            print(self.name, 'lost some of their composure due to frostbite!')
            time.sleep(1)
            self.raw_dmg((1 + self.increase_dmg[num]), num, 'yes', 'yes')

        elif self.inflicted[num] == 'graced by the gods':
            if 'dark' in self.type or 'undead' in self.type:
                self.raw_dmg((4 + self.increase_dmg[num]), num, 'yes', 'yes')
            else:
                self.will += 5
                print(self.name + 'suddenly had the will to fight!')

        elif self.inflicted[num] == 'curse of darkness':
            if 'dark' in self.type or 'undead' in self.type:
                self.temp_dmg += int(self.d / 2)
                self.will += 5
                print(self.name, 'is filled with cursed energy!')
                time.sleep(1)
                print('Their strength and will were increased!')
            else:
                self.raw_dmg(self.increase_dmg[num], num, 'yes', 'yes')

        elif self.inflicted[num] == 'breath of the abyss':
            self.raw_dmg(self.increase_dmg[num], num, 'yes', 'yes')

            self.temp_dmg += 5
            self.temp_d += 5
            print(self.name, 'has a void forming in their soul...')
            time.sleep(1)
            print('They are starting to lose their sense of self...')
            time.sleep(1)
            print('They feel their body getting stronger!')

            if self.last_turn[num] < 2:
                time.sleep(1)
                print(self.name + '\'s soul was overcome by the abyss...')
                time.sleep(1)
                print('Their final moments are approaching...')
                self.activate_status('death counter', 21)

        elif self.inflicted[num] == 'death counter':
            print('TURNS UNTIL DEATH:', str(self.last_turn[num] - 1))
            if self.last_turn[num] < 2:
                time.sleep(1)
                print(self.name, 'was consumed by the abyss...')
                time.sleep(1)
                print('They have perished...')

        elif self.inflicted[num] == "strengthen":
            self.temp_dmg += self.increase_dmg[num]

        time.sleep(1)

    # Damage section ---------------------------------------------------------------------------------------------------

    # --For status effects--
    def raw_dmg(self, damage, position, can_die, affect_will):
        txt = '{name} took {dmg} from {inflicted}!'

        if self.h - damage < 1 and can_die == 'yes':
            self.h = 0
            print(txt.format(name=self.name, dmg=damage, inflicted=self.inflicted[position]))

        else:
            self.h -= damage
            print(txt.format(name=self.name, dmg=damage, inflicted=self.inflicted[position]))

        if affect_will == 'yes':
            self.will -= damage
            print(self.name, 'lost some of their will to fight!')

    # --For basic damage--
    def take_health(self, amount):
        self.h -= amount
        print(self.name, 'took', amount, 'damage!')
        if self.h < 1 and self.will > 100:
            print(self.name, 'held on through sheer will!')
            self.h = 2

    # --Receives from enemy--
    def receive_dmg(self, attacker, amount):
        # dodging
        dodge = random.randint(1, 100)
        if self.dc >= dodge:
            print(self.name, 'evaded the attack!')
        else:
            # type sorting
            if attacker.type in self.type_weak:
                self.take_health(int(amount * 2))
                print('The attack was super effective!')
            elif self.type in attacker.type_weak:
                self.take_health(int(amount / 2))
                print("The attack wasn't very effective...")
            else:
                self.take_health(amount)

        time.sleep(1)

    # --Reduces based on affects or increases based on affects--
    def cal_total_dmg(self, target):
        temp_d = self.temp_dmg + self.bd

        if 'strengthen' in self.inflicted:
            temp_d += int(temp_d * 0.1)

        if ('curse of darkness' in self.inflicted and 'dark' in self.type or 'curse of darkness' in self.inflicted and
                'undead' in self.type):
            temp_d += int(temp_d / 2)

        elif 'curse of darkness' in self.inflicted:
            temp_d = int(temp_d / 2)

        if 'weaken' in self.inflicted:
            temp_d -= int(temp_d * 0.1)

        if 'frostbite' in self.inflicted:
            temp_d -= int(temp_d * 0.1)

        if self.will < 15:
            temp_d -= 5

        if temp_d < 1:
            temp_d = 1

        target.receive_dmg(self, temp_d)

    # Attacks and turn control -----------------------------------------------------------------------------------------
    def enemy_move(self, target):
        move = random.choice(self.moves)

        print(f"{self.name} used {move}!")

        with open("txt files/attacks.txt", "r") as atk:
            lines = atk.read().split("\n")

        for i in range(len(lines)):
            if move == lines[i]:
                move = lines[i + 1].split("/")
                break

        if "-" in move[0]:
            self.temp_dmg = int(random.choice(move[0].split("-")))
        else:
            self.temp_dmg = int(move[0])
        self.cal_total_dmg(target)
        if not move[2] == "none":
            ran = random.randint(1, 2)
            if ran == 1:
                target.activate_status(move[2], 3)

    def reset(self):
        self.temp_d = 0
        self.temp_dmg = 0

    # Battle end-er ----------------------------------------------------------------------------------------------------
    def give_item(self):
        it = random.choice(self.item_drop.split("-"))
        return it

    def is_alive(self):
        return self.h > 1


# Class Initialization (player) ----------------------------------------------------------------------------------------
class Player(Monster):
    def __init__(self, name, type1, type2, max_health, defense, base_dmg, dodge_chance, willpower, mana, move_set,
                 item_drop, gold, weapon):
        super().__init__(name, type1, type2, max_health, defense, base_dmg, dodge_chance, willpower, mana, move_set,
                         item_drop, gold)
        self.weapon = weapon
        self.inventory = []

    # Move Sets --------------------------------------------------------------------------------------------------------
    # -- Getting Weapon Moves --
    def get_moves(self, target):
        for i in range(len(self.weapon_lines)):
            if self.weapon == self.weapon_lines[i]:
                s = self.show_moves(self.weapon_lines[i + 1], target)
                return s

    # -- Showing Moves/Player Choice --
    def show_moves(self, n, target):
        # set up
        move_set = n.split("-")
        items = []

        with open("txt files/attacks.txt", "r") as dmg:
            dmg = dmg.read().split("\n")

        if isinstance(move_set, list):
            for i in range(len(move_set)):
                for a in range(len(dmg)):
                    if move_set[i] == dmg[a]:
                        items.append(dmg[a + 1])
        else:
            for a in range(len(dmg)):
                if move_set == dmg[a]:
                    items.append(dmg[a + 1])

        # Random atk chance
        while True:
            print(f"Enter the number of the attack or back to exit.\nWill: {self.will}\n")

            for i in range(len(move_set)):
                print(f"{move_set[i]} Atk: {items[i].split("/")[0]} Cost: {items[i].split("/")[1].split("-")[0]} [{i + 
                                                                                                                   1}]")

            attack = input()

            if attack.isdigit() and (int(attack) - 1) in range(len(move_set)):
                print(f"{self.name} used {move_set[int(attack) - 1]}!")

                if "-" in items[int(attack) - 1].split("/")[0]:
                    self.temp_dmg = items[int(attack) - 1].split("/")[0]
                    self.temp_dmg = int(random.choice(self.temp_dmg.split("-")))
                else:
                    self.temp_dmg = int(items[int(attack) - 1].split("/")[0])
                self.cal_total_dmg(target)
                self.will -= int(items[int(attack) - 1].split("/")[1].split("-")[0])
                if not items[int(attack) - 1].split("/")[2] == "none":
                    ran = random.randint(1, 2)
                    if ran == 1:
                        target.activate_status(items[int(attack) - 1].split("/")[2], 3)

                return "c"
            elif attack.upper() == "BACK":
                return "b"

            else:
                print("Please enter one of the choices.")

    # Inventory Shenanigans --------------------------------------------------------------------------------------------
    # -- Adding things to inventory --
    def inventory_add(self, add):
        self.inventory.append(add)
        print(f"{add} added to your inventory!")

    # -- Check and use items --
    def inventory_check_use(self):
        if self.inventory:
            while True:
                print("What would you like to use? (Please enter the number of the item or back)")

                for i in range(len(self.inventory)):
                    print(f"\n[{i + 1}] {self.inventory[i]}")

                item = input()

                if item.isdigit() and (int(item) - 1) < len(self.inventory):
                    if self.use_item((int(item) - 1)) == "ERROR":
                        print("Something went wrong... This item is unidentifiable.")
                        return "ERROR"
                    self.inventory.pop(int(item) - 1)
                    return "c"
                elif item.upper() == "BACK":
                    return "b"
                else:
                    print("Please enter a number for an item or back to exit.")
        else:
            print("Your inventory is empty.")
            return "b"

    # -- Actually uses items --
    # NOTE: It goes like this:
    # ///
    # go line by line and if ITEM chosen by Player == txt on line[i] then:
    # Effect type-damage/add effect/heal-End/repeat
    # Text
    # ///
    # In all, this part checks for 3 lines. The initial line, the line with the text, and the line with the effects.
    # It only uses line 3 for item_effects()
    def use_item(self, num):
        for i in range(len(self.item_lines)):
            if self.inventory[num] == self.item_lines[i]:
                if self.item_lines[i + 1] != "none":
                    print(self.item_lines[i + 1])
                    time.sleep(1)
                self.item_effects(self.item_lines[i + 2])
                return "Continue"

        return "ERROR"

    # -- Applies the item effects --
    def item_effects(self, split):
        split = split.split("-")
        start = 0
        while split[start] != "E":
            # For health potions
            if split[start] == "H":
                self.heal(int(split[start + 1]))

            # For dealing damage
            if split[start] == "D":
                self.take_health(int(split[start + 1]))

            # For removing effects
            elif split[start] == "R":
                for i in self.inflicted:
                    if split[start + 1] == self.inflicted[i]:
                        num = i
                self.last_turn.pop(num)
                self.inflicted.pop(num)
                self.increase_dmg.pop(num)

            # Adds effects
            elif split[start] == "A":
                self.activate_status(split[start + 1], int(split[start + 2]))
                start += 1

            elif split[start] == "W+":
                self.will += int(split[start + 1])

            # Random effects
            elif split[start] == "|":
                ran = " ".join(i for i in split if i.isalpha())
                ran = ran.split(" ")
                ran = random.choice(ran)
                for i in range(len(split)):
                    if ran == split[i]:
                        num = i
                self.item_effects((split[num] + "-" + split[num + 1] + "-E"))

            start += 2
            time.sleep(1)
