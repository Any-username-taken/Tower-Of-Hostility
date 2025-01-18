# File name-Base game.py

import random
import time
from Classes import *
from init_fights import *


def show_map(player_pos, visualizer):
    # -- Shows the map --
    y_pos = visualizer[player_pos[1]].split("-")
    if "P" in y_pos[player_pos[0]]:
        y_pos[player_pos[0]] = y_pos[player_pos[0]].replace("P", "*")
    else:
        y_pos[player_pos[0]] = y_pos[player_pos[0]].replace(" ", "*")
    player = ""
    for i in range(len(y_pos)):
        if i != 0 and i != len(y_pos):
            player = player + "-" + y_pos[i]
        else:
            player = player + y_pos[i]
    visualizer[player_pos[1]] = player

    for i in range(len(visualizer)):
        print(visualizer[i])


def check_move(player_pos, visualizer, map_number, keys):
    # -- Checks the space the Player is going to --
    # - This part is for battles/items -
    with open("txt files/map2.txt", "r") as maps:
        line_2 = maps.read().split("|")
    vis = line_2[map_number].split("\n")
    y = vis[player_pos[1] + 1].split("-")

    y_pos = visualizer[player_pos[1]].split("-")
    if "x" in y_pos[player_pos[0]]:
        return "wall"
    elif "N" in y_pos[player_pos[0]]:
        if "B" in y[player_pos[0]]:
            remove_char(y, player_pos, vis, map_number, "B")

            return "boss"
        else:
            return "up"
    elif "P" in y_pos[player_pos[0]]:
        return "down"
    else:
        if "E" in y[player_pos[0]]:
            remove_char(y, player_pos, vis, map_number, "E")

            return "monster"
        elif "I" in y[player_pos[0]]:
            remove_char(y, player_pos, vis, map_number, "I")

            return "item"
        elif "D" in y[player_pos[0]]:
            if keys == 0:
                print("A mysterious barrier blocks your path...")
                time.sleep(1)
                print("[1] Key needed")
                time.sleep(1)

                return "wall"

            else:
                print("Key used to open barrier!")
                time.sleep(1)

                remove_char(y, player_pos, vis, map_number, "D")

                return "decrease"

        elif "K" in y[player_pos[0]]:
            print("You found a key!")
            time.sleep(1)

            remove_char(y, player_pos, vis, map_number, "K")

            return "increase"
        else:
            return " "


def remove_char(y, player_pos, vis, map_num, char):
    y[player_pos[0]] = y[player_pos[0]].replace(char, " ")
    player = ""
    for i in range(len(y)):
        if i != 0 and i != len(y):
            player = player + "-" + y[i]
        else:
            player = player + y[i]
    vis[player_pos[1] + 1] = player
    player = ""
    for i in range(len(vis)):
        if i != 0 and i != len(vis):
            player = player + "\n" + vis[i]
        else:
            player = player + vis[i]

    with open("txt files/map2.txt", "r") as map_test:
        lines = map_test.read().split("|")

    lines.insert(map_num, player)
    lines.pop(map_num + 1)
    player = ""

    for i in range(len(lines)):
        if i != 0 and i != len(lines):
            player = player + "|" + lines[i]
        else:
            player = player + lines[i]

    var = open("txt files/map2.txt", "w")
    var.write(player)
    var.close()


def refresh_map(map_number):
    # -- Resets the map or else the player will appear on all previous spots --
    with open("txt files/map.txt", "r") as maps:
        lines = maps.read().split("|")
    visualizer = lines[map_number].split("\n")
    visualizer.pop(0)
    visualizer.pop(0)
    return visualizer


