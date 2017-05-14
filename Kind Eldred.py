# The Legend of King Eldred
# © Code Angel 2017

import map
import game_items

MAP_MAX_ROW = 7
MAX_MAP_COLUMN = 7

START_ROOM = '01'
END_ROOM = '24'

def main():

    map_row = 0
    map_column = 0

    new_row = 0
    new_column = 0

    game_over = False
    alive = True

    room = ''

    gold = 0

    town_map = map.get_town_map()
    room_descriptions = map.get_room_descriptions()
    doors = map.get_doors()
    chests = map.get_chests()
    deadly_exits = map.get_deadly_exits()
    signs = map.get_signs()
    talking = map.get_talking()
    hints = map.get_hints()

    all_items = game_items.get_items()

    display_intro()

    room_items = []

    inventory = []

    for row_num, row in enumerate(town_map):
        for col_num, next_room in enumerate(row):
            if next_room == START_ROOM:
                map_row = row_num
                map_column = col_num
                room = town_map[map_row][map_column]

                display_room_description(room_descriptions, room)
                room_items = get_room_items(room, all_items)
                chest_in_room = get_room_chest(room, chests)
                display_room_items(room_items, all_items, chest_in_room)

    direction_list = ['n', 'north', 's', 'south', 'e', 'east', 'w', 'west']
    command_list = ['help', 'hint', 'inv', 'take', 'drop', 'look', 'examine', 'open', 'unlock', 'read', 'talk']
    action_list = ['smash', 'dig', 'burn', 'give', 'drink', 'fill', 'say', 'pull', 'pierce', 'oil', 'turn']

    command_list.extend(direction_list)
    command_list.extend(action_list)


    while game_over is False:

        is_valid_room = True
        is_closed_door = False

        user_command = input("\nWhat do you want to do? ")
        is_valid_command = check_valid_command(command_list, user_command)

        if user_command in direction_list:
            new_row = get_new_map_row(map_row, user_command)
            new_column = get_new_map_column(map_column, user_command)
            is_valid_room = check_valid_room(town_map, new_row, new_column)
            is_closed_door = check_for_door(room, user_command, doors)

            is_deadly_exit = check_for_safe_exit(room, user_command, deadly_exits)
            if is_deadly_exit is True:
                game_over = True
                alive = False



        while is_valid_command is False or is_valid_room is False or is_closed_door is True and game_over is False:
            if is_valid_command is False:
                print("I don't know how to do that.")
            elif is_closed_door is True:
                print('The door is not open.')
            else:
                print("You can't go that way.")

            is_valid_room = True
            is_closed_door = False

            user_command = input("\nWhat do you want to do? ")
            is_valid_command = check_valid_command(command_list, user_command)

            if user_command in direction_list:
                new_row = get_new_map_row(map_row, user_command)
                new_column = get_new_map_column(map_column, user_command)
                is_valid_room = check_valid_room(town_map, new_row, new_column)
                is_closed_door = check_for_door(room, user_command, doors)

                is_deadly_exit = check_for_safe_exit(room, user_command, deadly_exits)
                if is_deadly_exit is True:
                    game_over = True
                    alive = False

        if user_command in direction_list:
            map_row = new_row
            map_column = new_column
            room = town_map[map_row][map_column]

            display_room_description(room_descriptions, room)
            room_items = get_room_items(room, all_items)
            chest_in_room = get_room_chest(room, chests)
            display_room_items(room_items, all_items, chest_in_room)


            if room == END_ROOM:
                game_over = True


        elif user_command == 'inv':
            display_inventory_description(inventory, all_items, gold)

        elif user_command == 'look':
            room_items = get_room_items(room, all_items)
            chest_in_room = get_room_chest(room, chests)
            display_room_description(room_descriptions, room)
            display_room_items(room_items, all_items, chest_in_room)




        elif user_command == 'help':
            display_all_commands(command_list)

        elif user_command == 'hint':
            gold = get_hint(room, hints, gold)

        elif 'take' in user_command:
            take_item(user_command, room_items, all_items, inventory)
        elif 'drop' in user_command:
            drop_item(user_command, room_items, all_items, inventory, room)
        elif 'door' in user_command:
            manage_door(doors, room, user_command, inventory, all_items)
        elif 'chest' in user_command:
            found_gold = manage_chest(chests, room, user_command, inventory, all_items)
            gold += found_gold
            if found_gold > 0:
                print('You now have ' + str(gold) + ' gold pieces.')
        elif 'examine' in user_command:
            chest_in_room = get_room_chest(room, chests)
            examine_item(room, user_command, room_items, all_items, inventory, chest_in_room)
        elif 'read' in user_command:
            read_sign(signs, room)
        elif 'talk' in user_command:
            talk_to_character(talking, room)

        else:
            death = carry_out_action(user_command, inventory, room_items, all_items, room,
                                     deadly_exits, room_descriptions, doors, chests, signs)
            if death is True:
                game_over = True
                alive = False

    if alive is True:
        print()
        print('You have conquered Wildemoor and solved The Legend of King Eldred.')
        if 'crown' in inventory:
            print('You found the Crown of Anquira which brings untold power and wealth to whomever wears it.')
        else:
            print('You failed to find the Crown of Anquira.')

        print('You leave Wildemoor with ' + str(gold) + ' gold pieces.')
    else:
        print('And so The Legend of Kind Eldred takes the life of another brave explorer...')


