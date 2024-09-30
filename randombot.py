import chess
from chessaholic import ChessEngine
import random


class RandomBot(ChessEngine):
    def __init__(self) -> None:
        super().__init__("Random Bot", "proplayer919")
    
    async def move(self, board: chess.Board, color: chess.Color) -> chess.Move:
        print(f"{"White" if color == chess.WHITE else "Black"} is selecting a move...")
        moves = list(board.legal_moves)
        print(f"Picking a random move for {"white" if color == chess.WHITE else "black"}...")
        move = random.choice(moves)
        print(f"Best move for {"white" if color == chess.WHITE else "black"}: {move}")
        return move
