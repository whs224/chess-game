from __future__ import annotations
from typing import List, Optional, Tuple, Dict, Set, Iterable, NamedTuple

FILES = "abcdefgh"
RANKS = "12345678"
WHITE, BLACK = "w", "b"


class Piece(NamedTuple):
    type: str  # 'P','N','B','R','Q','K'
    color: str  # 'w' or 'b'

    def symbol(self) -> str:
        return self.type.upper() if self.color == WHITE else self.type.lower()


class Move(NamedTuple):
    src: Tuple[int, int]
    dst: Tuple[int, int]
    promotion: Optional[str] = None
    is_en_passant: bool = False
    is_castle_king: bool = False
    is_castle_queen: bool = False
    captured: Optional[Piece] = None
    piece: Optional[Piece] = None  # filled by generator


def in_bounds(r: int, c: int) -> bool:
    return 0 <= r < 8 and 0 <= c < 8


def algebraic_to_coords(sq: str) -> Tuple[int, int]:
    sq = sq.strip().lower()
    file = FILES.index(sq[0])
    rank = int(sq[1])
    row = 8 - rank
    return (row, file)


def coords_to_algebraic(rc: Tuple[int, int]) -> str:
    r, c = rc
    return f"{FILES[c]}{8 - r}"


class Board:
    
    def __init__(self) -> None:
        self.board: List[List[Optional[Piece]]] = [[None] * 8 for _ in range(8)]
        self.turn = WHITE
        self.castling_rights: Set[str] = set("KQkq")
        self.en_passant: Optional[Tuple[int, int]] = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.history: List = []
        self.position_counts: Dict[str, int] = {}
        self.setup_starting_position()

    # --- Setup & helpers ---

    def _snapshot(self):
        return (
            [row[:] for row in self.board],
            self.turn,
            set(self.castling_rights),
            self.en_passant,
            self.halfmove_clock,
            self.fullmove_number,
        )

    def _restore(self, snap):
        (
            self.board,
            self.turn,
            self.castling_rights,
            self.en_passant,
            self.halfmove_clock,
            self.fullmove_number,
        ) = (
            [row[:] for row in snap[0]],
            snap[1],
            set(snap[2]),
            snap[3],
            snap[4],
            snap[5],
        )

    def _apply_move(self, move):
        src_r, src_c = move.src
        dst_r, dst_c = move.dst
        piece = self.board[src_r][src_c]
        self.board[src_r][src_c] = None

        if move.is_en_passant:
            self.board[src_r][dst_c] = None

        if move.is_castle_king:
            rook_src, rook_dst = (src_r, 7), (src_r, 5)
            self.board[rook_dst[0]][rook_dst[1]] = self.board[rook_src[0]][rook_src[1]]
            self.board[rook_src[0]][rook_src[1]] = None
        elif move.is_castle_queen:
            rook_src, rook_dst = (src_r, 0), (src_r, 3)
            self.board[rook_dst[0]][rook_dst[1]] = self.board[rook_src[0]][rook_src[1]]
            self.board[rook_src[0]][rook_src[1]] = None

        if move.promotion:
            piece = Piece(move.promotion, piece.color)

        self.board[dst_r][dst_c] = piece
        self.turn = WHITE if self.turn == BLACK else BLACK
        if self.turn == WHITE:
            self.fullmove_number += 1
        self._increment_position_count()

    def make_move(self, move):
        self._apply_move(move)
        return True

    def all_legal_moves(self):
        return self.generate_legal_moves(self.turn)

    def is_checkmate(self):
        return self.is_in_check(self.turn) and not self.all_legal_moves()

    def is_stalemate(self):
        return not self.is_in_check(self.turn) and not self.all_legal_moves()

    def setup_starting_position(self) -> None:
        self.board = [[None] * 8 for _ in range(8)]
        for c in range(8):
            self.board[6][c] = Piece("P", WHITE)
            self.board[1][c] = Piece("P", BLACK)
        order = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for c, t in enumerate(order):
            self.board[7][c] = Piece(t, WHITE)
            self.board[0][c] = Piece(t, BLACK)
        self.turn = WHITE
        self.castling_rights = set("KQkq")
        self.en_passant = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.history.clear()
        self.position_counts.clear()
        self._increment_position_count()

    def piece_at(self, r: int, c: int) -> Optional[Piece]:
        return self.board[r][c]

    def king_position(self, color: str) -> Tuple[int, int]:
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == color and p.type == "K":
                    return (r, c)
        raise RuntimeError("King not found")

    # --- Attack detection ---

    def is_square_attacked_by(self, target: Tuple[int, int], attacker_color: str) -> bool:
        r, c = target

        # Pawn attacks
        dr = -1 if attacker_color == WHITE else 1
        for dc in (-1, 1):
            rr, cc = r + dr, c + dc
            if in_bounds(rr, cc):
                p = self.board[rr][cc]
                if p and p.color == attacker_color and p.type == "P":
                    return True

        # Knight attacks
        for dr, dc in [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]:
            rr, cc = r + dr, c + dc
            if in_bounds(rr, cc):
                p = self.board[rr][cc]
                if p and p.color == attacker_color and p.type == "N":
                    return True

        # Sliding attacks
        for dr, dc, types in [
            (1, 0, ("R", "Q")), (-1, 0, ("R", "Q")),
            (0, 1, ("R", "Q")), (0, -1, ("R", "Q")),
            (1, 1, ("B", "Q")), (1, -1, ("B", "Q")),
            (-1, 1, ("B", "Q")), (-1, -1, ("B", "Q")),
        ]:
            rr, cc = r + dr, c + dc
            while in_bounds(rr, cc):
                p = self.board[rr][cc]
                if p:
                    if p.color == attacker_color and p.type in types:
                        return True
                    break
                rr += dr
                cc += dc

        # King attacks
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                rr, cc = r + dr, c + dc
                if in_bounds(rr, cc):
                    p = self.board[rr][cc]
                    if p and p.color == attacker_color and p.type == "K":
                        return True
        return False

    def is_in_check(self, color: str) -> bool:
        return self.is_square_attacked_by(self.king_position(color), WHITE if color == BLACK else BLACK)

    # --- Move generation ---

    def _generate_pseudo_moves_for_piece(self, r: int, c: int) -> Iterable[Move]:
        p = self.board[r][c]
        if not p:
            return []
        color = p.color
        dir_forward = -1 if color == WHITE else 1
        moves: List[Move] = []

        if p.type == "P":
            # Single and double pushes
            rr = r + dir_forward
            if in_bounds(rr, c) and self.board[rr][c] is None:
                if rr in (0, 7):
                    for promo in ("Q", "R", "B", "N"):
                        moves.append(Move((r, c), (rr, c), promotion=promo))
                else:
                    moves.append(Move((r, c), (rr, c)))

                start_rank = 6 if color == WHITE else 1
                rr2 = r + 2 * dir_forward
                if r == start_rank and self.board[rr2][c] is None:
                    moves.append(Move((r, c), (rr2, c)))

            # Captures
            for dc in (-1, 1):
                cc = c + dc
                rr = r + dir_forward
                if in_bounds(rr, cc):
                    target = self.board[rr][cc]
                    if target and target.color != color:
                        if rr in (0, 7):
                            for promo in ("Q", "R", "B", "N"):
                                moves.append(Move((r, c), (rr, cc), promotion=promo, captured=target))
                        else:
                            moves.append(Move((r, c), (rr, cc), captured=target))

            # En passant
            if self.en_passant:
                er, ec = self.en_passant
                if er == r + dir_forward and abs(ec - c) == 1:
                    moves.append(Move((r, c), (er, ec), is_en_passant=True))

        elif p.type == "N":
            for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]:
                rr, cc = r + dr, c + dc
                if in_bounds(rr, cc):
                    t = self.board[rr][cc]
                    if t is None or t.color != color:
                        moves.append(Move((r, c), (rr, cc), captured=t))

        elif p.type in ("B", "R", "Q"):
            directions = []
            if p.type in ("B", "Q"):
                directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            if p.type in ("R", "Q"):
                directions += [(1, 0), (-1, 0), (0, 1), (0, -1)]

            for dr, dc in directions:
                rr, cc = r + dr, c + dc
                while in_bounds(rr, cc):
                    t = self.board[rr][cc]
                    if t is None:
                        moves.append(Move((r, c), (rr, cc)))
                    else:
                        if t.color != color:
                            moves.append(Move((r, c), (rr, cc), captured=t))
                        break
                    rr += dr
                    cc += dc

        elif p.type == "K":
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    rr, cc = r + dr, c + dc
                    if in_bounds(rr, cc):
                        t = self.board[rr][cc]
                        if t is None or t.color != color:
                            moves.append(Move((r, c), (rr, cc), captured=t))

            # Castling
            if p.color == WHITE and (r, c) == (7, 4):
                if "K" in self.castling_rights and self.board[7][5] is None and self.board[7][6] is None:
                    moves.append(Move((r, c), (7, 6), is_castle_king=True))
                if "Q" in self.castling_rights and self.board[7][3] is None and self.board[7][2] is None and self.board[7][1] is None:
                    moves.append(Move((r, c), (7, 2), is_castle_queen=True))
            if p.color == BLACK and (r, c) == (0, 4):
                if "k" in self.castling_rights and self.board[0][5] is None and self.board[0][6] is None:
                    moves.append(Move((r, c), (0, 6), is_castle_king=True))
                if "q" in self.castling_rights and self.board[0][3] is None and self.board[0][2] is None and self.board[0][1] is None:
                    moves.append(Move((r, c), (0, 2), is_castle_queen=True))

        out = [Move(m.src, m.dst, m.promotion, m.is_en_passant, m.is_castle_king, m.is_castle_queen, m.captured, p) for m in moves]
        return out

    # --- Legal moves ---

    def generate_legal_moves(self, color: str) -> List[Move]:
        legal: List[Move] = []
        for m in self._generate_pseudo_moves_for_piece(0, 0): pass  # dummy to silence mypy
        for m in self.generate_pseudo_legal_moves(color):
            if m.piece and m.piece.type == "K" and (m.is_castle_king or m.is_castle_queen):
                if self.is_in_check(color):
                    continue
                path_cols = [5, 6] if m.is_castle_king else [3, 2]
                row = m.src[0]
                if any(self.is_square_attacked_by((row, cc), WHITE if color == BLACK else BLACK) for cc in path_cols):
                    continue
            snap = self._snapshot()
            self._apply_move(m)
            ok = not self.is_in_check(color)
            self._restore(snap)
            if ok:
                legal.append(m)
        return legal

    def generate_pseudo_legal_moves(self, color: str) -> List[Move]:
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == color:
                    moves.extend(self._generate_pseudo_moves_for_piece(r, c))
        return moves

    # --- Move parsing (auto-queen added here) ---

    def parse_move_str(self, s: str) -> Optional[Move]:
        s = s.strip().lower()
        if s in ("0-0", "o-o", "e1g1", "e8g8"):
            for m in self.all_legal_moves():
                if m.is_castle_king:
                    return m
            return None
        if s in ("0-0-0", "o-o-o", "e1c1", "e8c8"):
            for m in self.all_legal_moves():
                if m.is_castle_queen:
                    return m
            return None
        if len(s) not in (4, 5):
            return None

        try:
            src = algebraic_to_coords(s[:2])
            dst = algebraic_to_coords(s[2:4])
        except Exception:
            return None

        promo = s[4].upper() if len(s) == 5 else None
        for m in self.all_legal_moves():
            if m.src == src and m.dst == dst and ((promo or None) == (m.promotion or None)):
                return m

        # ✅ Auto-queen if pawn reaches last rank without promotion letter
        if promo is None:
            for m in self.all_legal_moves():
                if m.src == src and m.dst == dst and m.piece and m.piece.type == "P" and m.promotion == "Q":
                    return m
        return None
    # --- Position tracking ---

    def _position_key(self) -> str:
        rows = []
        for r in range(8):
            empty = 0
            row = []
            for c in range(8):
                p = self.board[r][c]
                if p is None:
                    empty += 1
                else:
                    if empty:
                        row.append(str(empty))
                        empty = 0
                    row.append(p.symbol())
            if empty:
                row.append(str(empty))
            rows.append("".join(row))
        pieces = "/".join(rows)
        cr = "".join(sorted(self.castling_rights)) or "-"
        ep = coords_to_algebraic(self.en_passant) if self.en_passant else "-"
        return f"{pieces} {self.turn} {cr} {ep}"

    def _increment_position_count(self) -> None:
        key = self._position_key()
        self.position_counts[key] = self.position_counts.get(key, 0) + 1

    