def check_valid_command(command_list, user_command):

    valid_command = False

    for command_word in user_command.split():
        if command_word in command_list:
            valid_command = True

    return valid_command

def get_new_map_row(row, direction):

    if direction == 'n' or direction == 'north':
        row -= 1
    elif direction == 's' or direction == 'south':
        row += 1

    return row

def get_new_map_column(col, direction):
    if direction =='e' or direction == 'east':
        col += 1
    elif direction == 'w' or direction == 'west':
        col -= 1

    return col



def check_valid_room(town_map, map_row, map_column):

    valid_room = True

    if map_row < 0:
        valid_room = False
    elif map_row > MAP_MAX_ROW - 1:
        valid_room = False
    elif map_column < 0:
        valid_room = False
    elif map_column > MAX_MAP_COLUMN - 1:
        valid_room = False
    elif town_map[map_row][map_column] == '--':
        valid_room = False

    return valid_room

def display_room_description(room_descriptions, room):
    print('\n' + room_descriptions.get(room))

def get_room_items(current_room, all_items):

    room_items = []

    for items_key, item in all_items.items():
        item_room = item.get('room')
        if item_room == current_room:
            room_items.append(items_key)


    return room_items

def get_room_chest(current_room, chests):
    room_chest = False

    for chests_key, chest in chests.items():
        chest_room = chest.get('room')
        if chest_room == current_room:
            room_chest = True

    return room_chest

def display_room_items(room_items, all_items, chest_in_room):

    item_found = False
    for item_key in room_items:
        item = all_items.get(item_key)

        if item_found is False:
            print('You can see:')
            item_found = True
        item_description = item.get('description')
        print(item_description)

    if chest_in_room is True:
        print('chest')

def take_item(user_command, room_items, all_items, inventory):

    item_in_inventory = False
    item_in_room = False
    take_item_dict_key = ''




    for item_key in room_items:
        item = all_items.get(item_key)
        item_name = item.get('name')
        if item_name in user_command:
            item_in_room = True
            take_item_dict_key = item_key

    for item_key in inventory:
            item = all_items.get(item_key)
            item_name = item.get('name')
            if item_name in user_command:
                item_in_inventory = True




    if item_in_room is True:
        item = all_items.get(take_item_dict_key)
        item_name = item.get('name')
        item_description = item.get('description')
        item_can_be_taken = item.get('inv')

        if item_name in user_command:
            if item_can_be_taken is True:
                print('You take the ' + item_description + '.')
                inventory.append(take_item_dict_key)
                room_items.remove(take_item_dict_key)
                all_items.get(take_item_dict_key)['room'] = '0'

            else:
                print('You cannot carry that item.')

        #if item_found is False:
        #    print('You cannot take that.')

    elif item_in_inventory is True:
        print('You are already carrying that.')

    else:
        print('You cannot take that.')


