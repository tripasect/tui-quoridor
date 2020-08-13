from math import ceil, floor
import numpy as np
import os
from time import sleep


def cls():
    """Wipes the screen altogether. Works on Linux BASH and Windows Command Line.
    Should also work on Mac OS, not sure."""
    os.system('cls' if os.name=='nt' else 'clear')


def set_up():
    "Sets all the global variables to their correct amount."

    # bringing globals in
    global turn, grid, players, N,\
    M, K, line, wall, row_labels, col_labels

    N = 8
    # length of the grid excluding the lines

    M = 2 * N + 1
    # length of the grid including the lines

    K = M - 1
    # the ordinal corresponding to the last cell in the grid
    # (for convinience of not having to substract 1 every time)

    grid = np.full((M, M), '+')
    # first making an array of '+'s with the shape (M, M)

    grid[1:-1:2, 1:-1:2] = np.full((N, N), ' ')
    # then replacing our free cells (which are for pawns to be at) with ' '

    # drawing the box with box-drawing characters
    grid[::2, :] = '─'
    grid[:, ::2] = '│'
    grid[2:M - 2:2, 2:M - 2:2] = '┼'
    grid[2::2, K] = '┤'
    grid[2::2, 0] = '├'
    grid[0, 0], grid[0, K], grid[K, 0], grid[K, K] = '┌', '┐', '└', '┘'
    grid[0, 2:-1:2] = '┬'
    grid[K, 2:-1:2] = '┴'

    # bringing all box characters to a single list for further checkings
    line = ['─', '│', '┼', '┌', '┐', '└', '┘', '┤', '┬', '├', '┴', '*']

    # bringing all wall characters to a single list for further checkings
    wall = ['x', 'X']

    # turn = 1 indicates player 0 turn and
    # turn = -1 indicates player 1 turn
    turn = 1

    # labels used to mark rows
    # extra ' ' at two ends are because no one needs to block a border so
    # no labels required to mark borders
    row_labels = [' '] + [chr(i) for i in range(65 + M - 3, 64, -1)] + [' ']

    # labels used to mark columns
    col_labels = [chr(i) for i in range(97, 97 + M - 2)]


    # a list of all the players as dictionaries of their
    # attributes such as symbol and walls left
    players = [
            {'symbol': 'B',
                'row': 1,
                'col': 2 * int(M / 4) + 1, # for setting the pawn at middle of the row
                'walls': 5},

            {'symbol': 'W',
                'row': -2,
                'col': 2 * int(M / 4) + 1, # for setting the pawn at middle of the row
                'walls': 5}
                ]
    refresh_grid()


def refresh_grid():
    "Updates grid according to the last pawn move."
    grid[players[0]['row'], players[0]['col']] = players[0]['symbol']
    grid[players[1]['row'], players[1]['col']] = players[1]['symbol']


def move(player, vector):
    "Moves player one cell with the vector given."
    before_row = player['row']
    before_col = player['col']
    # multiplies by two because we need to skip lines
    player['row'] -= 2 * vector[1]
    player['col'] += 2 * vector[0]
    refresh_grid()
    grid[before_row, before_col] = ' '


def display_turn():
    "Prints on the screen which player's turn it is."
    global players
    if turn == 1:
        print(f"""
\tTurn: BLACK
\tWalls Left: {players[0]['walls']}
\tOpponent Walls Left: {players[1]['walls']}""")
    elif turn == -1:
        print(f"""
\tTurn: WHITE
\tWalls Left: {players[1]['walls']}
\tOpponent Walls Left: {players[0]['walls']}""")
    else:
        pass


def char_to_vector(char):
    "Converts w, a, s, d to their appropriate vectors."
    if char == 'w':
        return [0, 1]
    elif char == 's':
        return [0, -1]
    elif char == 'a':
        return [-1, 0]
    elif char == 'd':
        return [1, 0]                   


def declare_winner(player):
    """Winner's pawn gets some beautiful asterisks ('*') to celebrate their
    winnership. Nice, eh?"""
    global grid, winner, M, players
    index = players.index(player)
    if index == 0:
        winner = players[0]
        r = M - 2
        c = players[0]['col']
        grid[r - 1:r + 2, c - 1:c + 2:2] = '*'
        grid[r, c] = players[0]['symbol']
    elif index == 1:
        winner = players[1]
        r = -M + 1
        c = players[1]['col']
        grid[r - 1:r + 2, c - 1:c + 2:2] = '*'
        grid[r, c] = players[1]['symbol']
    else:
        pass


def run():
    "The main function. All the good stuff happen here!"
    global winner
    if players[0]['row'] == M - 2:
        declare_winner(players[0])
        finish()
    elif players[1]['row'] == -M + 1:
        declare_winner(players[1])
        finish()
    else:
        global turn
        turn_index = int(-0.5 * turn + 0.5)
        cls()
        display()
        display_turn()
        inp = input(
        """\n\t\t[GUIDE]
        • w for moving your pawn UP
        • s for moving your pawn DOWN
        • a for moving your pawn LEFT
        • d for moving your pawn RIGHT
        • Use an uppercase and a lowercase
          letter for placing a wall in the
          relevant coordinates.
        Example 1: Bc (or cB)
        Example 2: iD (or Di)
> """)
        vect = char_to_vector(inp)
        if inp in ['w', 's', 'a', 'd']:
            vect = char_to_vector(inp)       
            if move_allowed(vect, players[turn_index]) == 'T':
                turn *= -1
                move(players[turn_index], vect)
                run()
            elif move_allowed(vect, players[turn_index]) == 'J':
                turn *= -1
                move(players[turn_index], [2*i for i in vect])
                run()
            else:
                warn("Incorrect! What are you missing?")
        else:
            if is_in_wall_position_format(inp):
                draw_wall(players[turn_index], inp)
                run()
            else:
                warn("Incorrect! What are you missing?")


