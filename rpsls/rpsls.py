import sys

n = int(input())

RULE = ['R', 'P', 'C', 'S', 'L']
RULE_LENGTH = 5


class Player:
    def __init__(self, id_, move):
        self.id = id_
        self.move = RULE.index(move)
        self.win = None
        self.opponents = []


def get_data():
    players_ = []

    for i in range(n):
        inputs = input().split()
        player_id = int(inputs[0])
        player_move = inputs[1]

        players_.append(Player(player_id, player_move))

    return players_


def get_result(a_player, b_player):
    a_player.win = None
    b_player.win = None

    if a_player.move == b_player.move:
        if a_player.id < b_player.id:
            a_player.win = True
            b_player.win = False
        else:
            a_player.win = False
            b_player.win = True

    else:
        if (a_player.move - b_player.move) % 5 in [1, 3]:
            a_player.win = True
            b_player.win = False

    if not a_player.win:
        a_player.win = False
        b_player.win = True

    a_player.opponents.append(str(b_player.id))
    b_player.opponents.append(str(a_player.id))


def get_current_matches(players_):
    for i in range(0, len(players_) - 1, 2):
        get_result(players_[i], players_[i + 1])


players = get_data()

while len(players) > 1:
    get_current_matches(players)
    players = [player for player in players if player.win is True]

print(players[0].id)
print(' '.join(players[0].opponents))
