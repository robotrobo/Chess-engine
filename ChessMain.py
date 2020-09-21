import pygame
import ChessEngine
from ChessEngine import Move

IMAGES = {}
WIDTH = HEIGHT = 512
DIMENSION = 8  # for the chess board
SQUARE_SIZE = WIDTH // DIMENSION


def load_images():
    global IMAGES
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    for piece in pieces:
        IMAGES[piece] = pygame.image.load(f"images/{piece}.png")


def draw_state(screen, board, sqSelected):
    draw_board(screen)
    highlight_squares(screen, sqSelected)
    draw_pieces(screen, board)


def draw_board(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def draw_pieces(screen, board):
    # board = game_state.board
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def highlight_squares(screen, selected_sq):
    if selected_sq:
        # print(selected_sq)
        r, c = selected_sq
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        s.set_alpha(100)
        s.fill(pygame.Color('red'))
        screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))


def main():
    pygame.init()
    load_images()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False
    running = True
    selected_sq = ()  # keeping track of last click
    player_clicks = []  # keep track of last 2 clicks
    while running:
        for e in pygame.event.get():

            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                print(player_clicks)
                location = pygame.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE

                if selected_sq == (row, col):
                    selected_sq = ()
                    player_clicks = []
                else:

                    selected_sq = (row, col)
                    player_clicks.append(selected_sq)
                    toPlay = "w" if game_state.white_to_move else "b"
                    if len(player_clicks) == 2:
                        move = Move(game_state.board, player_clicks[0], player_clicks[1])
                        # print(move.get_notation())
                        if move in valid_moves:
                            game_state.make_move(move)
                            move_made = True
                            player_clicks = []
                            selected_sq = []
                        else:
                            player_clicks = [selected_sq]

            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    game_state.undo_move()
                    move_made = True
        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False
        draw_state(screen, game_state.board, selected_sq)
        clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    main()
