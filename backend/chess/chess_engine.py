from __future__ import annotations
from typing import Optional
from .chess_board import Board, Move, WHITE, BLACK


class Engine:
    """Small but solid alpha-beta engine (material + mobility)."""

    PIECE_VALUES = {"P": 100, "N": 320, "B": 330, "R": 500, "Q": 900, "K": 0}

    def evaluate(self, board: Board) -> int:
        # Material
        score = 0
        for r in range(8):
            for c in range(8):
                p = board.board[r][c]
                if p:
                    v = self.PIECE_VALUES[p.type]
                    score += v if p.color == WHITE else -v

        # Mobility (tiny nudge)
        score += len(board.generate_legal_moves(WHITE)) - len(board.generate_legal_moves(BLACK))

        # Check status (tiny nudge)
        if board.is_in_check(WHITE):
            score -= 10
        if board.is_in_check(BLACK):
            score += 10

        return score

    def _search(self, board: Board, depth: int, alpha: int, beta: int) -> int:
        if depth == 0 or board.is_checkmate() or board.is_stalemate():
            return self.evaluate(board)

        best = -10**9 if board.turn == WHITE else 10**9
        moves = board.all_legal_moves()
        if not moves:
            return self.evaluate(board)

        # Simple move ordering: captures & promotions first
        def order(m: Move):
            return 1 if (m.captured or m.promotion) else 0

        moves.sort(key=order, reverse=True)

        for m in moves:
            snap = board._snapshot()
            board._apply_move(m)
            board.turn = WHITE if board.turn == BLACK else BLACK
            if board.turn == WHITE:
                board.fullmove_number += 1
            board._increment_position_count()

            val = self._search(board, depth - 1, alpha, beta)
            board._restore(snap)

            if board.turn == WHITE:
                if val > best:
                    best = val
                if best > alpha:
                    alpha = best
                if alpha >= beta:
                    break
            else:
                if val < best:
                    best = val
                if best < beta:
                    beta = best
                if alpha >= beta:
                    break

        return best

    def choose_move(self, board: Board, depth: int = 2) -> Optional[Move]:
        best_move: Optional[Move] = None
        best_val = -10**9 if board.turn == WHITE else 10**9

        moves = board.all_legal_moves()
        if not moves:
            return None

        def order(m: Move):
            return 1 if (m.captured or m.promotion) else 0

        moves.sort(key=order, reverse=True)

        for m in moves:
            snap = board._snapshot()
            board._apply_move(m)
            board.turn = WHITE if board.turn == BLACK else BLACK
            if board.turn == WHITE:
                board.fullmove_number += 1
            board._increment_position_count()

            val = self._search(board, depth - 1, -10**9, 10**9)
            board._restore(snap)

            if board.turn == WHITE:
                if val > best_val:
                    best_val, best_move = val, m
            else:
                if val < best_val:
                    best_val, best_move = val, m

        return best_move
