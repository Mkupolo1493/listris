from random import choice as pick, randint as rng
from bitmaps import piece_bmps
piece = [
    [0]
]
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
x = 3
y = 0
r = 0

standalone = False
if __name__ == "__main__":
    standalone = True
log = standalone

def move_right():
    global x
    x += 1
    if log: print("Moving right... x is now " + str(x))
    if collides():
        x -= 1
        if log: print("Could not move right. Returning to x = " + str(x))
def move_left():
    global x
    x -= 1
    if log: print("Moving left... x is now " + str(x))
    if collides():
        x += 1
        if log: print("Could not move left. Returning to x = " + str(x))
class CementRequest(Exception):
    pass
def soft_drop(direct=True):
    global y
    y += 1
    if direct and log: print("Moving down... y is now " + str(y))
    if collides():
        y -= 1
        if direct and standalone:
            if log: print("Could not move down. Cementing at y = " + str(y))
            cement()
        else:
            if direct and log: print("Could not move down. Raising cement request at y = " + str(y))
            raise CementRequest()
def firm_drop(direct=True):
    try:
        while y < 20:
            soft_drop(False)
    except CementRequest:
        if direct and log: print("Firm dropped! y is now " + str(y))
def hard_drop():
    firm_drop(False)
    if standalone:
        if log: print("Hard dropped! Cementing at y = " + str(y))
        cement()
    else:
        if log: print("Hard dropped! Raising cement request at y = " + str(y))
        raise CementRequest()
def rotate_cw(on_collide="undo"):
    global piece
    global r
    piece_copy = []
    for sy, row in enumerate(piece):
        piece_copy.append([])
        for sx, mino in enumerate(row):
            piece_copy[sy].append(piece[len(piece) - 1 - sx][sy])
    piece = piece_copy
    r = (r + 1) % 4
    if log: print(f"Rotated bitmap clockwise. Now {r} ({piece}).")
    if on_collide == "ignore": return
    if collides():
        if on_collide == "crash": raise Exception("Piece stuck! Aborting infinite loop...")
        if log: print("Failed rotation, rotating back counterclockwise...")
        rotate_ccw("crash")
def rotate_ccw(on_collide="undo"):
    global piece
    global r
    piece_copy = []
    for sy, row in enumerate(piece):
        piece_copy.append([])
        for sx, mino in enumerate(row):
            piece_copy[sy].append(piece[sx][len(piece) - 1 - sy])
    piece = piece_copy
    r = (r - 1) % 4
    if log: print(f"Rotated bitmap counterclockwise. Now {r} ({piece}).")
    if on_collide == "ignore": return
    if collides():
        if on_collide == "crash": raise Exception('Collided with on_collide set to "crash"')
        if log: print("Failed rotation, rotating back clockwise...")
        rotate_cw("crash")
def set_rotation(new_r):
    diff = (new_r - r) % 4
    if not diff:
        return
    if diff == 3:
        rotate_ccw("crash")
        return
    if diff == 2:
        rotate_cw("ignore")
    rotate_cw("crash")
def collides():
    for sy, row in enumerate(piece):
        for sx, mino in enumerate(row):
            if not mino: continue
            if x + sx < 0 or x + sx > 9 or y + sy >= len(board) or board[y + sy][x + sx]: return True
    return False
def cement(new_piece=[[0]], zone_style=False): # zone_style moves full lines under the board instead of deleting them.
    global piece
    global x
    global y
    global r
    for sy, row in enumerate(piece):
        for sx, mino in enumerate(row):
            if mino: board[y + sy][x + sx] = 1 # if statement to prevent IndexError
    rows_to_delete = []
    for ry, row in enumerate(board):
        clear = True
        if not 0 in row: rows_to_delete.append(ry)
    if zone_style:
        for row in reversed(rows_to_delete):
            del board[row]
            board.append([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
            if log: print("Zone-style cleared line " + str(row + 1))
    else:
        for row in rows_to_delete:
            del board[row]
            board.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            if log: print("Cleared line " + str(row + 1))
    if standalone:
        if rng(64, 70) == 69: # 1 in 7 chance
            piece = [[1,1],[1,1]] # O
        else:
            piece = pick([
                [
                    [0, 0, 0, 0], #
                    [1, 1, 1, 1], # I
                    [0, 0, 0, 0], #
                    [0, 0, 0, 0]  #
                ],
                [
                    [1, 0, 0], #
                    [1, 1, 1], # J
                    [0, 0, 0]  #
                ],
                [
                    [0, 0, 1], #
                    [1, 1, 1], # L
                    [0, 0, 0]  #
                ],
                [
                    [0, 1, 1], #
                    [1, 1, 0], # S
                    [0, 0, 0]  #
                ],
                [
                    [0, 1, 0], #
                    [1, 1, 1], # T
                    [0, 0, 0]  #
                ],
                [
                    [1, 1, 0], #
                    [0, 1, 1], # Z
                    [0, 0, 0]  #
                ]
            ])
    else:
        piece = new_piece
    x = (10 - len(piece[0])) // 2 # spawn centered, or slightly to the left if impossible
    y = 0
    r = 0
if standalone: cement()
def display_board(dont_print=False):
    global y
    real_y = y
    firm_drop(False)
    shadow_y = y
    y = real_y
    result = ""
    result += "█" * 28 + "\n██" + " " * 24 + "██\n"
    for sy, row in enumerate(board):
        result += "██  "
        for sx, tile in enumerate(row):
            is_piece_mino = False
            is_shadow_mino = False
            if sx - x < len(piece) and sx - x >= 0:
                if sy - y < len(piece) and sy - y >= 0: is_piece_mino = piece[sy - y][sx - x] == 1
                if sy - shadow_y < len(piece) and sy - shadow_y >= 0: is_shadow_mino = piece[sy - shadow_y][sx - x] == 1
            result += f"{'██' if tile else ('▒▒' if is_piece_mino else ('░░' if is_shadow_mino else '[]'))}"
        result += "  ██\n"
    result += "██" + " " * 24 + "██\n" + "█" * 28 + "\n"
    if dont_print: return result
    print(result)
if standalone:
    print('Launching in standalone mode!\nType (case insensitive) letters to create input chains.\nr = right, l = left, u = rotate clockwise, d = soft drop, space = firm drop, v = hard drop, z = rotate counterclockwise.\nPress enter to execute and display board, or to quit (if the line consists of only the letter q).')
    function_map = {
        "r": move_right,
        "p": move_right,
        "l": move_left,
        "i": move_left,
        "u": rotate_cw,
        "9": rotate_cw,
        "d": soft_drop,
        "o": soft_drop,
        " ": firm_drop,
        "v": hard_drop,
        "z": rotate_ccw
    }
    while True:
        inputs = input("listrezpc> ").lower()
        if inputs == "q":
            break
        case = 0
        for char in inputs:
            if char == "q":
                case = 2
                break
            if char not in "rludvz 9iop":
                case = 1
        if case:
            if case == 1:
                print("Only allowed input characters are r, l, u, d, space, v, and z. Please try again.")
            else:
                print('Make sure to only type q and then press enter if you want to quit; q is not a valid character otherwise.')
            continue
        for char in inputs:
            function_map[char]()
        display_board()
