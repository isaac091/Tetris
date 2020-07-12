import sys, pygame
import copy
import random
pygame.init()

black = 0, 0, 0
screen = pygame.display.set_mode([750, 750])

class Piece:
    def __init__(self, pts, color):
        self.pts = pts
        self.color = color

all_pts = {
    "s_pts": [[150, 25], [150, 50], [175, 50], [175, 75], [175, 100], [150, 100], [150, 75], [125, 75], [125, 50], [125, 25]],
    "z_pts": [[150, 25], [175, 25], [175, 50], [175, 75], [150, 75], [150, 100], [125, 100], [125, 75], [125, 50], [150, 50]],
    "j_pts": [[150, 25], [175, 25], [175, 50], [175, 75], [175, 100], [150, 100], [125, 100], [125, 75], [150, 75], [150, 50]],
    "l_pts": [[150, 25], [150, 50], [150, 75], [175, 75], [175, 100], [150, 100], [125, 100], [125, 75], [125, 50], [125, 25]],
    "t_pts": [[150, 25], [150, 50], [175, 50], [175, 75], [150, 75], [150, 100], [125, 100], [125, 75], [125, 50], [125, 25]],
    "i_pts": [[150, 25], [175, 25], [200, 25], [200, 50], [175, 50], [150, 50], [125, 50], [100, 50], [100, 25], [125, 25]],
    "o_pts": [[150, 25], [175, 25], [175, 50], [175, 75], [150, 75], [125, 75], [125, 50], [125, 25]]
}

pieces = [Piece(copy.deepcopy(all_pts["s_pts"]), (255, 0, 0)),
          Piece(copy.deepcopy(all_pts["z_pts"]), (255, 0, 0)),
          Piece(copy.deepcopy(all_pts["j_pts"]), (255, 0, 0)),
          Piece(copy.deepcopy(all_pts["l_pts"]), (255, 0, 0)),
          Piece(copy.deepcopy(all_pts["t_pts"]), (255, 0, 0)),
          Piece(copy.deepcopy(all_pts["i_pts"]), (255, 0, 0)),
          Piece(copy.deepcopy(all_pts["o_pts"]), (255, 0, 0))]
piece_names = ["s", "z", "j", "l", "t", "i", "o"]

def draw_grid():
    for i in range(1, 12):
        pygame.draw.line(screen, (255, 255, 255), [i * 25, 25], [i * 25, 525])
    for i in range (1, 22):
        pygame.draw.line(screen, (255, 255, 255), [25, i * 25], [275, i * 25])

def move_poly(pts, x, y):
    for pt in pts:
        pt[0] = pt[0] + x
        pt[1] = pt[1] + y

    return pts

new_piece = True
curr_piece_index = 0
curr_piece = pygame.draw.polygon(screen, pieces[curr_piece_index].color, pieces[curr_piece_index].pts)

while 1:
    if new_piece:
        # reset start position for next piece of the same type
        pieces[curr_piece_index] = Piece(copy.deepcopy(all_pts[piece_names[curr_piece_index] + "_pts"]), (255, 0, 0))

        curr_piece_index = random.randint(0,6)
        new_piece = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and curr_piece.top > 25:
                pieces[curr_piece_index].pts = move_poly(pieces[curr_piece_index].pts, 0, -25)
            elif event.key == pygame.K_a and curr_piece.left > 25:
                pieces[curr_piece_index].pts = move_poly(pieces[curr_piece_index].pts, -25, 0)
            elif event.key == pygame.K_s and curr_piece.top + curr_piece.height < 525:
                pieces[curr_piece_index].pts = move_poly(pieces[curr_piece_index].pts, 0, 25)
            elif event.key == pygame.K_d and curr_piece.left + curr_piece.width < 275:
                pieces[curr_piece_index].pts = move_poly(pieces[curr_piece_index].pts, 25, 0)
            elif event.key == pygame.K_r:
                new_piece = True;

    screen.fill(black)

    curr_piece = pygame.draw.polygon(screen, pieces[curr_piece_index].color, pieces[curr_piece_index].pts)

    draw_grid()

    pygame.display.flip()
