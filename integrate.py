import cmdtetr as ct
from bitmaps import piece_bmps as pieces
from random import choice as choiche
def find_positions():
    rv = []
    inputs_rv = []
    positions = [[ct.x, ct.y, ct.r, "flurz", ""]]
    position_codes = [f"{ct.x} {ct.y} {ct.r}"] # unique codes to determine if a position is already registered
    for p in positions:
        while p[3]:
            ct.x = p[0]
            ct.y = p[1]
            ct.set_rotation(p[2])
            action = p[3][0]
            p[3] = p[3][1:]
            if action == "r":
                ct.move_right()
            elif action == "l":
                ct.move_left()
            elif action == "u":
                ct.rotate_cw()
            elif action == "z":
                ct.rotate_ccw()
            elif action == "f":
                try:
                    ct.soft_drop()
                    ct.firm_drop()
                except ct.CementRequest:
                    old_board = copy_matrix(ct.board)
                    old_piece = ct.piece
                    old_y = ct.y
                    ct.cement(zone_style=True)
                    new_board = ct.board
                    in_bounds = True
                    for tile in ct.board[4]:
                        if tile:
                            in_bounds = False
                            break
                    pits = [0]
                    divisible = True
                    for x in range(10):
                        holes = 0
                        for y in range(5, 9):
                            if not ct.board[y][x]:
                                holes += 1
                        if holes:
                            pits[-1] += holes
                        elif pits[-1] % 4:
                            divisible = False
                            break
                        else:
                            pits.append(0)
                    ct.board = old_board
                    ct.piece = old_piece
                    ct.x = p[0]
                    ct.y = old_y
                    ct.r = p[2] # setting directly is ok because the piece is already in its old bitmap
                    # print(end=f"[{ct.x} {ct.y} {ct.r}] ({p[4]})") # no "+ action" because it's always f
                    if in_bounds and divisible and new_board not in rv:
                        # print(": ")
                        # ct.display_board()
                        inputs_rv.append(p[4].rstrip("f") + "v")
                        rv.append(new_board)
                    # elif not in_bounds:
                    #     print(" is out of bounds.")
                    # elif new_board in rv:
                    #     print(" creates a duplicate board.")
                    # else:
                    #     print(" is off-parity.")
            code = f"{ct.x} {ct.y} {ct.r}"
            if code not in position_codes:
                # print(f"Created ({code})!")
                position_codes.append(code)
                positions.append([ct.x, ct.y, ct.r, "flurz", p[4] + action])
    return zip(inputs_rv, rv)