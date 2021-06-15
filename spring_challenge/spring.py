import sys
import math
import numpy as np
from enum import Enum
import random as rnd

params = {
    'write_input': False,
    'my_trees_length': 7,
    'chop_center_tree': 21,
    'chop_center_3leaf': 10,  # 10?
    'chop_tree': 12,
    'stop_seed': 15
}


class Cell:
    def __init__(self, cell_index_, richness_, neighbors):
        self.cell_index = cell_index_
        self.richness = richness_
        self.neighbors = neighbors
        self.tree = None


class Tree:
    def __init__(self, cell_index_, size_, is_mine_, is_dormant_):
        self.cell_index = cell_index_
        self.size = size_
        self.is_mine = bool(is_mine_)
        self.is_dormant = bool(is_dormant_)


class ActionType(Enum):
    WAIT = "WAIT"
    SEED = "SEED"
    GROW = "GROW"
    COMPLETE = "COMPLETE"


class Action:
    def __init__(self, type_, idx, target_cell_id=None, origin_cell_id=None):
        self.idx = idx
        self.type = type_
        self.target_cell_id = target_cell_id
        self.origin_cell_id = origin_cell_id
        self.score = 0
        self.cost = 0
        self.disabled = False

    def __str__(self):
        if self.type == ActionType.WAIT:
            return 'WAIT'
        elif self.type == ActionType.SEED:
            return f'SEED {self.origin_cell_id} {self.target_cell_id}'
        else:
            return f'{self.type.name} {self.target_cell_id}'

    @staticmethod
    def parse(action_string, idx):
        split = action_string.split(' ')
        if split[0] == ActionType.WAIT.name:
            return Action(ActionType.WAIT, idx)
        if split[0] == ActionType.SEED.name:
            return Action(ActionType.SEED, idx, int(split[2]), int(split[1]))
        if split[0] == ActionType.GROW.name:
            return Action(ActionType.GROW, idx, int(split[1]))
        if split[0] == ActionType.COMPLETE.name:
            return Action(ActionType.COMPLETE, idx, int(split[1]))


