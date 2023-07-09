"""
A Text-Based Escape Room Game in Python.

Author: Ainsley Baker
Version: 3.11
"""

import json

"""Declaring Global variables"""
ITEM_COST = {
    "usb": 10,
    "book": 20,
    "stool": 40,
    "mop": 10,
    "crowbar": 20,
    "key": 0
}
GAME_ROOMS = {}

def load_rooms():
    """Loads room file containing each room, a description and items"""
    global GAME_ROOMS
    try:
        with open("Game_rooms.json", "r") as file:
            GAME_ROOMS = json.load(file)
    except FileNotFoundError:
        return "Game_rooms.json not found."
    
def describe(room):
    """Reads and prints a description of the current room"""
    if room in GAME_ROOMS["rooms"]:
        return GAME_ROOMS["rooms"][room]["description"]
    else:
        return "ERROR: unknown location: " + str(room)


def describe_items(room):
    """Prints the items available in the current room"""
    room_items = "You can see:"
    for item in GAME_ROOMS["rooms"][room]["items"]:
        if item in ITEM_COST:
            price = ITEM_COST[item]
            item = f"{item}(${price})"
        room_items += " " + item
    return room_items


def move_central(direction):
    """Handles movement from the central room"""
    if direction == "north":
        return "reading"
    elif direction == "east":
        return "janitor"
    return ""


def move_janitor(direction):
    """Handles movement from the janitor room."""
    if direction == "west":
        return "central"
    return ""


def move_computer(direction):
    """Handles movement from the computer room."""
    if direction == "east":
        return "reading"
    return ""


def move_reading(direction, states):
    """Handles movement from the reading room."""
    if direction == "west":
        if states["door_locked"]:
            print(file_read("18"))
        else:
            return "computer"
    elif direction == "south":
        return "central"
    elif direction == "east":
        if states["end_locked"]:
            print(file_read("19"))
        else:
            return "end"
    return ""

def move(direction, room, states):
    """Handles the move command to change to corresponding room"""
    if room == "central":
        new_room = move_central(direction)
    elif room == "computer":
        new_room = move_computer(direction)
    elif room == "janitor":
        new_room = move_janitor(direction)
    elif room == "reading":
        new_room = move_reading(direction, states)
    else: 
        print("Invalid state: " + direction)
        new_room = ""

    # Checking if it was an invalid move, or move that wins game.
    if new_room == "":
        print("You cannot go " + str(direction) + " from here.")
        return room
    elif new_room == "end":
        return "end"
    else:
        print(describe(new_room))
        print(describe_items(new_room))
        return new_room
    
def get(obj, carrying, cash, room):
    """Handles the get command to pick up an object"""
    # Objects that arent able to be picked up
    nonpickup_items = ["door", "table", "computer", "bookshelf"]
    if obj in GAME_ROOMS["rooms"][room]["items"] and obj not in nonpickup_items:
        if len(carrying) < 3:
            cost = ITEM_COST[obj]
            if cash < cost:
                print("Not enough cash. Try dropping an item.")
            else:
                print(f"You picked up {obj}.")
                GAME_ROOMS["rooms"][room]["items"].remove(obj)
                carrying.append(obj)
                cash -= cost
                print(f"You now have ${cash} left")
        else:
            print("Too many items in inventory.")
    else:
        print("You cannot pick that up!")
    return cash

def drop(obj, carrying, cash, room):
    """Handles the drop command to drop an object"""
    if obj in carrying:
        GAME_ROOMS["rooms"][room]["items"].insert(0, obj)
        print("You dropped " + obj)
        carrying.remove(obj)
        cash_back = ITEM_COST[obj] * 0.5
        cash += cash_back
        print(f"You received ${cash_back} back and now have ${cash}")
    else:
        print("You can't drop that item")
    return cash


def look_at(obj, room, states):
    """Handles the look at command to inspect an object"""
    if obj == "bookshelf" and room == "reading":
        print(file_read("2"))
        GAME_ROOMS["rooms"][room]["items"].append("book")
        print(describe_items(room))
    elif obj == "table" and room == "central":
        print(file_read("3"))
        GAME_ROOMS["rooms"][room]["items"].append("usb")
        print(describe_items(room))
    elif obj == "computer" and room == "computer":
        print(file_read("4"))
        states["logged_in"] = True
    else:
        print(f"item {obj} is unable to be looked at")


