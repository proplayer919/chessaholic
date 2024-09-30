import pygame
import chess
import time
import asyncio


piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

# Constants for display
WIDTH, HEIGHT = 512, 512
SIDEBAR_WIDTH = 200  # Width of the sidebar
SCREEN_WIDTH = WIDTH + SIDEBAR_WIDTH  # Total width with sidebar
SQUARE_SIZE = WIDTH // 8
WHITE = (255, 207, 159)
BLACK = (210, 140, 69)
DOT_COLOR = (0, 255, 0)
DOT_COLOR_CAPTURE = (255, 0, 0)
DOT_COLOR_SELECT = (0, 0, 255)
SIDEBAR_BG = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)

# Time controls (5 minutes per player)
TIME_CONTROL = "2+5"  # 30 minutes per player

# Initialize pygame
pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 24)

# Load piece images
PIECES = {
    "r": pygame.image.load("images/black_rook.png"),
    "n": pygame.image.load("images/black_knight.png"),
    "b": pygame.image.load("images/black_bishop.png"),
    "q": pygame.image.load("images/black_queen.png"),
    "k": pygame.image.load("images/black_king.png"),
    "p": pygame.image.load("images/black_pawn.png"),
    "R": pygame.image.load("images/white_rook.png"),
    "N": pygame.image.load("images/white_knight.png"),
    "B": pygame.image.load("images/white_bishop.png"),
    "Q": pygame.image.load("images/white_queen.png"),
    "K": pygame.image.load("images/white_king.png"),
    "P": pygame.image.load("images/white_pawn.png"),
}

# Resize pieces to fit the board
for piece in PIECES:
    PIECES[piece] = pygame.transform.scale(PIECES[piece], (SQUARE_SIZE, SQUARE_SIZE))


def parse_time(time_str):
    """Parse a time control string into minutes to start and seconds to add per move."""
    minutes, seconds = time_str.split("+")
    return int(minutes), int(seconds)


def draw_text_wrapped(surface, text, font, color, rect):
    """Draw text with wrapping if it exceeds the width of the rect."""
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        # Check if adding the next word will exceed the width
        if font.size(current_line + word)[0] < rect.width:
            current_line += word + " "
        else:
            # Add the current line and start a new one
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)  # Add the last line

    y = rect.top
    for line in lines:
        if y + font.get_height() > rect.bottom:
            break  # Stop drawing if we've reached the bottom of the rect
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (rect.left, y))
        y += font.get_height()


class ChessEngine:
    def __init__(self, name: str = "ChessEngine", author: str = "Anonymous") -> None:
        self.name = name
        self.author = author

    async def move(
        self,
        board: chess.Board,
        color: chess.Color,
        time_remaining: int,
        time_increment: int,
    ) -> chess.Move:
        """Get a move from the engine."""
        pass


