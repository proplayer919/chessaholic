from chessaholic import ChessEngine
import chess
from engine_utils import *


class Aqua3(ChessEngine):
    def __init__(self) -> None:
        super().__init__("Aqua V3", "proplayer919")

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

        # Bonus for king safety (encourage checks and checkmates)
        check_bonus = 0
        if board.is_check():
            check_bonus = 10  # Increase the weight of checks slightly

        # Combine scores
        combined_score = piece_score + positional_score + check_bonus

        # Return score based on the current turn
        return combined_score if board.turn == color else -combined_score

    def search(
        self,
        board: chess.Board,
        color: chess.Color,
        depth: int,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
        in_check_sequence: bool = False,
    ) -> tuple[chess.Move, float]:
        """Improved search with depth extensions for checks and avoidance of repeated checks."""
        # Check for terminal positions
        if board.is_checkmate():
            return None, float("inf") if board.turn == color else float("-inf")
        if (
            board.is_stalemate()
            or board.is_insufficient_material()
            or board.is_fivefold_repetition()
        ):
            return None, 0  # Draw condition

        if depth == 0:
            return None, self.evaluate_board(board, color)

        best_move = None
        best_evaluation = float("-inf") if board.turn == color else float("inf")
        moves = self.order_moves(board, list(board.legal_moves))

        for move in moves:
            if not board.is_legal(move):
                continue

            new_board = board.copy()
            new_board.push(move)

            # Extend the search if the move is a check
            next_depth = depth - 1
            if new_board.is_check() or new_board.is_checkmate():
                next_depth += 1  # Extend depth for critical moves

            # Penalize repeated checks that do not lead to progress
            if (
                in_check_sequence
                and not new_board.is_checkmate()
                and new_board.is_check()
                and not new_board.is_repetition()
            ):
                next_depth -= 1  # Shorten search depth if stuck in check sequences

            _, evaluation = self.search(
                new_board, color, next_depth, alpha, beta, new_board.is_check()
            )

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

            # Alpha-beta pruning
            if beta <= alpha:
                break

        return best_move, best_evaluation

    def order_moves(
        self, board: chess.Board, moves: list[chess.Move]
    ) -> list[chess.Move]:
        # Prioritize captures, checks, and forcing moves
        return sorted(
            moves,
            key=lambda move: (
                board.is_capture(move),
                board.gives_check(move),
                1 if move.promotion else 0,
            ),
            reverse=True,
        )

    async def move(self, board: chess.Board, color: chess.Color) -> chess.Move:
        return self.search(board, color, 2)[
            0
        ]  # Increase depth to 4 for better evaluation