def use(obj, carrying, room, states):
    """Handles the use command to use an object"""
    if obj in carrying:
        # Using usb object
        if obj == "usb":
            if room != "computer":
                print(file_read("5"))
            elif room == "computer" and states["logged_in"]:
                print(file_read("6"))
                carrying.remove("usb")
            elif room == "computer":
                print(file_read("7"))
        # Using book object
        elif obj == "book":
            print(file_read("8"))
        # Using stool object
        elif obj == "stool":
            if room == "janitor":
                print(file_read("9"))
                GAME_ROOMS["rooms"][room]["items"].append("key")
                print(describe_items(room))
            elif room == "computer":
                print(file_read("10"))
            elif room == "central":
                print(file_read("11"))
            elif room == "reading":
                print(file_read("12"))
        # Using key object
        elif obj == "key":
            if room == "reading":
                print(file_read("13"))
                states["end_locked"] = False
            else:
                print(file_read("14"))
        # Using crowbar object
        elif obj == "crowbar":
            if room == "reading":
                print(file_read("15"))
                states["door_locked"] = False
            else:
                print(file_read("16"))
        # Using mop object
        elif obj == "mop":
            print(file_read("17"))
    # Object not able to be used
    else:
        print("You can't use that item")


def file_read(start):
    """Loads and reads a section of the file starting from the given position"""
    try:
        with open("Game_Data.txt", "r") as file:
            file_content = file.read()
    except FileNotFoundError:
        return "Game_data.txt Not Found."
    
    try:
        assert 0 < int(start) < 20
        end = str(int(start) + 1)
    except (ValueError, AssertionError):
        return "Invalid start position: Must be an integer between 1-19"
    else:
        # Numbers are used throughout text file to inidicate each section. 
        start_index = file_content.find(start)
        end_index = file_content.find(end)
        section_result = file_content[start_index:end_index].strip(start)
        return section_result


def player_stats():
    """Reads and display the player's name and cash amount"""
    try:
        with open("Player_stats.txt", "r") as stats:
            stats = stats.readlines()
            name = stats[0].split()[1]
            cash = int(stats[1].split("$")[1])
            return name, cash
    except FileNotFoundError:
       print("Player_stats.txt Not Found.")


def game():
    """Main game loop that handles user input and function calls"""
    move_count = 30
    room = "central"
    carrying = []
    states = {"logged_in": False, "door_locked": True, "end_locked": True}

    load_rooms()
    print(file_read("1"))
    name, cash = player_stats()
    print(f"Your name is {name} and you have ${cash}")
    input("Press Enter to Start...")
    print("\n" + describe(room))
    print(describe_items(room))

    while move_count != 0:
        action = input(f"Move {move_count}> Enter your action: ")
        action = " ".join(action.split())
        action = action.lower()
        move_count -= 1

        if action == "quit":
            print("Game Over! Thanks for playing.")
            exit()
        elif action.startswith("move "):
            direction = action[5:]
            result = move(direction, room, states)
            if result == "end":
                break
            room = result
        elif action.startswith("get "):
            get_obj = action[4:]
            cash = get(get_obj, carrying, cash, room)
        elif action.startswith("look at "):
            look_at_obj = action[8:]
            look_at(look_at_obj, room, states)
        elif action.startswith("use "):
            use_obj = action[4:]
            use(use_obj, carrying, room, states)
        elif action in ["inv", "inventory"]:
            print(carrying)
            move_count += 1
        elif action.startswith("drop "):
            drop_obj = action[5:]
            cash = drop(drop_obj, carrying, cash, room)
            move_count += 1
        elif action.startswith("drop") and not action.startswith("drop "):
            print("Specify an object to drop")
        else:
            print(f"Input '{action}' not recognized. Try move/get/quit")

    if move_count > 0:
        print(f"Congratulations you have successfully escaped the library. \
It took you {30 - move_count} moves.")
        
        # Write name and cash amount to file
        with open("Player_stats.txt", "w") as stats:
            stats.write(f"Name: {name}\n")
            stats.write(f"Cash: ${cash}")
    else:
        print("You ran out of moves. Better luck next time!")
    input("Press Enter to Close...")


if __name__ == "__main__":
    game()
