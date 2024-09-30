from chessaholic import ChessGame
from Aqua1 import Aqua1
from Aqua2 import Aqua2
from Aqua3 import Aqua3
from Aqua4 import Aqua4
from randombot import RandomBot
import asyncio


async def main():
    game = ChessGame(use_gui=True, white=Aqua2(), black=Aqua4())
    await game.play_game()


asyncio.run(main())