def choose_path(map_number, player):
    # -- Opens .txt file --
    with open("txt files/map.txt", "r") as maps:
        lines = maps.read().split("|")
    # I don't like looking at this, but it is necessary for it to work.
    visualizer = lines[map_number].split("\n")
    player_pos = visualizer[1].split(" ")
    player_pos[0] = int(player_pos[0])
    player_pos[1] = int(player_pos[1])
    dimensions = visualizer[0].split(" ")
    dimensions[0] = int(dimensions[0])
    dimensions[1] = int(dimensions[1])
    visualizer.pop(0)
    visualizer.pop(0)
    keys = 0
    print(f"Which way do you want to go? (controls: u) up, d) down, l) left, r) right, i) Inventory\n[F{map_number}]")
    show_map(player_pos, visualizer)
    while True:
        # -- Resets Map --
        visualizer = refresh_map(map_number)
        # -- Controls --
        check = "Nan"
        ask = input()

        if ask.lower() == "w":
            if player_pos[1] > 0:
                check = check_move((int(player_pos[0]), (int(player_pos[1]) - 1)), visualizer, map_number, keys)
                if check == "up" or check == "down" or check == " " or check == "monster" or check == "item" or check == "boss" or check == "increase" or check == "decrease":
                    player_pos[1] -= 1
                else:
                    print("Can't move here...")
                    time.sleep(1)
            else:
                print("Can't move here...")
                time.sleep(1)

        elif ask.lower() == "s":
            if player_pos[1] < dimensions[1]:
                check = check_move((int(player_pos[0]), (int(player_pos[1]) + 1)), visualizer, map_number, keys)
                if check == "up" or check == "down" or check == " " or check == "monster" or check == "item" or check == "boss" or check == "increase" or check == "decrease":
                    player_pos[1] += 1
                else:
                    print("Can't move here...")
                    time.sleep(1)
            else:
                print("Can't move here...")
                time.sleep(1)

        elif ask.lower() == "a":
            if player_pos[0] > 0:
                check = check_move(((int(player_pos[0]) - 1), int(player_pos[1])), visualizer, map_number, keys)
                if check == "up" or check == "down" or check == " " or check == "monster" or check == "item" or check == "boss" or check == "increase" or check == "decrease":
                    player_pos[0] -= 1
                else:
                    print("Can't move here...")
                    time.sleep(1)
            else:
                print("Can't move here...")
                time.sleep(1)

        elif ask.lower() == "d":
            if player_pos[0] < dimensions[0]:
                check = check_move(((int(player_pos[0]) + 1), int(player_pos[1])), visualizer, map_number, keys)
                if check == "up" or check == "down" or check == " " or check == "monster" or check == "item" or check == "boss" or check == "increase" or check == "decrease":
                    player_pos[0] += 1
                else:
                    print("Can't move here...")
                    time.sleep(1)
            else:
                print("Can't move here...")
                time.sleep(1)

        elif ask.upper() == "INVENTORY" or ask.upper() == "I":
            player.inventory_check_use()

        else:
            print("Please enter one of the actions. (controls: u) up, d) down, l) left, r) right)")

        # -- Shows Map/Exits Loop --
        if check == "up":
            return "up"
        elif check == "down":
            return "down"
        else:
            if check == "monster":
                enemy = get_enemy(map_number)
                mock_fight(enemy, player)
                print(f"[F{map_number}]")
                show_map(player_pos, visualizer)
            elif check == "item":
                player.inventory_add("Strength Potion [s]")
                print(f"[F{map_number}]")
                show_map(player_pos, visualizer)
            elif check == "boss":
                enemy = get_boss(map_number)
                mock_fight(enemy, player)
                print("BOSS")
                return "up"
            else:
                if check == "increase":
                    keys += 1
                elif check == "decrease":
                    keys -= 1
                print(f"[F{map_number}]")
                show_map(player_pos, visualizer)


def main(player):
    # -- Controls # of floor
    with open("txt files/map.txt", "r") as thing:
        maps = thing.read().split("|")
    floor = 0
    while floor < len(maps):
        traverse = choose_path(floor, player)
        if traverse == "up":
            floor += 1
        else:
            floor -= 1


with open("txt files/map2save.txt", "r") as save:
    lines = save.read()
reset = open("txt files/map2.txt", "w")
reset.write(lines)
reset.close()

# -- Player set-up --

n = input("Please enter your name:\n")

player = Player(n, "normal", "", 50, 0, 0, 5, 100, 50, "", "", 0, "wooden sword")

# -- Starts main loop --
main(player)
time.sleep(1)
print("Congratulations on reaching the peak of the tower(so far)!")