def drop_item(user_command, room_items, all_items, inventory, room):
    item_in_inventory = False

    for item_key in inventory:
        item = all_items.get(item_key)
        item_name = item.get('name')
        item_description = item.get('description')
        if item_name in user_command:
            item_in_inventory = True

            print('You drop the ' + item_description + '.')
            inventory.remove(item_key)
            room_items.append(item_key)
            all_items.get(item_key)['room'] = room

    if item_in_inventory is False:
        print('You are not carrying that item.')

def examine_item(room, user_command, room_items, all_items, inventory, chest_in_room):

    item_found = False

    for item_key in inventory + room_items:
        item = all_items.get(item_key)
        item_name = item.get('name')
        item_examine= item.get('examine')
        item_can_be_taken = item.get('inv')



        if item_name in user_command:
            item_found = True
            if item_can_be_taken is True:
                print(item_examine)

            else:
                item_discovered = item.get('discovered')
                secret_item = item.get('secret item')
                if secret_item == "none":
                    status = item.get('status')
                    display_status = item.get('display status')
                    if display_status == None:
                        status = ''
                    print(item_examine + status)

                elif item_discovered is False:
                    print(item_examine)
                    room_items.append(secret_item)
                    all_items.get(secret_item)['room'] = room
                    item['discovered'] = True
                    display_room_items(room_items, all_items, chest_in_room)
                else:
                    print('There is nothing more to be discovered here.')



    if item_found is False:
        print("You can't examine that item.")

def check_for_safe_exit(room, direction, deadly_exits):

    deadly_exit = False

    direction = direction[:1]

    for deadly_exit_key in deadly_exits:
        exit = deadly_exits.get(deadly_exit_key)
        exit_room = exit.get('room')
        if exit_room == room:
            room_safe = exit.get('safe')
            exit_direction = exit.get('direction')

            if direction == exit_direction:
                if room_safe is True:
                    deadly_exit = False
                else:
                    deadly_exit = True
                    death_text = exit.get('death')
                    print(death_text)

    return deadly_exit

def check_for_door(room, direction, doors):

    closed_door = False

    direction = direction[:1]

    for door_key in doors:
        door = doors.get(door_key)
        door_room = door.get('room')
        if door_room == room:
            door_open = door.get('open')
            door_locked = door.get('locked')
            door_direction = door.get('direction')

            if direction == door_direction:
                if door_locked is True or door_open is False:
                    closed_door = True

    return closed_door


def manage_door(doors, room, user_command, inventory, all_items):

    this_room_door = {}

    for door_dict_key in doors:
        door = doors.get(door_dict_key)
        door_room = door.get('room')
        if door_room == room:
            this_room_door = door




    if this_room_door:
        door_open = this_room_door.get('open')
        door_locked = this_room_door.get('locked')
        unlock_key = this_room_door.get('unlock key')

        if 'examine' in user_command:
            door_examine = this_room_door.get('examine')
            print(door_examine)
        elif 'open' in user_command:

            if door_open is True:
                print('The door is already open.')
            elif door_locked is True:
                print('The door is locked.')
            else:
                print('You open the door.')
                this_room_door['open'] = True

        elif 'unlock' in user_command:
            if door_locked is False:
                print('The door is already unlocked')
            else:
                if unlock_key in inventory:
                    unlock_key_record = all_items.get(unlock_key)

                    unlock_key_description = unlock_key_record.get('description')
                    print('You unlock the door with the ' + unlock_key_description + '.')
                    this_room_door['locked'] = False
                    inventory.remove(unlock_key)

                elif unlock_key == 'code':
                    unlock_key_code = this_room_door.get('unlock code')
                    if unlock_key_code in user_command:
                        print('The code ' + unlock_key_code + ' unlocks the door.')
                        this_room_door['locked'] = False
                    else:
                        print('That code does not unlock the door.')


                else:
                    print('You do not have a key to unlock this door.')



    else:
        print('There is no door here.')