class Game:
    def __init__(self):
        self.day = 0
        self.day_part = 0
        self.counter = 0
        self.nutrients = 0
        self.board = []
        self.trees = []
        self.possible_actions = []
        self.action_types = []
        self.my_sun = 0
        self.my_score = 0
        self.opponent_sun = 0
        self.opponent_score = 0
        self.opponent_is_waiting = False
        self.enable = {
            'complete': False,
            'grow': False,
            'seed': False
        }
        self.max_score = {
            'complete': -math.inf,
            'grow': -math.inf,
            'seed': -math.inf,
        }
        self.game_state = {
            'can_seed_center': False,
            'can_seed_center_next_turn': False,
            'center_full': False,
            'stop_seed': False,
            'new_seed_in_center': False,
            'have_center_tree': False,
            'enough_tree': False
        }

    def get_next_action(self):
        self.print_game()

        self.get_action_types()

        self.score()

        self.get_max_scores()

        self.get_game_state()

        print(f'# action_types: {self.action_types}', file=sys.stderr, flush=True)

        print(f'# max_scores: {self.max_score}', file=sys.stderr, flush=True)

        self.get_valid_actions()

        print(f'# valid_actions: {self.enable}', file=sys.stderr, flush=True)

        self.print_possible_actions()

        idx = 0

        if self.enable['complete']:
            idx = self.get_max_score_idx(ActionType.COMPLETE, self.max_score['complete'])
        elif self.enable['grow']:
            idx = self.get_max_score_idx(ActionType.GROW, self.max_score['grow'])
        elif self.enable['seed']:
            idx = self.get_max_score_idx(ActionType.SEED, self.max_score['seed'])

        return self.possible_actions[idx]

    def score(self):
        for action in self.possible_actions:
            if action.type == ActionType.COMPLETE:
                self.get_complete_scores(action)
            elif action.type == ActionType.GROW:
                self.get_grow_scores(action)
            elif action.type == ActionType.SEED:
                self.get_seed_scores(action)

    def get_seed_scores(self, action):
        cell = self.board[action.target_cell_id]

        action.score = cell.richness

        # center cell
        if action.target_cell_id == 0:
            action.score += 1

    def get_grow_scores(self, action):
        cell = self.board[action.target_cell_id]

        # add richness
        grow_outer = \
            self.game_state["center_full"] \
            and (self.game_state["have_2nd_growable_tree"] or self.game_state["have_3rd_growable_tree"])
        if grow_outer and cell.cell_index > 6:
            action.score += cell.richness + 6
            # outer_grow = \
            #     any(action.type == ActionType.GROW and action.target_cell_id > 6 for action in self.possible_actions)
            # if not outer_grow:
            #     self.enable['grow'] = False
            # return
        else:
            action.score += cell.richness

        next_spooky_score = self.get_spooky_score(action.target_cell_id, 1)

        # add spooky
        action.score += next_spooky_score

        # can seed central
        if self.tree_can_seed_center(cell.tree, True):
            action.score += 1

        # add central cell
        if action.target_cell_id == 0:
            action.score += 1

        # add tree size
        action.score += cell.tree.size

    def get_complete_scores(self, action):
        cell = self.board[action.target_cell_id]

        not_chop_tree_size = cell.tree.size < 3
        not_chop_center_tree = action.target_cell_id == 0 and self.day < params['chop_center_tree']
        not_chop_3leaf = 6 >= action.target_cell_id > 0 and self.day < params['chop_center_3leaf']
        not_chop_day = action.target_cell_id > 6 and self.day < params['chop_tree']

        action.disabled = not_chop_tree_size or not_chop_center_tree or not_chop_3leaf or not_chop_day

        # print(f'# COMPLETE disabled', file=sys.stderr, flush=True)

        next_spooky_score = self.get_spooky_score(action.target_cell_id, -3)

        # add spooky
        action.score += next_spooky_score

        # add richness
        action.score += cell.richness

        # add central cell
        if action.target_cell_id <= 6:
            action.score += 1

    def get_shadow_cells_idx(self, tree):
        opposite_dirs_set = (3, 4, 5, 0, 1, 2)
        sun_direction = (self.day_part + 1) % 6
        opposite_sun_direction = opposite_dirs_set[sun_direction]

        shadow_cell_indexes_ = []

        for idx in range(3):

            if len(shadow_cell_indexes_) == 0:
                shadow_cell_indexes_.append(self.board[tree.cell_index].neighbors[opposite_sun_direction])
            elif shadow_cell_indexes_[idx - 1] > -1:
                shadow_cell_indexes_.append(self.board[shadow_cell_indexes_[idx - 1]].neighbors[opposite_sun_direction])
            else:
                break

        shadow_cell_indexes_ = [idx for idx in shadow_cell_indexes_ if idx > -1]

        return shadow_cell_indexes_

    def get_spooky_trees_idx(self, tree_cell_index, grow):
        spooky_trees_idx = []

        if tree_cell_index is not None:
            self.board[tree_cell_index].tree.size += grow

        for tree in self.trees:

            if tree.size > 0:
                shadow_cell_indexes = self.get_shadow_cells_idx(tree)

                # print(f'# tree: {tree.cell_index}', file=sys.stderr, flush=True)
                # print(f'# shadow_cells {shadow_cell_indexes}', file=sys.stderr, flush=True)

                for shadow_size in range(len(shadow_cell_indexes)):
                    idx = shadow_cell_indexes[shadow_size]
                    # print(f'# idx: {idx}', file=sys.stderr, flush=True)
                    shadow_tree = self.board[idx].tree
                    if shadow_tree is not None and shadow_tree.size >= tree.size and shadow_tree.size >= shadow_size + 1:
                        spooky_trees_idx.append(tree.cell_index)

        if tree_cell_index is not None:
            self.board[tree_cell_index].tree.size -= grow

        # print(f'# tree: {tree_cell_index} grow: {grow}', file=sys.stderr, flush=True)
        # print(f'# spooky_trees: {spooky_trees_idx}', file=sys.stderr, flush=True)

        return spooky_trees_idx

    def get_spooky_score(self, tree_cell_index, grow):
        spooky_trees_idx = self.get_spooky_trees_idx(tree_cell_index, grow)

        score_ = 0

        if len(spooky_trees_idx) > 0:
            for idx in spooky_trees_idx:
                tree = self.board[idx].tree

                if tree is not None:
                    # print(f'# spooky_tree_size: {tree.size}', file=sys.stderr, flush=True)
                    if tree.is_mine:
                        score_ -= tree.size
                    else:
                        score_ += tree.size

        return score_

    def get_action_types(self):
        all_types = [action.type for action in self.possible_actions]
        action_types = set(all_types)

        self.action_types = action_types

        for action_type in self.action_types:
            if action_type == ActionType.COMPLETE:
                self.enable['complete'] = True
            elif action_type == ActionType.GROW:
                self.enable['grow'] = True
            elif action_type == ActionType.SEED:
                self.enable['seed'] = True

    def get_max_scores(self):
        for action_type in self.action_types:
            if action_type == ActionType.COMPLETE:
                self.max_score['complete'] = self.get_max_score(ActionType.COMPLETE)
            elif action_type == ActionType.GROW:
                self.max_score['grow'] = self.get_max_score(ActionType.GROW)
            elif action_type == ActionType.SEED:
                self.max_score['seed'] = self.get_max_score(ActionType.SEED)

    def get_max_score(self, action_type):
        max_score = max(action.score for action in self.possible_actions
                        if action.type == action_type)

        return max_score

    def get_max_score_idx(self, action_type, max_score):
        actions = [action for action in self.possible_actions
                   if action.type == action_type and action.score == max_score and not action.disabled]

        if len(actions) > 0:
            target_cell = min(action.target_cell_id for action in actions)

            print(f'# action: {action_type} max_score_target_cell: {target_cell}', file=sys.stderr, flush=True)

            action = [action for action in actions if action.target_cell_id == target_cell][0]

            return action.idx

        else:
            return 0

    def have_tree(self, richness_, size_):

        for tree in self.trees:
            if tree.is_mine and not tree.is_dormant \
                    and self.board[tree.cell_index].richness == richness_ and tree.size == size_:
                return True

        return False

    def get_game_state(self):
        self.game_state["can_seed_center"] = self.can_seed_center()
        self.game_state["can_seed_center_next_turn"] = self.can_seed_center(True)
        self.game_state["center_full"] = self.center_full()
        self.game_state["stop_seed"] = self.day >= params["stop_seed"]
        self.game_state["chop_tree"] = self.day >= params["chop_tree"]
        self.game_state["chop_center_3leaf"] = self.day >= params["chop_center_3leaf"]
        self.game_state["chop_center_tree"] = self.day >= params["chop_center_tree"]
        self.game_state["new_seed_in_center"] = self.have_tree(3, 0)
        self.game_state["have_center_growable_tree"] = \
            self.game_state["new_seed_in_center"] or self.have_tree(3, 1) or self.have_tree(3, 2)
        self.game_state["have_2nd_growable_tree"] = self.have_tree(2, 0) or self.have_tree(2, 1) or self.have_tree(
            2, 2)
        self.game_state["have_3rd_growable_tree"] = self.have_tree(1, 0) or self.have_tree(1, 1) or self.have_tree(
            1, 2)
        self.game_state["have_growable_tree"] = \
            self.game_state["have_center_growable_tree"] \
            or self.game_state["have_2nd_growable_tree"] \
            or self.game_state["have_3rd_growable_tree"]

    def have_grow_sun_points(self, size_):
        number_of_trees_ = 0
        cost_array = [1, 3, 7]
        for tree in self.trees:
            if tree.is_mine and tree.size == size_:
                number_of_trees_ += 1
        cost = number_of_trees_ + cost_array[size_]

        return self.my_sun >= cost

    def get_valid_actions(self):

        my_trees_length = len([tree for tree in self.trees if tree.is_mine])
        self.game_state['enough_tree'] = my_trees_length >= params['my_trees_length']

        for action_type in self.action_types:

            if action_type == ActionType.COMPLETE:
                if all(action.disabled for action in self.possible_actions if action.type == ActionType.COMPLETE):
                    self.enable['complete'] = False

            elif action_type == ActionType.GROW:

                # can seed center
                can_seed_center_ = not self.game_state['center_full'] and self.game_state['can_seed_center'] and \
                                   self.game_state['stop_seed']

                if can_seed_center_ and not self.game_state['new_seed_in_center']:
                    self.enable['grow'] = False

                have_outer_tree = self.game_state["have_2nd_growable_tree"] or self.game_state["have_3rd_growable_tree"]

                print(f'# center_full: {self.game_state["center_full"]}', file=sys.stderr, flush=True)
                print(f'# outer_tree: {have_outer_tree}', file=sys.stderr, flush=True)
                print(f'# chop_tree: {self.game_state["chop_tree"]}', file=sys.stderr, flush=True)
                print(f'# have_grow_sun_points: {self.have_grow_sun_points(2)}', file=sys.stderr, flush=True)

                if self.game_state['center_full'] and have_outer_tree \
                        and not self.have_grow_sun_points(2) \
                        and not self.game_state["chop_tree"] and not self.game_state['new_seed_in_center']:
                    self.enable['grow'] = False

            elif action_type == ActionType.SEED:

                # print(f'# DAY: {self.day <= 1 and self.day_part <= 1}', file=sys.stderr, flush=True)

                if self.game_state["stop_seed"] or self.game_state["enough_tree"]:
                    self.enable['seed'] = False
                    # print(f'# SEED_1: {self.enable["seed"]}', file=sys.stderr, flush=True)

                elif self.game_state['center_full'] and self.game_state['have_center_tree']\
                        and self.game_state["enough_tree"]:
                    self.enable['seed'] = False
                    # print(f'# SEED_2: {self.enable["seed"]}', file=sys.stderr, flush=True)

                # no seeding in first round
                elif self.day <= 1 and self.day_part <= 1:
                    self.enable['seed'] = False
                    # print(f'# SEED_3: {self.enable["seed"]}', file=sys.stderr, flush=True)

                # if grow -> can seed center
                elif not self.game_state['can_seed_center']:
                    if self.game_state['can_seed_center_next_turn']:
                        self.enable['seed'] = False
                        # print(f'# SEED_4: {self.enable["seed"]}', file=sys.stderr, flush=True)

    def center_full(self):
        cell_counter = 0

        for idx in range(7):
            if self.board[idx].tree is not None or self.board[idx].richness == 0:
                cell_counter += 1

        return cell_counter == 7

    def tree_can_seed_center(self, tree, grow=False):
        neighbours_idx = []
        tree_size = tree.size

        if grow:
            tree_size += 1

        if tree_size == 0:
            return False
        elif tree_size == 3:
            return True

        neighbours_idx = neighbours_idx + self.board[tree.cell_index].neighbors
        neighbours_idx = [idx for idx in neighbours_idx if idx > -1]

        if tree_size == 2:
            for idx in neighbours_idx:
                neighbours_idx = neighbours_idx + self.board[idx].neighbors

        neighbours_idx = set(neighbours_idx)

        neighbours_idx = [idx for idx in neighbours_idx if idx > -1]

        center_neighbours = set([self.board[idx] for idx in neighbours_idx if 6 >= idx >= 0])

        can_seed = any(cell.tree is None and cell.richness > 0
                       for cell in center_neighbours)

        # print(f'# tree: {tree.cell_index} CAN_SEED {can_seed}', file=sys.stderr, flush=True)

        return can_seed

    def can_seed_center(self, grow=False):
        if grow:
            for tree in self.trees:
                if tree.is_mine:
                    if self.tree_can_seed_center(tree, grow):
                        return True
        else:
            for tree in self.trees:
                if tree.is_mine and tree.size > 0 and not tree.is_dormant:
                    if self.tree_can_seed_center(tree):
                        return True

        return False

    def reset_cell_tree(self):
        for cell in self.board:
            cell.tree = None

    def print_possible_actions(self):
        for action in self.possible_actions:
            print(f'# action: {action}: {action.score} {action.disabled}', file=sys.stderr, flush=True)
        if not params['write_input']:
            print(f'######### \n', file=sys.stderr, flush=True)

    def print_game(self):
        print(f'# day: {self.day} counter: {self.counter} day_part: {self.day_part}', file=sys.stderr, flush=True)
        # print(f'# nutrients: {self.nutrients}', file=sys.stderr, flush=True)
        # print(f'# my_sun: {self.my_sun}', file=sys.stderr, flush=True)
        print(f'# my_score: {self.my_score}', file=sys.stderr, flush=True)
        # print(f'# opponent_sun: {self.opponent_sun}', file=sys.stderr, flush=True)
        print(f'# opponent_score: {self.opponent_score}', file=sys.stderr, flush=True)
        print(f'# opponent_is_waiting: {self.opponent_is_waiting}', file=sys.stderr, flush=True)
        if not params['write_input']:
            print(f'######### \n', file=sys.stderr, flush=True)


