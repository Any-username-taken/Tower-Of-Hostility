# File name-init_fights.py

import time
import random
from Classes import *


def tutorial():
    # Come back later
    return


def get_enemy(map_num):
    with open("txt files/enemy.txt", "r") as choose:
        lines = choose.read().split("|")
    lines.pop(0)

    for i in range(len(lines)):
        if str(map_num) == lines[i].split("\n")[0]:
            lines = lines[i]
            print("Found enemy successfully")
            break

    lines = lines.split("\n")
    lines.pop(len(lines) - 1)
    lines.pop(len(lines) - 1)
    lines.pop(0)

    lines = random.choice(lines)

    lines = lines.split("/")

    if lines[2] == "none":
        type2 = ""
    else:
        type2 = lines[2] + " "

    monster = Monster(lines[0], lines[1].split("-"), type2, lines[3], lines[4], lines[5], lines[6], lines[7],
                      lines[8], lines[9].split("-"), lines[10], lines[11])

    return monster


def get_boss(map_num):
    with open("txt files/enemy.txt", "r") as choose:
        lines = choose.read().split("|")
    lines.pop(0)

    for i in range(len(lines)):
        if str(map_num) == lines[i].split("\n")[0]:
            lines = lines[i]
            print("Found BOSS")
            break

    lines = lines.split("\n")
    lines.pop(len(lines) - 1)
    lines.pop(0)

    lines = lines[len(lines) - 1]

    lines = lines.split("/")

    type2 = lines[2] + " "

    monster = Monster(lines[0], lines[1].split("-"), type2, lines[3], lines[4], lines[5], lines[6], lines[7],
                      lines[8], lines[9].split("-"), lines[10], lines[11])

    return monster


def mock_fight(enemy, player):
    # come back later
    print(f"{enemy.name} appears!")
    time.sleep(1)
    enemy.find_weakness()
    player.find_weakness()
    run = False
    skip = False

    # Main loop
    while enemy.is_alive() and player.is_alive() and not run:
        player.reset()
        player.inflict_status()
        # -- Visuals --
        enemy.show_health()

        print("\n\n")

        player.show_health()

        # -- Main Player Loop __
        while True:
            if skip:
                skip = False
                break
            if run:
                break
            print("[FIGHT]   [ACTION]\n[ITEM]    [SPELLS]")
            action = input()

            # -- Action Section --
            if action.upper() == "FIGHT" or action.upper() == "F":
                if player.get_moves(enemy) == "c":
                    break

            elif action.upper() == "ACTION" or action.upper() == "A":
                while True:
                    ans = input("[INFO]   [RUN]\n[BACK]    [DEFEND]\n")

                    if ans.upper() == "INFO" or ans.upper() == "I":
                        print(f"Name: {enemy.name} Health: {enemy.h}")
                        time.sleep(1)
                        break

                    elif ans.upper() == "RUN" or ans.upper() == "R":
                        ran = random.randint(0, 100)

                        if ran <= player.dc:
                            run = True
                            print("You ran from the fight...")
                            time.sleep(1)
                            break
                        else:
                            print("You couldn't run from the fight!")
                            time.sleep(1)
                            skip = True
                            break

                    elif ans.upper() == "DEFEND" or ans.upper() == "D":
                        player.temp_d += 5
                        print(f"{player.name} defended!")

                    elif ans.upper() == "BACK" or ans.upper() == "B":
                        break

                    else:
                        print("Please enter one of the choices.")

            elif action.upper() == "ITEM" or action.upper() == "I":
                if player.inventory_check_use() == "c":
                    break

            # --COME BACK FOR SPELLS--
            else:
                print("Please enter one of the choices...")
                time.sleep(1)
        enemy.inflict_status()

        if enemy.is_alive() and not run:
            enemy.reset()
            ran = random.randint(1, 20)
            if ran < 18:
                enemy.enemy_move(player)
            elif ran < 19:
                print(f"{enemy.name} defended!")
                time.sleep(1)
                enemy.temp_d += 3
            else:
                enemy.heal(int((enemy.mh / 3)))
        elif not run:
            print(f"{player.name} defeated {enemy.name}!")
            player.inventory_add(enemy.give_item())
            if enemy.gold > 1:
                print(f"{player.name} got {enemy.gold} gold.")
                player.gold += enemy.gold