class ChessGame:
    def __init__(
        self, use_gui: bool = True, white: ChessEngine = None, black: ChessEngine = None
    ):
        self.use_gui = use_gui

        self.board = chess.Board()

        if use_gui:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
            pygame.display.set_caption(
                f"Chessaholic Game: {white.name if white else 'Human'} vs. {black.name if black else 'Human'}"
            )
            self.selected_square = None
            self.clock = pygame.time.Clock()

        self.legal_moves = []
        self.white = white
        self.black = black
        self.game_over = False

        # Initialize clocks
        self.white_time = parse_time(TIME_CONTROL)[0] * 60
        self.black_time = self.white_time
        self.time_bonus = parse_time(TIME_CONTROL)[1]
        self.last_move_time = time.time()  # Store the last time a move was made
        self.current_turn_time = None

    def draw_board(self):
        """Draws the chessboard."""
        colors = [WHITE, BLACK]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                    ),
                )

    def draw_pieces(self):
        """Draws the chess pieces based on the board's FEN."""
        fen = self.board.board_fen()
        rows = fen.split(" ")[0].split("/")

        for row_idx, row in enumerate(rows):
            col_idx = 0
            for char in row:
                if char.isdigit():
                    # Empty squares, skip by that many columns
                    col_idx += int(char)
                else:
                    # Draw the piece
                    self.screen.blit(
                        PIECES[char],
                        pygame.Rect(
                            col_idx * SQUARE_SIZE,
                            row_idx * SQUARE_SIZE,
                            SQUARE_SIZE,
                            SQUARE_SIZE,
                        ),
                    )
                    col_idx += 1

    def update_time(self):
        """Update the time for the current player."""
        now = time.time()
        if self.board.turn == chess.WHITE:
            self.white_time -= now - self.last_move_time
        else:
            self.black_time -= now - self.last_move_time
        self.last_move_time = now

        # Check for time out
        if self.white_time <= 0:
            self.game_over = True
            self.show_result("Black wins on time!")
        elif self.black_time <= 0:
            self.game_over = True
            self.show_result("White wins on time!")

    def draw_sidebar(self):
        """Draws the sidebar with player information and game status."""
        pygame.draw.rect(
            self.screen, SIDEBAR_BG, pygame.Rect(WIDTH, 0, SIDEBAR_WIDTH, HEIGHT)
        )

        # White
        white_name = (
            "Human" if not self.white else f"{self.white.name} ({self.white.author})"
        )
        draw_text_wrapped(
            self.screen,
            f"White: {white_name}",
            font,
            TEXT_COLOR,
            pygame.Rect(WIDTH + 10, 10, SIDEBAR_WIDTH - 20, HEIGHT // 8),
        )

        # Black
        black_name = (
            "Human" if not self.black else f"{self.black.name} ({self.black.author})"
        )
        draw_text_wrapped(
            self.screen,
            f"Black: {black_name}",
            font,
            TEXT_COLOR,
            pygame.Rect(WIDTH + 10, 100, SIDEBAR_WIDTH - 20, HEIGHT // 8),
        )
        # Turn Information
        turn_text = "White" if self.board.turn == chess.WHITE else "Black"
        draw_text_wrapped(
            self.screen,
            f"Turn: {turn_text}",
            font,
            TEXT_COLOR,
            pygame.Rect(WIDTH + 10, 190, SIDEBAR_WIDTH - 20, HEIGHT // 8),
        )

        # Move amount
        move_count = self.board.fullmove_number
        draw_text_wrapped(
            self.screen,
            f"Move: {move_count}",
            font,
            TEXT_COLOR,
            pygame.Rect(WIDTH + 10, 230, SIDEBAR_WIDTH - 20, HEIGHT // 8),
        )

        # Game status
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            self.game_over = f"Winner: {winner}"
        elif self.board.is_stalemate():
            self.game_over = "Stalemate"
        elif self.board.is_insufficient_material():
            self.game_over = "Draw: Insufficient Material"
        elif self.board.is_fivefold_repetition():
            self.game_over = "Draw: 5-fold Repetition"
        elif self.board.is_seventyfive_moves():
            self.game_over = "Draw: 75-move Rule"
        else:
            self.game_over = ""

        if self.game_over:
            draw_text_wrapped(
                self.screen,
                self.game_over,
                font,
                TEXT_COLOR,
                pygame.Rect(WIDTH + 10, 320, SIDEBAR_WIDTH - 20, HEIGHT // 8),
            )

        # Draw clocks
        white_time_text = (
            f"White Time: {int(self.white_time // 60)}:{int(self.white_time % 60):02d}"
        )
        black_time_text = (
            f"Black Time: {int(self.black_time // 60)}:{int(self.black_time % 60):02d}"
        )
        draw_text_wrapped(
            self.screen,
            white_time_text,
            font,
            TEXT_COLOR,
            pygame.Rect(WIDTH + 10, 410, SIDEBAR_WIDTH - 20, HEIGHT // 8),
        )
        draw_text_wrapped(
            self.screen,
            black_time_text,
            font,
            TEXT_COLOR,
            pygame.Rect(WIDTH + 10, 460, SIDEBAR_WIDTH - 20, HEIGHT // 8),
        )

    def draw_avalable_moves(self, square: chess.Square):
        """Draws the available moves on the board for the selected piece."""
        pygame.draw.circle(
            self.screen,
            DOT_COLOR_SELECT,
            (
                (self.selected_square % 8) * SQUARE_SIZE + SQUARE_SIZE // 2,
                (7 - self.selected_square // 8) * SQUARE_SIZE + SQUARE_SIZE // 2,
            ),
            10,
        )

        for move in self.legal_moves:
            if move.from_square == square:
                pygame.draw.circle(
                    self.screen,
                    DOT_COLOR_CAPTURE if self.board.is_capture(move) else DOT_COLOR,
                    (
                        (move.to_square % 8) * SQUARE_SIZE + SQUARE_SIZE // 2,
                        (7 - move.to_square // 8) * SQUARE_SIZE + SQUARE_SIZE // 2,
                    ),
                    10,
                )

    def handle_click(self, pos: tuple[int, int]):
        """Handles mouse click events."""
        if pos[0] > WIDTH:  # Ignore clicks on the sidebar
            return

        if self.game_over:
            return

        self.update_time()  # Update time before handling move

        col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
        square = chess.square(col, 7 - row)

        if self.selected_square is None:
            # Select a piece
            if self.board.piece_at(square) is not None:
                self.selected_square = square
                self.legal_moves = [
                    move
                    for move in self.board.legal_moves
                    if move.from_square == square
                ]
        else:
            if self.board.turn == chess.WHITE:
                self.white_time += self.time_bonus
            else:
                self.black_time += self.time_bonus

            # Try to move the piece to the clicked square
            move = chess.Move(self.selected_square, square)

            # Check if the move is a pawn promotion
            if chess.PAWN == self.board.piece_type_at(self.selected_square) and (
                chess.square_rank(square) == 7 or chess.square_rank(square) == 0
            ):
                # Promotion handling
                promotion_piece = self.get_promotion_choice()
                move.promotion = promotion_piece

            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.legal_moves = []
            else:
                # Reset selection if illegal move
                self.selected_square = None
                self.legal_moves = []

    def get_promotion_choice(self) -> int:
        """Display a GUI for choosing a promotion piece."""
        promotion_pieces = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        promotion_names = ["Queen", "Rook", "Bishop", "Knight"]

        # Display promotion options
        promotion_popup = True
        while promotion_popup:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if WIDTH // 2 - 50 < x < WIDTH // 2 + 50:
                        for i, piece in enumerate(promotion_pieces):
                            if HEIGHT // 2 + i * 60 < y < HEIGHT // 2 + (i + 1) * 60:
                                promotion_popup = False
                                return piece

            self.screen.fill(WHITE)
            for i, name in enumerate(promotion_names):
                text = font.render(name, True, BLACK)
                self.screen.blit(
                    text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 60)
                )

            pygame.display.flip()

    async def play_game(self):
        if self.white is None or self.black is None:
            raise ValueError(
                "Both white and black engines must be provided to play the game."
            )

        running = True
        while running and not self.game_over:
            # Handle engine move if necessary
            current_player = (
                self.white if self.board.turn == chess.WHITE else self.black
            )
            self.update_time()
            
            move = await current_player.move(self.board, self.board.turn)
            if move and move in self.board.legal_moves:
                self.board.push(move)
                self.last_move_time = time.time()  # Reset last move time
                if self.board.turn == chess.WHITE:
                    self.white_time += self.time_bonus  # Increment time after each move
                else:
                    self.black_time += self.time_bonus

            # Update and draw game state
            self.update_time()
            if self.use_gui:
                self.draw_board()
                self.draw_pieces()
                self.draw_sidebar()
                pygame.display.flip()

                self.clock.tick(60)  # Maintain FPS to avoid excessive CPU usage

        if self.game_over:
            self.show_result(
                f"{self.game_over} in {self.board.fullmove_number} moves: {self.board.result()}"
            )

        if self.use_gui:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

    def show_result(self, result_text: str):
        """Display the result and end the game."""
        print(result_text)