def manage_chest(chests, room, user_command, inventory, all_items):

    this_room_chest = {}

    found_gold = 0

    for chest_dict_key in chests:
        chest = chests.get(chest_dict_key)
        chest_room = chest.get('room')
        if chest_room == room:
            this_room_chest = chest




    if this_room_chest:
        chest_open = this_room_chest.get('open')
        chest_locked = this_room_chest.get('locked')
        unlock_key = this_room_chest.get('unlock key')

        if 'examine' in user_command:
            door_examine = this_room_chest.get('examine')
            print(door_examine)
        elif 'open' in user_command:


            if chest_open is True:
                print('The chest is already open.')
            elif chest_locked is True:
                print('The chest is locked.')
            else:
                print('You open the chest.')
                this_room_chest['open'] = True
                found_gold = this_room_chest.get('gold')
                print('Inside the chest you find ' + str(found_gold) + ' gold pieces.')
                this_room_chest['gold'] = 0

        elif 'unlock' in user_command:
            if chest_locked is False:
                print('The chest is already unlocked')
            else:
                if unlock_key in inventory:
                    unlock_key_record = all_items.get(unlock_key)
                    unlock_key_description = unlock_key_record.get('description')
                    print('You unlock the chest with the ' + unlock_key_description + '.')
                    this_room_chest['locked'] = False
                    inventory.remove(unlock_key)
                else:
                    print('You do not have a key to unlock this chest.')



    else:
        print('There is no chest here.')

    return found_gold

def read_sign(signs, room):
    sign = signs.get(room)
    visible = signs.get(room).get('visible')
    if sign and visible is True:
        sign_message = sign.get('read')
        print(sign_message)
    else:
        print('There is nothing to read here.')

def talk_to_character(talking, room):
    talk_details = talking.get(room)
    if talk_details:
        says = talk_details.get('says')
        print(says)
    else:
        print('There is noone to talk to here.')



