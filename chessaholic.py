import pygame
import chess


def is_middle_game(board: chess.Board) -> bool:
    # Count the major and minor pieces remaining
    piece_count = 0
    for piece_type in [chess.ROOK, chess.QUEEN, chess.BISHOP, chess.KNIGHT]:
        piece_count += len(board.pieces(piece_type, chess.WHITE)) + len(
            board.pieces(piece_type, chess.BLACK)
        )

    # Middle game is roughly when both sides have 5 or more major and minor pieces
    return piece_count > 10


piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0,
}

king_table_midgame = [
    -3.0,
    -4.0,
    -4.0,
    -5.0,
    -5.0,
    -4.0,
    -4.0,
    -3.0,
    -3.0,
    -4.0,
    -4.0,
    -5.0,
    -5.0,
    -4.0,
    -4.0,
    -3.0,
    -3.0,
    -4.0,
    -4.0,
    -5.0,
    -5.0,
    -4.0,
    -4.0,
    -3.0,
    -3.0,
    -4.0,
    -4.0,
    -5.0,
    -5.0,
    -4.0,
    -4.0,
    -3.0,
    -2.0,
    -3.0,
    -3.0,
    -4.0,
    -4.0,
    -3.0,
    -3.0,
    -2.0,
    -1.0,
    -2.0,
    -2.0,
    -2.0,
    -2.0,
    -2.0,
    -2.0,
    -1.0,
    2.0,
    2.0,
    0.0,
    0.0,
    0.0,
    0.0,
    2.0,
    2.0,
    2.0,
    3.0,
    1.0,
    0.0,
    0.0,
    1.0,
    3.0,
    2.0,
]

king_table_endgame = [
    -5.0,
    -4.0,
    -3.0,
    -2.0,
    -2.0,
    -3.0,
    -4.0,
    -5.0,
    -3.0,
    -2.0,
    -1.0,
    0.0,
    0.0,
    -1.0,
    -2.0,
    -3.0,
    -3.0,
    -1.0,
    2.0,
    3.0,
    3.0,
    2.0,
    -1.0,
    -3.0,
    -3.0,
    -1.0,
    3.0,
    4.0,
    4.0,
    3.0,
    -1.0,
    -3.0,
    -3.0,
    -1.0,
    3.0,
    4.0,
    4.0,
    3.0,
    -1.0,
    -3.0,
    -3.0,
    -1.0,
    2.0,
    3.0,
    3.0,
    2.0,
    -1.0,
    -3.0,
    -3.0,
    -3.0,
    0.0,
    0.0,
    0.0,
    0.0,
    -3.0,
    -3.0,
    -5.0,
    -3.0,
    -3.0,
    -3.0,
    -3.0,
    -3.0,
    -3.0,
    -5.0,
]


def get_position_table(board: chess.Board) -> dict[list[float]]:
    position_tables = {
        chess.PAWN: [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            5.0,
            5.0,
            5.0,
            5.0,
            5.0,
            5.0,
            5.0,
            5.0,
            1.0,
            1.0,
            2.0,
            3.0,
            3.0,
            2.0,
            1.0,
            1.0,
            0.5,
            0.5,
            1.0,
            2.5,
            2.5,
            1.0,
            0.5,
            0.5,
            0.0,
            0.0,
            0.0,
            2.0,
            2.0,
            0.0,
            0.0,
            0.0,
            0.5,
            -0.5,
            -1.0,
            0.0,
            0.0,
            -1.0,
            -0.5,
            0.5,
            0.5,
            1.0,
            1.0,
            -2.0,
            -2.0,
            1.0,
            1.0,
            0.5,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ],
        chess.KNIGHT: [
            -5.0,
            -4.0,
            -3.0,
            -3.0,
            -3.0,
            -3.0,
            -4.0,
            -5.0,
            -4.0,
            -2.0,
            0.0,
            0.5,
            0.5,
            0.0,
            -2.0,
            -4.0,
            -3.0,
            0.5,
            1.0,
            1.5,
            1.5,
            1.0,
            0.5,
            -3.0,
            -3.0,
            0.0,
            1.5,
            2.0,
            2.0,
            1.5,
            0.0,
            -3.0,
            -3.0,
            0.5,
            1.5,
            2.0,
            2.0,
            1.5,
            0.5,
            -3.0,
            -3.0,
            0.0,
            1.0,
            1.5,
            1.5,
            1.0,
            0.0,
            -3.0,
            -4.0,
            -2.0,
            0.0,
            0.5,
            0.5,
            0.0,
            -2.0,
            -4.0,
            -5.0,
            -4.0,
            -3.0,
            -3.0,
            -3.0,
            -3.0,
            -4.0,
            -5.0,
        ],
        chess.BISHOP: [
            -2.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -2.0,
            -1.0,
            0.0,
            0.0,
            0.5,
            0.5,
            0.0,
            0.0,
            -1.0,
            -1.0,
            0.0,
            0.5,
            1.0,
            1.0,
            0.5,
            0.0,
            -1.0,
            -1.0,
            0.5,
            0.5,
            1.0,
            1.0,
            0.5,
            0.5,
            -1.0,
            -1.0,
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            -1.0,
            -1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            -1.0,
            -1.0,
            0.5,
            0.0,
            0.0,
            0.0,
            0.0,
            0.5,
            -1.0,
            -2.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -1.0,
            -2.0,
        ],
        chess.ROOK: [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.5,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.5,
            -0.5,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            -0.5,
            -0.5,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            -0.5,
            -0.5,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            -0.5,
            -0.5,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            -0.5,
            -0.5,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            -0.5,
            0.0,
            0.0,
            0.0,
            0.5,
            0.5,
            0.0,
            0.0,
            0.0,
        ],
        chess.QUEEN: [
            -2.0,
            -1.0,
            -1.0,
            -0.5,
            -0.5,
            -1.0,
            -1.0,
            -2.0,
            -1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            -1.0,
            -1.0,
            0.0,
            0.5,
            0.5,
            0.5,
            0.5,
            0.0,
            -1.0,
            -0.5,
            0.0,
            0.5,
            0.5,
            0.5,
            0.5,
            0.0,
            -0.5,
            0.0,
            0.0,
            0.5,
            0.5,
            0.5,
            0.5,
            0.0,
            -0.5,
            -1.0,
            0.5,
            0.5,
            0.5,
            0.5,
            0.5,
            0.0,
            -1.0,
            -1.0,
            0.0,
            0.5,
            0.0,
            0.0,
            0.0,
            0.0,
            -1.0,
            -2.0,
            -1.0,
            -1.0,
            -0.5,
            -0.5,
            -1.0,
            -1.0,
            -2.0,
        ],
        chess.KING: king_table_midgame if is_middle_game(board) else king_table_endgame,
    }
    return position_tables


