# board: 4x4
# piece: 4 binary attributes, 2^4 = 16 pieces
# attributes are: color (dark, light), shape (circle, square), size (big, small), hole (yes, no)
# winning: 4 in a row for any attribute
# player places a piece and picks the piece for the opponent

# total number of games = (16 * 16) * (15 * 15) * ...

from random import choice

ALL_PIECES = set([i for i in range(16)])


def piece_to_str(piece: int):
    out = ""
    if piece & 0b1000:
        out += "dark "
    else:
        out += "light "

    if piece & 0b0100:
        out += "square "
    else:
        out += "circle "

    if piece & 0b0010:
        out += "big "
    else:
        out += "small "

    if piece & 0b0001:
        out += "hole"
    else:
        out += "no hole"

    return out


class Board:
    def __init__(self):
        self.next_piece = None
        self.board = [[None for _ in range(4)] for _ in range(4)]

    def actions(self):
        used_pieces = set([self.next_piece]) if self.next_piece is not None else set()
        left_positions = set()

        for x in range(4):
            for y in range(4):
                if self.board[x][y] is not None:
                    used_pieces.add(self.board[x][y])
                else:
                    left_positions.add((x, y))

        left_pieces = ALL_PIECES - used_pieces

        for pos in left_positions:
            for piece in left_pieces:
                yield pos, piece

    def with_action(self, pos: tuple[int], piece: int):
        act = (pos, piece)
        if act not in self.actions():
            raise ValueError("Invalid action")

        new_board = Board()

        new_board.board = [row.copy() for row in self.board]
        new_board.board[pos[0]][pos[1]] = self.next_piece
        new_board.next_piece = piece

        return new_board

    def paths(self):
        # x axis paths
        for x in range(4):
            path = []
            for y in range(4):
                path.append((x, y))

            yield path

        # y axis paths
        for y in range(4):
            path = []
            for x in range(4):
                path.append((x, y))

            yield path

        # diagonal paths
        path = []
        for i in range(4):
            path.append((i, i))

        yield path

        path = []
        for i in range(4):
            path.append((i, 3 - i))

        yield path

    def winning(self):
        for path in self.paths():
            win = 0b1111
            win_inv = 0b1111

            for x, y in path:
                value = self.board[x][y]
                value = value if value is not None else 0
                win &= value

                inv = self.board[x][y]
                inv = ~inv if inv is not None else 0
                win_inv &= inv

            if win != 0 or win_inv != 0:
                return True

        return False

    def __str__(self):
        out = ""
        for y in range(4):
            for x in range(4):
                value = self.board[y][x]
                if value is None:
                    out += "---- "
                else:
                    out += f"{value:04b} "
            out += "\n"

        return out


def rollout(board: Board):
    player = True
    starting_player = player

    while True:
        actions = list(board.actions())
        if len(actions) == 0:
            return 0  # draw

        action = choice(actions)
        board = board.with_action(*action)
        if board.winning():
            break

        player = not player

    if player == starting_player:
        return 1
    else:
        return -1


def minmax(board: Board, max_depth=3):
    if board.winning():
        return None, -1

    actions = list(board.actions())
    if len(actions) == 0:
        return None, 0

    if max_depth == 0:
        avg_score = 0
        iters = 10

        for _ in range(iters):
            avg_score += rollout(board)

        avg_score /= iters
        return None, avg_score

    best_score = -999999
    best_action = None

    for action in actions:
        new_board = board.with_action(*action)
        _, score = minmax(new_board, max_depth - 1)
        score = -score

        # if max_depth == 5:
        #     print(action, score)

        if score > best_score:
            best_score = score
            best_action = action

    return best_action, best_score


if __name__ == "__main__":
    board = Board()

    board.board = [
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]

    # you play by writing moves here lmao
    moves = [
    ]

    for move in moves:
        board = board.with_action(*move)

    print(board)

    (pos, piece), score = minmax(board, max_depth=5)

    print(score)
    print(pos, "piece: ", piece_to_str(piece))