number_of_cells = int(input())
if params['write_input']:
    print(f'{number_of_cells}', file=sys.stderr, flush=True)

game = Game()

# input board info
for i in range(number_of_cells):
    cell_index, richness, neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5 = [int(j) for j in input().split()]

    if params['write_input']:
        print(f'{cell_index} {richness} {neigh_0} {neigh_1} {neigh_2} {neigh_3} {neigh_4} {neigh_5}',
              file=sys.stderr, flush=True)

    game.board.append(Cell(cell_index, richness, [neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5]))

opponent_move = None

while True:
    # input data, modify game class
    try:
        day_ = int(input())
        if params['write_input']:
            print(f'{day_}', file=sys.stderr, flush=True)
        game.day = day_
        game.day_part = day_ % 6
        nutrients = int(input())
        if params['write_input']:
            print(f'{nutrients}', file=sys.stderr, flush=True)
        game.nutrients = nutrients
        sun, score = [int(i) for i in input().split()]
        if params['write_input']:
            print(f'{sun} {score}', file=sys.stderr, flush=True)
        game.my_sun = sun
        game.my_score = score
        opp_sun, opp_score, opp_is_waiting = [int(i) for i in input().split()]
        if params['write_input']:
            print(f'{opp_sun} {opp_score} {opp_is_waiting}', file=sys.stderr, flush=True)
        game.opponent_sun = opp_sun
        game.opponent_score = opp_score
        game.opponent_is_waiting = bool(opp_is_waiting)
        number_of_trees = int(input())
        if params['write_input']:
            print(f'{number_of_trees}', file=sys.stderr, flush=True)
        game.trees.clear()
        game.reset_cell_tree()
        for i in range(number_of_trees):
            inputs = input().split()
            cell_index = int(inputs[0])
            size = int(inputs[1])
            is_mine = int(inputs[2])
            is_dormant = int(inputs[3])
            if params['write_input']:
                print(f'{cell_index} {size} {is_mine} {is_dormant}', file=sys.stderr, flush=True)
            game.board[cell_index].tree = Tree(cell_index, size, is_mine, is_dormant)
            game.trees.append(Tree(cell_index, size, is_mine, is_dormant))

        number_of_possible_actions = int(input())
        if params['write_input']:
            print(f'{number_of_possible_actions}', file=sys.stderr, flush=True)
        game.possible_actions.clear()
        for i in range(number_of_possible_actions):
            possible_action = input()
            if params['write_input']:
                print(f'{possible_action}', file=sys.stderr, flush=True)
            game.possible_actions.append(Action.parse(possible_action, i))

        game.enable['complete'] = False
        game.enable['grow'] = False
        game.enable['seed'] = False

        game.max_score['complete'] = -math.inf
        game.max_score['grow'] = -math.inf
        game.max_score['seed'] = -math.inf

    except EOFError:
        break

    next_action = game.get_next_action()

    game.counter += 1

    print(next_action)
