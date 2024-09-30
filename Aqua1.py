from chessaholic import ChessEngine
import chess
import random

piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0
}

class Aqua1(ChessEngine):
    def __init__(self) -> None:
        super().__init__("Aqua V1", "proplayer919")

    def evaluate_board(self, board: chess.Board, color: chess.Color) -> float:
        piece_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None and piece.color == color:
                piece_score += piece_values[piece.piece_type]

        attack_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None and piece.color != color:
                for attacker in board.attackers(color, square):
                    attack_score += 0.05

        defense_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None and piece.color == color:
                for defender in board.attackers(color, square):
                    defense_score += 0.05

        check_score = 2 if board.is_check() else 0

        combined_score = piece_score + attack_score + defense_score + check_score

        return float('inf') if board.is_checkmate() else combined_score

    async def move(self, board: chess.Board, color: chess.Color) -> chess.Move:
        moves = list(board.generate_legal_moves())

        best_move = None
        best_evaluation = float('-inf')

        for move in moves:
            new_board = board.copy()
            new_board.push(move)
            evaluation = (self.evaluate_board(new_board, color) + 0.5) if board.is_capture(move) else self.evaluate_board(new_board, color)

            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_move = move

        return best_move
