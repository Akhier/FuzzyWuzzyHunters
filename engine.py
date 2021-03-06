import libtcodpy as libtcod

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from input_handlers import (
    handle_keys, handle_mouse, handle_main_menu, handle_weapon_menu)
from loader_functions.initialize_new_game import (
    get_constants, get_game_variables)
from loader_functions.data_loaders import load_game, save_game
from menus import menu, main_menu, message_box
from render_functions import clear_all, render_all


def play_game(player, entities, game_map, message_log,
              game_state, con, panel, constants):
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None
    moved = False

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(
            libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(
                fov_map, player.x, player.y, constants['fov_radius'],
                constants['fov_light_walls'], constants['fov_algorithm'])

        render_all(
            con, panel, entities, player, game_map, fov_map, fov_recompute,
            message_log, constants['screen_width'], constants['screen_height'],
            constants['bar_width'], constants['panel_height'],
            constants['panel_y'], mouse, constants['colors'], game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        if (game_state == GameStates.PLAYERS_TURN and
                not moved and constants['weapon'] == 'daggers'):
            player.fighter.dodge_chance = 0
        elif (game_state == GameStates.PLAYERS_TURN and
              moved and constants['weapon'] == 'sword'):
            player.fighter.dodge_chance = 0

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(
                    entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                    if constants['weapon'] == 'sword':
                        player.fighter.dodge_chance = 50
                    moved = False
                else:
                    player.move(dx, dy)

                    if constants['weapon'] == 'daggers':
                        if player.fighter.dodge_chance < 25:
                            player.fighter.dodge_chance += 5
                        if dx == -1 and dy == -1:
                            tx1 = destination_x
                            ty1 = destination_y + 1
                            tx2 = destination_x + 1
                            ty2 = destination_y
                        elif dx == 0 and dy == -1:
                            tx1 = destination_x - 1
                            ty1 = destination_y
                            tx2 = destination_x + 1
                            ty2 = destination_y
                        elif dx == 1 and dy == -1:
                            tx1 = destination_x - 1
                            ty1 = destination_y
                            tx2 = destination_x
                            ty2 = destination_y + 1
                        elif dx == 1 and dy == 0:
                            tx1 = destination_x
                            ty1 = destination_y - 1
                            tx2 = destination_x
                            ty2 = destination_y + 1
                        elif dx == 1 and dy == 1:
                            tx1 = destination_x
                            ty1 = destination_y - 1
                            tx2 = destination_x - 1
                            ty2 = destination_y
                        elif dx == 0 and dy == 1:
                            tx1 = destination_x + 1
                            ty1 = destination_y
                            tx2 = destination_x - 1
                            ty2 = destination_y
                        elif dx == -1 and dy == 1:
                            tx1 = destination_x + 1
                            ty1 = destination_y
                            tx2 = destination_x
                            ty2 = destination_y - 1
                        else:
                            tx1 = destination_x
                            ty1 = destination_y + 1
                            tx2 = destination_x
                            ty2 = destination_y - 1

                        target = get_blocking_entities_at_location(
                            entities, tx1, ty1)
                        if target:
                            attack_results = player.fighter.attack(target)
                            player_turn_results.extend(attack_results)
                        target = get_blocking_entities_at_location(
                            entities, tx2, ty2)
                        if target:
                            attack_results = player.fighter.attack(target)
                            player_turn_results.extend(attack_results)

                    fov_recompute = True
                    moved = True

                if constants['weapon'] == 'pike':
                    destination_x += dx
                    destination_y += dy
                    if not target:
                        target = get_blocking_entities_at_location(
                            entities, destination_x, destination_y)
                        if target:
                            attack_results = player.fighter.attack(target)
                            player_turn_results.extend(attack_results)
                    destination_x += dx
                    destination_y += dy
                    target = get_blocking_entities_at_location(
                        entities, destination_x, destination_y)
                    if target:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)

                game_state = GameStates.ENEMY_TURN

        elif wait:
            game_state = GameStates.ENEMY_TURN
            moved = False

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if (entity.item and entity.x == player.x and
                        entity.y == player.y):
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    moved = False

                    break
            else:
                message_log.add_message(
                    Message('There is nothing here to pick up.',
                            libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if (inventory_index is not None and
                previous_game_state != GameStates.PLAYER_DEAD and
                inventory_index < len(player.inventory.items)):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(
                    item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if (entity.stairs and entity.x == player.x and
                        entity.y == player.y):
                    entities = game_map.next_floor(
                        player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)
                    moved = True

                    break
            else:
                message_log.add_message(
                    Message('There are no stairs here.', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1

            game_state = previous_game_state

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(
                    targeting_item, entities=entities, fov_map=fov_map,
                    target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state in (
                    GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY,
                    GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(
                    player, entities, game_map, message_log, game_state)

                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message, fuzzydied = kill_monster(dead_entity)
                    fov_recompute = True

                message_log.add_message(message)
                if fuzzydied:
                    message_log.add_message(Message(
                        'Fuzzy Wuzzy wasn\'t very fuzzy was he? ' +
                        'Congratulations on a succesfull hunt! You win!',
                        libtcod.green))
                    game_state = GameStates.PLAYER_DEAD

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(
                    Message('You gain {0} experience points.'.format(xp)))

                if leveled_up:
                    message_log.add_message(
                        Message('Your battle skills grow stronger! ' +
                                'You reached level {0}'.format(
                                    player.level.current_level) + '!',
                                libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(
                        player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


def main():
    constants = get_constants()

    libtcod.console_set_custom_font(
        'arial10x10.png',
        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(
        constants['screen_width'], constants['screen_height'],
        constants['window_title'], False)

    con = libtcod.console_new(
        constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(
        constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    get_weapon = False
    show_load_error_message = False

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(
            libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(
                con, None, constants['screen_width'],
                constants['screen_height'])

            if show_load_error_message:
                message_box(
                    con, 'No save game to load', 50,
                    constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (
                    new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = (
                    get_game_variables(constants))
                get_weapon = True
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = (
                        load_game())
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        elif get_weapon:
            menu(
                con, 'Choose Weapon',
                ['Sword and Board (Chance to block when fighting straight on)',
                 'Daggers (Gets a sneaky stab in and can dodge when moving)',
                 'Pike (Attacks twice as far as other weapons)'],
                64, constants['screen_width'], constants['screen_height'])
            libtcod.console_flush()

            action = handle_weapon_menu(key)
            exit = action.get('exit')
            sword = action.get('sword')
            daggers = action.get('daggers')
            pike = action.get('pike')

            if exit:
                libtcod.console_clear(0)
                show_main_menu = True
                get_weapon = False
            elif sword:
                get_weapon = False
                constants['weapon'] = 'sword'
            elif daggers:
                get_weapon = False
                constants['weapon'] = 'daggers'
            elif pike:
                get_weapon = False
                constants['weapon'] = 'pike'

        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log,
                      game_state, con, panel, constants)

            libtcod.console_clear(0)
            libtcod.console_flush()
            show_main_menu = True


if __name__ == '__main__':
    main()
