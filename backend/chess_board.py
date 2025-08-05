from chess_engine import Piece, Pawn, Rook, Knight, Bishop, Queen, King

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()

    def setup_board(self):
        for col in range(8):
            self.board[6][col] = Pawn("w")
            self.board[1][col] = Pawn("b")

        self.board[7][0] = Rook("w")
        self.board[7][1] = Knight("w")
        self.board[7][2] = Bishop("w")
        self.board[7][3] = Queen("w")
        self.board[7][4] = King("w")
        self.board[7][5] = Bishop("w")
        self.board[7][6] = Knight("w")
        self.board[7][7] = Rook("w")

        self.board[0][0] = Rook("b")
        self.board[0][1] = Knight("b")
        self.board[0][2] = Bishop("b")
        self.board[0][3] = Queen("b")
        self.board[0][4] = King("b")
        self.board[0][5] = Bishop("b")
        self.board[0][6] = Knight("b")
        self.board[0][7] = Rook("b")

    def print_board(self):
        print("\n  a  b  c  d  e  f  g  h")
        for i, row in enumerate(self.board):
            row_str = f"{8 - i} "
            for piece in row:
                if piece:
                    label = piece.__class__.__name__[0] + piece.color
                else:
                    label = " . "
                row_str += label + " "
            print(row_str + f"{8 - i}")
        print("  a  b  c  d  e  f  g  h")

    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos[0]][start_pos[1]]
        self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = None

    def is_in_check(self, color):
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        if not king_pos:
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color != color:
                    try:
                        if king_pos in piece.get_legal_moves(self.board, (row, col)):
                            return True
                    except:
                        continue
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    start_pos = (row, col)
                    try:
                        moves = piece.get_legal_moves(self.board, start_pos)
                    except:
                        continue
                    if not moves:
                        continue
                    for end_pos in moves:
                        captured = self.board[end_pos[0]][end_pos[1]]
                        self.board[end_pos[0]][end_pos[1]] = piece
                        self.board[start_pos[0]][start_pos[1]] = None
                        still_in_check = self.is_in_check(color)
                        self.board[start_pos[0]][start_pos[1]] = piece
                        self.board[end_pos[0]][end_pos[1]] = captured
                        if not still_in_check:
                            return False
        return True

    def is_legal_move(self, start_pos, end_pos):
        if start_pos == end_pos:
            return False
        piece = self.board[start_pos[0]][start_pos[1]]
        if piece is None:
            return False
        target = self.board[end_pos[0]][end_pos[1]]
        if target and target.color == piece.color:
            return False

        try:
            if end_pos not in piece.get_legal_moves(self.board, start_pos):
                return False
            captured = self.board[end_pos[0]][end_pos[1]]
            self.board[end_pos[0]][end_pos[1]] = piece
            self.board[start_pos[0]][start_pos[1]] = None
            in_check = self.is_in_check(piece.color)
            self.board[start_pos[0]][start_pos[1]] = piece
            self.board[end_pos[0]][end_pos[1]] = captured
            return not in_check
        except:
            return False