def carry_out_action(user_command, inventory, room_items, all_items, room, deadly_exits, room_descriptions, doors, chests, signs):

    all_items_valid = False
    death = False

    if 'smash' in user_command and 'bottle' in user_command and 'hammer' in user_command:
        if 'bottle' in inventory + room_items and 'hammer' in inventory + room_items:
            all_items_valid = True
            print('The hammer smashes the bottle.')
            print('A key falls to the floor.')
            inventory.remove('bottle')
            room_items.append('key 1')
            all_items.get('key 1')['room'] = room

    if 'dig' in user_command and 'spoon' in user_command and 'dirt' in user_command:
        if 'spoon' in inventory + room_items and 'dirt' in room_items:
            all_items_valid = True
            print('You dig the dirt with the spoon for what seems like hours.')
            print('Eventually you uncover a rock. It looks as though it has something carved into it.')
            room_items.append('rock')
            all_items.get('rock')['room'] = room

    if 'burn' in user_command and 'straw' in user_command and 'torch' in user_command:
        if 'torch' in inventory + room_items and 'straw' in room_items:
            all_items_valid = True
            print('You toss the lit torch onto the bed of straw.')
            print('The fire takes hold almost instantly and within minutes all the vipers are dead.')
            all_items.get('straw')['room'] = '00'
            deadly_exits.get('vipers')['safe'] = True
            room_descriptions[room] = 'It smells really bad in this tunnel, like burned sausages.  \
The floor and most of the walls are blackened with ash.'
            inventory.remove('torch')

    if 'give' in user_command and 'dog' in user_command and 'bone' in user_command:
        if 'bone' in inventory + room_items and 'dog' in room_items:
            all_items_valid = True
            print('You throw the bone in the direction of the large black dog. The dog gets up slowly and paces \
over to the bone.')
            print('It sniffs twice at the bone then picks it up in its enormous mouth and wanders off.')
            all_items.get('dog')['room'] = '00'
            deadly_exits.get('dog')['safe'] = True
            room_descriptions[room] = 'To the east are a set of marble steps which lead up to an old \
oak door. The door is open. There is a small gap leading to a cave in the west.'
            inventory.remove('bone')

    if 'drink' in user_command and 'fountain' in user_command:
        if 'fountain' in room_items:
            all_items_valid = True
            print('You drink the water. It is crystal clear, ice cold and very refreshing.')

    if 'fill' in user_command and 'bucket' in user_command:
        if 'bucket' in inventory + room_items and 'fountain' in room_items:
            all_items_valid = True
            print('You fill the bucket with ice cold crystal clear water from the fountain.')
            all_items.get('bucket')['status'] = 'filled'
            all_items.get('bucket')['description'] = 'bucket of water'
            all_items.get('bucket')['examine'] = 'An old bucket filled with ice cold water.'
            # inventory.remove('bucket')
            # inventory.append('bucket of water')


    if 'drink' in user_command and 'lake' in user_command:
        if 'lake' in room_items:
            all_items_valid = True
            print('You cup your hands together and drink some of the water. It tastes bitter.')
            print('You start to feel dizzy and everything around you is spinning.')
            print('You lie down and instantly fall into a deep, deep sleep.')
            print('You dream of kings and gold.')
            print('In your dream King Eldred appears as a vision and speaks some mysterious words.')
            print("'Learn the code of Python and all will be well with the world.'")
            print('You wake sometime later, dazed and confused.')

    if 'give' in user_command and 'horse' in user_command and 'water' in user_command:
        if 'bucket' in inventory + room_items and 'horse' in room_items:
            all_items_valid = True

            if all_items.get('bucket').get('status') == 'filled':
                print('You hold the bucket of water out to the horse.')
                print('It eyes you suspiciously at first, and the bends its neck to drink from the bucket.')
                print('As it drinks, a piece of parchment falls from underneath its saddle.')
                inventory.remove('bucket')
                room_items.append('parchment')
                all_items.get('parchment')['room'] = room
            else:
                print('The bucket is empty.')

    if 'give' in user_command and 'toy' in user_command and 'andrid' in user_command:
        if 'toy' in inventory + room_items and 'andrid' in room_items:
            all_items_valid = True
            print("Andrid turns to you and smiles. 'Thank you so much. This is my favourite toy.'")
            print('"Do you want this old bone key?", she adds, "It is of no use to me!"')
            print('Andrid hands you an old bone key.')
            inventory.remove('toy')
            inventory.append('key 7')

    if 'give' in user_command and 'egg' in user_command and 'baker' in user_command:
        if 'egg' in inventory + room_items and 'baker' in room_items:
            all_items_valid = True
            print('The baker says:"This is fantastic - now I can bake my cake.')
            print("It's for the banker, it's her birthday today.")
            print("Don't tell her I said this but she looks about 100 years old!")
            print('Wait! Here, take this as a reward for your troubles. It may come in handy..."')
            print('The baker hands you a floor plan drawn onto a large sheet of parchment.')
            inventory.remove('egg')
            inventory.append('floor plan')



    if 'say' in user_command and 'guard' in user_command and 'king' in user_command:
        if 'guard' in room_items:
            all_items_valid = True
            print('The guard pulls a hand-crafted silver key from his chest pocket, turns and slowly unlocks \
the door behind him.')
            print("'You may enter', he growls as he stands aside")
            doors.get('king')['locked'] = False
            doors.get('king')['open'] = True
    elif 'say' in user_command and 'guard' in user_command:
        if 'guard' in room_items:
            all_items_valid = True
            print("The guard moves his hand to the scimitar tucked into he belt and mutters 'No talk unless password.'")

    if 'pull' in user_command and 'gold lever' in user_command:
        if 'gold lever' in room_items:
            all_items_valid = True
            print('You pull the gold lever. For a brief second nothing happens.')
            print('You hear a click below you and so you look down. \
You realise you are standing on what appears to be a trap door.')
            print('Before you can react the trap door swings open and you are sent tumbling into a dark dungeon.')
            print("With no food or water in here you will not last for long. But long enough to reflect on the \
words you once saw on a sign: 'Water over earth, young over old, and silver over bronze and gold.'")
            death = True

    if 'pull' in user_command and 'silver lever' in user_command:
        if 'silver lever' in room_items:
            all_items_valid = True
            print('You pull the silver lever. For a brief second nothing happens.')
            print('You hear a click coming from inside the chest. It sounds as if the chest has somehow unlocked.')
            chests.get('lever room')['locked'] = False

    if 'pierce' in user_command and 'oil can' in user_command and 'nail' in user_command:
        if 'oil can' in inventory + room_items and 'nail' in inventory + room_items:
            all_items_valid = True
            all_items.get('oil can')['status'] = 'pierced'
            all_items.get('oil can')['description'] = 'pierced oil can'
            all_items.get('oil can')['examine'] = 'The oil can has been pierced and a small amount \
of oil is running out of the hole.'
            print('With some effort you manage to pierce a hole in the oil can. A small amount of oil \
seeps out of the hole.')

    if 'oil' in user_command and ('lever' in user_command or 'cogs' in user_command):
        if 'oil can' in inventory + room_items and 'marble lever' in room_items:
            all_items_valid = True
            oil_can_status = all_items.get('oil can').get('status')
            if oil_can_status == 'pierced':
                print('You pour a few drops of oil onto the rusted cogs of the marble lever.')
                all_items.get('marble lever')['status'] = 'oiled'
            else:
                print('The oil can is sealed and so no oil will come out.')

    if 'pull' in user_command and 'lever' in user_command:
        if 'marble lever' in room_items:
            all_items_valid = True
            lever_status =  all_items.get('marble lever').get('status')
            if lever_status == 'rusted':
                print('You try pulling the marble lever with all your strength but it will not shift. \
The cogs are badly rusted.')
            else:
                print('You try pulling the marble lever. At first it will not move.')
                print('But then slowly the freshly oiled cogs begin to turn and the lever moves.')
                print('The marble lid of the sarcophogus slides on to the floor providing a bridge across the \
deadly spikes.')
                print('')
                print('A skeleton lies inside the sarcophogus.')
                print('A beautiful marble chest sits at the feet of the skeleton.')
                print('A golden crown studded with large emeralds and diamonds sits on the skull of the skeleton.')
                print('There is a plaque on the side of the sarcophogus.')

                deadly_exits.get('spikes')['safe'] = True
                chests.get('marble')['room'] = room
                signs.get(room)['visible'] = True
                all_items.get('crown')['room'] = room
                room_items.append('crown')

                room_descriptions[room] = 'You are standing in the tomb of King Eldred. \
\nThere are 3 dials on the wall: the first copper, the second bronze and the third silver.\
\nEach dial has 3 settings: sun, crescent moon, and star.\
\nTo the east is a solid marble door.\
\nThe marble sarcophogus lid forms a safe bridge to cross a pit layered with spikes.'

    if 'turn' in user_command and 'dial' in user_command:
        if 'copper dial' in room_items:
            all_items_valid = True
            valid_dial = False
            if 'copper' in user_command or 'first' in user_command:
                if 'moon' in user_command:
                    all_items.get('copper dial')['status'] = 'moon'
                    print('The copper dial is now set to: moon')
                    valid_dial = True
                elif 'sun' in user_command:
                    all_items.get('copper dial')['status'] = 'sun'
                    print('The copper dial is now set to: sun')
                    valid_dial = True
                elif 'star' in user_command:
                    all_items.get('copper dial')['status'] = 'star'
                    print('The copper dial is now set to: star')
                    valid_dial = True

            elif 'bronze' in user_command or 'second' in user_command:
                if 'moon' in user_command:
                    all_items.get('bronze dial')['status'] = 'moon'
                    print('The bronze dial is now set to: moon')
                    valid_dial = True
                elif 'sun' in user_command:
                    all_items.get('bronze dial')['status'] = 'sun'
                    print('The bronze dial is now set to: sun')
                    valid_dial = True
                elif 'star' in user_command:
                    all_items.get('bronze dial')['status'] = 'star'
                    print('The bronze dial is now set to: star')
                    valid_dial = True

            elif 'silver' in user_command or 'third' in user_command:
                if 'moon' in user_command:
                    all_items.get('silver dial')['status'] = 'moon'
                    print('The silver dial is now set to: moon')
                    valid_dial = True
                elif 'sun' in user_command:
                    all_items.get('silver dial')['status'] = 'sun'
                    print('The silver dial is now set to: sun')
                    valid_dial = True
                elif 'star' in user_command:
                    all_items.get('silver dial')['status'] = 'star'
                    print('The silver dial is now set to: star')
                    valid_dial = True

            if valid_dial is True:
                copper_dial = all_items.get('copper dial').get('status')
                bronze_dial = all_items.get('bronze dial').get('status')
                silver_dial = all_items.get('silver dial').get('status')

                if copper_dial == 'moon' and bronze_dial == 'moon' and silver_dial == 'sun':
                    print('You hear a series of sharp clicks, followed by a low rumble as the solid marble door slowly \
swings open.')
                    print('Bright sunshine spills into the room from the exit to the east.')
                    doors.get('exit')['locked'] = False
                    doors.get('exit')['open'] = True


            else:
                print('You cannot turn the dial to that setting')




    if all_items_valid is False:
        print("It is not possible to do that. Perhaps you don't have all the items, or perhaps it just makes no sense!")


    return death