def evaluate_board(board: chess.Board, color: chess.Color) -> float:
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
                positional_score += get_position_table(board)[piece.piece_type][square]

    # Bonus for king safety (encourage checks and checkmates)
    check_bonus = 0
    if board.is_check():
        check_bonus = 10  # Increase the weight of checks slightly

    # Combine scores
    combined_score = piece_score + positional_score + check_bonus

    # Return score based on the current turn
    return combined_score if board.turn == color else -combined_score


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

    def move(self, board: chess.Board, color: chess.Color) -> chess.Move:
        """Get a move from the engine."""
        pass


class ChessGame:
    def __init__(self, white: ChessEngine = None, black: ChessEngine = None):
        self.board = chess.Board()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))
        pygame.display.set_caption(f"Chessaholic Game: {white.name if white else 'Human'} vs. {black.name if black else 'Human'}")
        self.selected_square = None
        self.legal_moves = []
        self.white = white
        self.black = black
        self.game_over = False

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
            pygame.Rect(WIDTH + 10, 280, SIDEBAR_WIDTH - 20, HEIGHT // 8),
        )

        # Game status
        if self.board.is_checkmate():
            winner = "Black" if self.board.turn == chess.WHITE else "White"
            status_text = f"Winner: {winner}"
            self.game_over = True
        elif self.board.is_stalemate():
            status_text = "Stalemate"
            self.game_over = True
        elif self.board.is_insufficient_material():
            status_text = "Draw: Insufficient Material"
            self.game_over = True
        elif self.board.is_fivefold_repetition():
            status_text = "Draw: 5-fold Repetition"
            self.game_over = True
        elif self.board.is_seventyfive_moves():
            status_text = "Draw: 75-move Rule"
            self.game_over = True
        else:
            status_text = ""

        if status_text:
            draw_text_wrapped(
                self.screen,
                status_text,
                font,
                TEXT_COLOR,
                pygame.Rect(WIDTH + 10, 370, SIDEBAR_WIDTH - 20, HEIGHT // 8),
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
        """Display a UI for choosing a promotion piece."""
        promotion_pieces = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
        promotion_names = ["Queen", "Rook", "Bishop", "Knight"]

        # Simple console input for promotion choice (you can make a Pygame UI)
        print("Choose a promotion piece:")
        for i, name in enumerate(promotion_names):
            print(f"{i + 1}: {name}")

        choice = 0
        while choice not in range(1, 5):
            choice = int(input("Enter 1-4: "))

        return promotion_pieces[choice - 1]

    def play_game(self):
        """Main loop for the game."""
        running = True
        clock = pygame.time.Clock()

        while running and not self.game_over:
            current_player = (
                self.white if self.board.turn == chess.WHITE else self.black
            )

            if not current_player:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_click(pygame.mouse.get_pos())
            else:
                move = current_player.move(board=self.board, color=self.board.turn)
                self.board.push(move)

            # Draw board, pieces, and sidebar
            self.draw_board()
            self.draw_pieces()
            if self.selected_square: self.draw_avalable_moves(self.selected_square)
            self.draw_sidebar()

            # Update the display
            pygame.display.update()

            clock.tick(60)

        if self.game_over:
            print(self.board.result())

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
