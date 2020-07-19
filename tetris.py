import sys, pygame
import copy
import random
import time
pygame.init()

black = 0, 0, 0
screen = pygame.display.set_mode([750, 750])

class Piece:
    def __init__(self, rects, color, shape):
        self.rects = rects
        self.color = color
        self.shape = shape

    def draw(self):
        for rect in self.rects:
            pygame.draw.rect(screen, self.color, rect)

    def move(self, x, y):
        for i in range(4):
            self.rects[i] = self.rects[i].move(x, y)

    def get_left(self):
        left = 10000

        for rect in self.rects:
            if rect.left < left:
                left = rect.left

        return left

    def get_right(self):
        right = 0

        for rect in self.rects:
            if rect.left + rect.width > right:
                right = rect.left + rect.width

        return right

    def get_top(self):
        top = 10000

        for rect in self.rects:
            if rect.top < top:
                top = rect.top

        return top

    def get_bottom(self):
        bottom = 0

        for rect in self.rects:
            if rect.top + rect.height > bottom:
                bottom = rect.top + rect.height

        return bottom

block_rects = {
    "s_rects": [pygame.Rect(125, 25, 25, 25), pygame.Rect(125, 50, 25, 25), pygame.Rect(150, 50, 25, 25), pygame.Rect(150, 75, 25, 25)],
    "z_rects": [pygame.Rect(150, 25, 25, 25), pygame.Rect(150, 50, 25, 25), pygame.Rect(125, 50, 25, 25), pygame.Rect(125, 75, 25, 25)],
    "j_rects": [pygame.Rect(150, 25, 25, 25), pygame.Rect(150, 50, 25, 25), pygame.Rect(150, 75, 25, 25), pygame.Rect(125, 75, 25, 25)],
    "l_rects": [pygame.Rect(125, 25, 25, 25), pygame.Rect(125, 50, 25, 25), pygame.Rect(125, 75, 25, 25), pygame.Rect(150, 75, 25, 25)],
    "t_rects": [pygame.Rect(125, 25, 25, 25), pygame.Rect(125, 50, 25, 25), pygame.Rect(125, 75, 25, 25), pygame.Rect(150, 50, 25, 25)],
    "i_rects": [pygame.Rect(100, 25, 25, 25), pygame.Rect(125, 25, 25, 25), pygame.Rect(150, 25, 25, 25), pygame.Rect(175, 25, 25, 25)],
    "o_rects": [pygame.Rect(125, 25, 25, 25), pygame.Rect(125, 50, 25, 25), pygame.Rect(150, 25, 25, 25), pygame.Rect(150, 50, 25, 25)]
}

pieces = [Piece(copy.deepcopy(block_rects["s_rects"]), (0, 240, 0), "s"),
          Piece(copy.deepcopy(block_rects["z_rects"]), (240, 0, 0), "z"),
          Piece(copy.deepcopy(block_rects["j_rects"]), (0, 0, 240), "j"),
          Piece(copy.deepcopy(block_rects["l_rects"]), (240, 160, 0), "l"),
          Piece(copy.deepcopy(block_rects["t_rects"]), (160, 0, 240), "t"),
          Piece(copy.deepcopy(block_rects["i_rects"]), (0, 240, 240), "i"),
          Piece(copy.deepcopy(block_rects["o_rects"]), (240, 240, 0), "o")]

def draw_grid():
    for i in range(1, 12):
        pygame.draw.line(screen, (255, 255, 255), [i * 25, 25], [i * 25, 525])
    for i in range (1, 22):
        pygame.draw.line(screen, (255, 255, 255), [25, i * 25], [275, i * 25])

last_time_moved = time.time()
new_piece = True
curr_piece_index = 0
curr_piece = pieces[0]

while 1:
    if new_piece:
        # reset start position for next piece of the same type
        pieces[curr_piece_index].rects = copy.deepcopy(block_rects[pieces[curr_piece_index].shape + "_rects"])

        curr_piece_index = random.randint(0,6)
        curr_piece = pieces[curr_piece_index]
        new_piece = False

    if curr_piece.get_bottom() > 525:
        new_piece = True;

    if time.time() - last_time_moved >= .5:
        last_time_moved = time.time()
        curr_piece.move(0, 25)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and curr_piece.get_top() > 25:
                curr_piece.move(0, -25)
            elif event.key == pygame.K_a and curr_piece.get_left() > 25:
                curr_piece.move(-25, 0)
            elif event.key == pygame.K_s and curr_piece.get_bottom() < 525:
                curr_piece.move(0, 25)
            elif event.key == pygame.K_d and curr_piece.get_right() < 275:
                curr_piece.move(25, 0)
            elif event.key == pygame.K_r:
                new_piece = True;

    screen.fill(black)

    curr_piece.draw()

    draw_grid()

    pygame.display.flip()