def display_inventory_description(inventory, all_items, gold):

        print('You are carrying:')
        for item_key in inventory:
            item = all_items.get(item_key)
            item_description = item.get('description')
            print(item_description)

        print('Gold: ' + str(gold))

def get_hint(room, hints, gold):
    hint = hints.get(room)

    if hint:
        hint_text = hint.get('hint')
        hint_cost = hint.get('cost')
        if gold >= hint_cost:
            print(hint_text)
            gold -= hint_cost
            print('The cost of that hint was ' + str(hint_cost) + ' gold. You have ' + str(gold) + ' remaining.')
        else:
            print('The hint costs ' + str(hint_cost) + ' gold but you only have ' + str(gold) + ' gold.')
    else:
        print('Sorry, no hints here.')

    return gold

def display_intro():
    print('')
    print('Welcome to The Legend of King Eldred')
    print('------------------------------------')
    print('')
    print("To play the game, just type a command e.g. 'north', 'look', 'give carrot to donkey'.")
    print("To see the full list of commands available, type 'help'.")
    print("If you get really stuck, type 'hint'. But hints are not free...")
    print('')
    print("Your task is to explore the village of Wildemoor and its icy dungeons to find the hidden treasure.")
    print("Your task is also to stay alive!")
    print('')
    print('------------------------------------')
    print('')
    print('For many years Wildemoor was ruled by King Eldred. Eldred was a popular king who was very ')
    print('generous to his subjects. When he died, King Eldred was buried in a sealed tomb beneath Wildemoor.')
    print('It is said he was buried with great treasures including his crown which, according to ')
    print('legend brings untold power and wealth to the wearer.')


