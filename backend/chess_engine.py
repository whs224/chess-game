# chess_engine.py

class Piece:
    def __init__(self, color):
        self.color = color

class Pawn(Piece):
    def get_legal_moves(self, board, position):
        row, col = position
        moves = []
        if self.color == "w":
            if row > 0 and board[row - 1][col] is None:
                moves.append((row - 1, col))
                if row == 6 and board[row - 2][col] is None:
                    moves.append((row - 2, col))
            if row > 0 and col < 7:
                target = board[row - 1][col + 1]
                if target is not None and target.color == "b":
                    moves.append((row - 1, col + 1))
            if row > 0 and col > 0:
                target = board[row - 1][col - 1]
                if target is not None and target.color == "b":
                    moves.append((row - 1, col - 1))
        else:
            if row < 7 and board[row + 1][col] is None:
                moves.append((row + 1, col))
                if row == 1 and board[row + 2][col] is None:
                    moves.append((row + 2, col))
            if row < 7 and col > 0:
                target = board[row + 1][col - 1]
                if target is not None and target.color == "w":
                    moves.append((row + 1, col - 1))
            if row < 7 and col < 7:
                target = board[row + 1][col + 1]
                if target is not None and target.color == "w":
                    moves.append((row + 1, col + 1))
        return moves

class Rook(Piece):
    def get_legal_moves(self, board, position):
        row, col = position
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

class Knight(Piece):
    def get_legal_moves(self, board, position):
        row, col = position
        moves = []
        directions = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2),  (1, 2),
            (2, -1),  (2, 1)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves

class Bishop(Piece):
    def get_legal_moves(self, board, position):
        row, col = position
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

class Queen(Piece):
    def get_legal_moves(self, board, position):
        row, col = position
        moves = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

class King(Piece):
    def get_legal_moves(self, board, position):
        row, col = position
        moves = []
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))
        return moves
