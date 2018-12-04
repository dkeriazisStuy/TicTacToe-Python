''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# layouts look like "_x_ox__o_"

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {} # this is a dictionary with key = a layout, and value = its corresponding BoardNode

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endState = None # if this is a terminal board, endState == 'x' or 'o' for wins, of 'd' for draw, else None
        self.parents = [] # all layouts that can lead to this one, by one move
        self.children = [] # all layouts that can be reached with a single move

    def print_me(self):
        print ('layout:',self.layout, 'endState:',self.endState)
        print ('parents:',self.parents)
        print ('children:',self.children)

def get_next_player(layout):
    num_xs = layout.count('x')
    num_os = layout.count('o')
    if num_xs == num_os:
        return 'x'
    else:
        return 'o'


def set_end_state(b):
    layout = b.layout
    for win in Wins:
        plays = set(layout[i] for i in win)
        if plays == {'x'}:
            b.endState = 'x'
            return True
        elif plays == {'o'}:  # X or O wins
            b.endState = 'o'
            return True

    if layout.count('_') == 0:  # No blanks, tie
        b.endState = 'd'
        return True

    return False


def CreateAllBoards(layout,parent):
    # recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary
    b = BoardNode(layout)
    if parent is not None:
        b.parents.append(parent)
    AllBoards[layout] = b
    next_player = get_next_player(layout)
    if set_end_state(b):
        return b
    for i, c in enumerate(layout):
        if c != '_':
            continue
        new_layout = layout[:i] + next_player + layout[i+1:]
        b.children.append(CreateAllBoards(new_layout, b))
    return b


def num_descendants(layout):
    num = 1
    for b in AllBoards[layout].children:
        num += num_descendants(b.layout)
    return num


def children():
    num = 0
    for b in AllBoards.values():
        num += len(b.children)
    return num


def stats():
    num_x_wins = 0
    num_o_wins = 0
    num_draws = 0
    num_not_end = 0
    for b in AllBoards.values():
        if b.endState == 'x':
            num_x_wins += 1
        elif b.endState == 'o':
            num_o_wins += 1
        elif b.endState == 'd':
            num_draws += 1
        else:
            num_not_end += 1
    return num_x_wins, num_o_wins, num_draws, num_not_end


if __name__ == "__main__":
    empty = '_________'
    CreateAllBoards(empty, None)
    print('all boards:', len(AllBoards))
    print('all children:', children())
    x, o, d, not_end = stats()
    print('x wins:', x)
    print('o wins:', o)
    print('draws:', d)
    print('not end:', not_end)

