class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_log = []
        self.white_to_move = True
        self.pieces = {"R": self.get_rook_moves, "p": self.get_pawn_moves, "N": self.get_knight_moves,
                       "Q": self.get_queen_moves, "B": self.get_bishop_moves, "K": self.get_king_moves}

    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.movedPiece
        # print(self.board)
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        # print([x.get_notation() for x in self.move_log])
        # print(move.get_notation())

    def undo_move(self):
        if len(self.move_log) == 0:
            pass
        else:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.movedPiece
            self.board[move.end_row][move.end_col] = move.pieceTaken
            self.white_to_move = not self.white_to_move
            # print(self.move_log)

    def get_valid_moves(self):
        return self.get_possible_moves()
        pass

    def get_pawn_moves(self, r, c, moves):
        if self.white_to_move:

            if r >= 1:
                if self.board[r - 1][c] == "--":
                    moves.append(Move(self.board, (r, c), (r - 1, c)))
                    if r == 6 and self.board[r - 2][c] == "--":
                        moves.append(Move(self.board, (r, c), (r - 2, c)))

                if c >= 1:
                    if self.board[r - 1][c - 1][0] == "b":
                        moves.append(Move(self.board, (r, c), (r - 1, c - 1)))
                if c <= 6:
                    if self.board[r - 1][c + 1][0] == "b":
                        moves.append(Move(self.board, (r, c), (r - 1, c + 1)))
        else:

            if r >= 1:
                if self.board[r + 1][c] == "--":
                    moves.append(Move(self.board, (r, c), (r + 1, c)))
                    if r == 1 and self.board[r + 2][c] == "--":
                        moves.append(Move(self.board, (r, c), (r + 2, c)))

                if c >= 1:
                    if self.board[r + 1][c - 1][0] == "w":
                        moves.append(Move(self.board, (r, c), (r + 1, c - 1)))
                if c <= 6:
                    if self.board[r + 1][c + 1][0] == "w":
                        moves.append(Move(self.board, (r, c), (r + 1, c + 1)))

    def get_rook_moves(self, r, c, moves, dirs=None):
        # dirs =
        if not dirs:  # no direction supplied hence assuming rook, else bishop
            dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        enemy = "b" if self.white_to_move else "w"

        for d in dirs:
            for i in range(1, 8):
                end_row = r + d[0] * i
                end_col = c + d[1] * i
                # print(f"r : {r}, c : {c}, end : {end_row}, {end_col}")
                if (0 <= end_row < 8) and (0 <= end_col < 8):
                    end_piece = self.board[end_row][end_col]
                    # print(end_piece)
                    if end_piece == "--":
                        moves.append(Move(self.board, (r, c), (end_row, end_col)))

                    elif end_piece[0] == enemy:
                        moves.append(Move(self.board, (r, c), (end_row, end_col)))
                        break
                    else:
                        break  # friendly piece hence stopped looking any forward
                else:
                    break
            # print([x.get_notation() for x in moves])
        # print([x.get_notation() for x in moves])

    def get_bishop_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves, [(-1, -1), (1, 1), (-1, 1), (1, -1)])
        # pass

    def get_knight_moves(self, r, c, moves):
        dirs = [(2, 1), (1, 2), (-1, 2), (2, -1), (1, -2), (-2, 1), (-2, -1), (-1, -2)]
        enemy = "b" if self.white_to_move else "w"
        for d in dirs:
            end_row = r + d[0]
            end_col = c + d[1]
            if (0 <= end_row < 8) and (0 <= end_col < 8):
                end_piece = self.board[end_row][end_col]
                if end_piece == enemy or end_piece == "--":
                    moves.append(Move(self.board, (r, c), (end_row, end_col)))

    def get_king_moves(self, r, c, moves):
        self.get_knight_moves(r, c, moves):

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves, [(-1, -1), (1, 1), (-1, 1), (1, -1), (-1, 0), (1, 0), (0, 1), (0, -1)])

    def get_possible_moves(self):

        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                # print(r, c)
                # print("here")
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                # print(piece, turn)
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    # print(moves)
                    # if piece == 'p':
                    #     self.get_pawn_moves(r, c, moves)
                    # elif piece == 'R':
                    #     self.get_rook_moves(r, c, moves)
                    self.pieces[piece](r, c, moves)
            # pass
        return moves


class Move:
    def __init__(self, board, start_pos, end_pos):
        self.movedPiece = board[start_pos[0]][start_pos[1]]
        self.pieceTaken = board[end_pos[0]][end_pos[1]]
        self.board = board
        self.start_row = start_pos[0]
        self.start_col = start_pos[1]
        self.end_row = end_pos[0]
        self.end_col = end_pos[1]
        self.move_id = 1000 * self.start_row + 100 * self.start_col + 10 * self.end_row + self.end_col
        # print(self.start_row, self.start_col, self.movedPiece)

    def get_notation(self):
        # pos is a tuple - (row, column)
        ranks = ["a", "b", "c", "d", "e", "f", "g", "h"]
        files = ["8", "7", "6", "5", "4", "3", "2", "1"]
        # notation = f"{files[self.start_col]}{ranks[self.start_row]}{files[self.end_col]}{ranks[self.end_col]}"
        if self.movedPiece[1] == 'p':
            notation = ranks[self.end_col] + files[self.end_row]
        else:
            notation = self.movedPiece[1] + ranks[self.end_col] + files[self.end_row]
        # print(notation)
        return notation

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False
