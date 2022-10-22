piece_bmps = {
    "i": [
        [0, 0, 0, 0], #
        [1, 1, 1, 1], # I
        [0, 0, 0, 0], #
        [0, 0, 0, 0]  #
    ],
    "j": [
        [1, 0, 0], #
        [1, 1, 1], # J
        [0, 0, 0]  #
    ],
    "l": [
        [0, 0, 1], #
        [1, 1, 1], # L
        [0, 0, 0]  #
    ],
    "o": [
        [1, 1], # O
        [1, 1]  #
    ],
    "s": [
        [0, 1, 1], #
        [1, 1, 0], # S
        [0, 0, 0]  #
    ],
    "t": [
        [0, 1, 0], #
        [1, 1, 1], # T
        [0, 0, 0]  #
    ],
    "z": [
        [1, 1, 0], #
        [0, 1, 1], # Z
        [0, 0, 0]  #
    ]
}

def copy_matrix(matrix):
    copy = []
    for row in matrix:
        copy.append(row[:])
    return copy

def generate_queue(queue_str):
    rv = []
    for char in queue_str:
        rv.append(copy_matrix(piece_bmps[char]))
    return rv