def finish():
    """Brings game to a conclusion and asks the player whether
    they intend to do another game or not."""
    cls()
    display()
    winner_symbol = winner['symbol']
    print(f'{winner_symbol} has won! Congrats!')
    prompt = "Another hand? [Y/n]\n> "
    answer = input(prompt)
    if answer in ['Y', 'y', '']:
        set_up()
        run()
    else:
        quit()


def is_in_wall_position_format(place):
    "Decides whether its input has a form like 'iB' or not."
    if len(place) == 2 and place[0].isupper() and place[1].islower():
        upper = place[0]
        lower = place[1]
    elif len(place) == 2 and place[1].isupper() and place[0].islower():
        upper = place[1]
        lower = place[0]        
    else:
        return False
    if upper in row_labels[1:-1] and lower in col_labels:
        return True
    else:
        return False


def display():
    """Prints stuff on the screen in a pretty way."""
    i = 0
    for row in grid:
        print(row_labels[i], end=' ')
        i += 1
        for cell in row:
            if cell in [line[0], wall[0]]:
                print(5 * cell, sep='', end='')
            elif cell in line + wall:
                print(cell, sep='', end='')
            else:
                print('  ', cell, '  ', sep='', end='')
        print()
    final_label = '     '
    for char in col_labels:
        final_label += char + 2 * ' '
    print(final_label)


def move_allowed(vector, player):
    """Decides whether {player} is allowed to move with
    the vector {vector}.
    -- 'F' means not allowed,
    -- 'T' means allowed and
    -- 'J' means it is allowed but it has to jump over the
        opponents's pawn."""
    i, j = vector[0], vector[1]
    r = player['row']
    c = player['col']
    try:
        if i == 0 and j ** 2 == 1 and grid[r - 2 * j, c] == ' ' and\
            not wall_ahead(i, j, r, c):
            return 'T'
        elif j == 0 and i ** 2 == 1 and grid[r, c + 2 * i] == ' ' and\
            not wall_ahead(i, j, r, c):
            return 'T'        
        elif i == 0 and j ** 2 == 1 and grid[r - 2 * j, c] in ['B', 'W'] and\
            grid[r - 4 * j, c] == ' ' and\
            not wall_ahead(i, j, r, c):
            return 'J'
        elif j == 0 and i ** 2 == 1 and grid[r, c + 2 * i] in ['B', 'W'] and\
            grid[r, c + 4 * i] == ' ' and\
            not wall_ahead(i, j, r, c):
            return 'J'
        else:
            return 'F'
    # index error happens when it tries to check for a white space
    # outside of the grid. Of course it is a NO NOT ALLOWED when that happens!
    except IndexError:
        return 'F'


def wall_ahead(i, j, r, c):
    """Returns True if the object at [r, c] has a wall ahead of it
    if it intends to move with the vector [i, j]. False otherwise."""
    global grid
    ahead = grid[r - j, c + i]
    if 'x' in ahead or 'X' in ahead:
        return True
    else:
        return False


def label_to_tuple(place):
    "Converts a string looking like 'iB' to a tuple looking like (9, 4)."
    if len(place) == 2 and place[0].isupper() and place[1].islower():
        upper = place[0]
        lower = place[1]
    elif len(place) == 2 and place[1].isupper() and place[0].islower():
        upper = place[1]
        lower = place[0]        
    else:
        warn("Invalid place.")
    return (ord(lower) - 96, - ord(upper) + 80)


def warn(string):
    """Wipes screen and then shows the warning
    and then comes back to the game"""
    cls()
    print(string)
    sleep(1.5)
    run()


def draw_wall(player, place):
    """Draws a wall in the grid by {player} in the place {place}.
    {place} is a string looking like 'iB' (labels)."""
    global turn, grid, K
    if player['walls'] > 0:
        r = label_to_tuple(place)[1]
        c = label_to_tuple(place)[0]
        if r % 2 == 0 and c % 2 == 0:
            warn("You can't make walls at conjunctions!")
        elif r % 2 == 1 and c % 2 == 1:
            warn("You can't make walls on free spaces!")
        elif grid[r, c] in wall:
            warn("Wall is already establishid in there!")
        else:
            player['walls'] -= 1
            r = label_to_tuple(place)[1]
            c = label_to_tuple(place)[0]
            grid[r, c] = wall_char_from_line_char(grid[r, c])
            turn *= -1
    else:
        warn("You don't have any walls left! Try moving.")
    

def plain_display():
    """Designated for developing purposes. No use in the game.
    display() is used in the game."""
    for row in grid:
        for cell in row:
            print(cell, end='')
        print()


def wall_char_from_line_char(line_char):
    """Decides what wall character ('x' or 'X') should
    be chosen based on what line character (horizontal or vertical) it
    is going to replace."""
    global line, wall
    try:
        return wall[line.index(line_char)]
    except ValueError:
        return line_char


# Establishing a few global variables for the first time.
# Their values will be manipulated by functions.
N = None
M = None
grid = None
line = None
players = None
wall = None
winner = None
turn = None
row_labels = None
col_labels = None


# First run of the game
set_up()
refresh_grid()
run()