def display_all_commands(commands):
    print('The commands you can use in Legend of King Eldred are:')
    print('north, south, east, west (or n, s, e, w)')
    print('help - displays all possible commands')
    print('inv - inventory')
    print('hint - get a hint for a small fee')
    print('take <item> - you never know when something might come in handy')
    print('drop <item> - maybe you know this will not come in handy')
    print('look - review what is in the current location')
    print('examine <item> - it is always a good idea to examine every item in Wildemoor')
    print('open <item> - good for chests and doors, but they have to be unlocked first')
    print('unlock <item> - unlock a door or a chest, but you will need the correct key or code')
    print('read sign - you never know what useful information will be displayed on a sign')
    print("talk to <person> - it's good to talk")
    print('smash <item> with <item> - occasionally a little bit of vandalism is necessary')
    print('dig <item> with <item> - you dig...?')
    print('burn <item> with <item> - handy for the budding arsonists out there')
    print('give <item> to <person> - you never know what you might get back')
    print('drink - being an adventurer can be thirsty work')
    print('fill <item> with <something>')
    print('say <something> to <person>')
    print('pull <item> - handy for levers, all levers in games are there to be pulled')
    print('pierce <item> with <item> - make a hole in something with a sharp object')
    print('oil <item> - always solves those rusty problems')
    print("turn <dial> to <setting> - no point in having a dial if you can't turn it")



if __name__ == "__main__":
    main()