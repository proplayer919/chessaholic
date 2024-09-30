from chessaholic import ChessEngine
import chess
from engine_utils import *
import chess.polyglot
import asyncio


class Aqua4(ChessEngine):
    def __init__(self) -> None:
        super().__init__("Aqua 4", "proplayer919")
        self.transposition_table = {}
        self.history_table = {}  # For history heuristic
        self.killer_moves = {}  # For killer move heuristic

    def evaluate_board(self, board: chess.Board, color: chess.Color) -> float:
        piece_score = 0
        positional_score = 0

        # Piece and positional scoring
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                piece_value = piece_values[piece.piece_type]
                piece_score += piece_value if piece.color == color else -piece_value

                # Positional advantage (e.g., center control)
                if piece.color == color:
                    positional_score += get_position_table(board)[piece.piece_type][
                        square
                    ]

        # King safety improvement: reduce points if king is exposed
        king_safety = self.evaluate_king_safety(board, color)

        # Tactical pattern recognition (forks, pins, skewers, etc.)
        tactical_bonus = self.tactical_evaluation(board, color)

        # Combine scores
        combined_score = piece_score + positional_score + king_safety + tactical_bonus

        # Return score based on the current turn
        return combined_score if board.turn == color else -combined_score

    def evaluate_king_safety(self, board: chess.Board, color: chess.Color) -> float:
        """Evaluate king safety based on pawn structure and piece activity near the king."""
        king_square = board.king(color)
        king_safety_score = 0
        if not board.is_attacked_by(not color, king_square):
            king_safety_score += 15  # bonus if the king is not under threat
        return king_safety_score

    def tactical_evaluation(self, board: chess.Board, color: chess.Color) -> float:
        """Evaluate common tactical patterns like forks, pins, and skewers."""
        tactical_score = 0
        for move in board.legal_moves:
            if board.gives_check(move):
                tactical_score += 5

        if board.is_attacked_by(color, board.king(not color)):
            tactical_score += 5

        if board.is_attacked_by(not color, board.king(color)):
            tactical_score -= 10

        return tactical_score

    async def search_in_parallel(
        self,
        board: chess.Board,
        color: chess.Color,
        moves: list[chess.Move],
        depth: int,
        alpha: float,
        beta: float,
    ):
        """Parallel search for moves using asyncio."""
        tasks = [self.search(board, color, depth, alpha, beta) for move in moves]
        results = await asyncio.gather(*tasks)
        return results

    async def search(
        self,
        board: chess.Board,
        color: chess.Color,
        depth: int,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
    ) -> tuple[chess.Move, float]:
        """Search function using async to avoid UI blocking."""
        board_hash = chess.polyglot.zobrist_hash(board)
        if (
            board_hash in self.transposition_table
            and self.transposition_table[board_hash][1] >= depth
        ):
            return self.transposition_table[board_hash]

        if board.is_checkmate():
            return None, float("inf") if board.turn == color else float("-inf")
        if board.is_stalemate() or board.is_insufficient_material():
            return None, 0
        
        # Don't let the bot draw from repitition
        if board.can_claim_threefold_repetition():
            return None, -1000

        if depth == 0:
            return None, await self.quiescence_search(board, color, alpha, beta)

        best_move = None
        best_evaluation = float("-inf") if board.turn == color else float("inf")
        moves = self.order_moves(board, list(board.legal_moves))

        for move in moves:
            new_board = board.copy()
            new_board.push(move)
            next_depth = depth - 1

            # Increase depth in checks
            if new_board.is_check():
                next_depth += 1

            _, evaluation = await self.search(new_board, color, next_depth, alpha, beta)

            if board.turn == color:
                if evaluation > best_evaluation:
                    best_evaluation = evaluation
                    best_move = move
                alpha = max(alpha, best_evaluation)
            else:
                if evaluation < best_evaluation:
                    best_evaluation = evaluation
                    best_move = move
                beta = min(beta, best_evaluation)

            if beta <= alpha:
                self.update_history_heuristic(board, move, depth)
                self.update_killer_moves(board, move)
                break

        self.transposition_table[board_hash] = (best_move, best_evaluation)
        return best_move, best_evaluation

    async def quiescence_search(
        self, board: chess.Board, color: chess.Color, alpha: float, beta: float
    ) -> float:
        """Quiescence search using async to prevent blocking."""
        stand_pat = self.evaluate_board(board, color)
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in board.legal_moves:
            if not board.is_capture(move) and not board.gives_check(move):
                continue
            new_board = board.copy()
            new_board.push(move)
            score = -await self.quiescence_search(new_board, not color, -beta, -alpha)

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    def order_moves(
        self, board: chess.Board, moves: list[chess.Move]
    ) -> list[chess.Move]:
        """Efficient move ordering with history and killer heuristics."""
        return sorted(
            moves,
            key=lambda move: (
                self.killer_moves.get((board.turn, move), 0),  # Killer move priority
                self.history_table.get(
                    (board.turn, move), 0
                ),  # History heuristic priority
                board.is_capture(move),
                board.gives_check(move),
                1 if move.promotion else 0,
            ),
            reverse=True,
        )

    def update_killer_moves(self, board: chess.Board, move: chess.Move) -> None:
        """Update killer move heuristic for moves that caused cutoffs."""
        if move not in self.killer_moves:
            self.killer_moves[(board.turn, move)] = 1
        else:
            self.killer_moves[(board.turn, move)] += 1

    def update_history_heuristic(
        self, board: chess.Board, move: chess.Move, depth: int
    ) -> None:
        """Update the history heuristic table to favor moves that cause cutoffs."""
        self.history_table[(board.turn, move)] = (
            self.history_table.get((board.turn, move), 0) + depth**2
        )

    async def move(self, board: chess.Board, color: chess.Color) -> chess.Move:
        """Move calculation using asyncio without blocking."""
        best_move, _ = await self.search(board, color, 2)
        print(f"Best move for {'white' if color == chess.WHITE else 'black'}: {best_move}")
        return best_move
