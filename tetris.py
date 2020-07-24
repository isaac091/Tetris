import sys, pygame
import copy
import random
import time
pygame.init()

black = 0, 0, 0
screen = pygame.display.set_mode([750, 750])
sq_size = 25

class Piece:
    def __init__(self, rect_coords, color, shape):
        # in the form [(left_coord, top_coord), (l, t), (l, t), (l, t)]
        self.rect_coords = rect_coords

        # in the form (r, g, b)
        self.color = color

        # i.e. 's'
        self.shape = shape

    def draw(self):
        for coord in self.rect_coords:
            pygame.draw.rect(screen, self.color, pygame.Rect(coord[0] * sq_size, coord[1] * sq_size, sq_size, sq_size))

    def move(self, x, y):
        for i in range(4):
            self.rect_coords[i][0] = self.rect_coords[i][0] + x
            self.rect_coords[i][1] = self.rect_coords[i][1] + y

    def get_left(self):
        left = 10

        for coord in self.rect_coords:
            if coord[0] < left:
                left = coord[0]

        return left

    def get_right(self):
        right = 1

        for coord in self.rect_coords:
            if coord[0] + 1 > right:
                right = coord[0] + 1

        return right

    def get_top(self):
        top = 10

        for coord in self.rect_coords:
            if coord[1] < top:
                top = coord[1]

        return top

    def get_bottom(self):
        bottom = 1

        for coord in self.rect_coords:
            if coord[1] + 1 > bottom:
                bottom = coord[1] + 1

        return bottom

block_rects = {
    "s_rects": [[5, 1], [5, 2], [6, 2], [6, 3]],
    "z_rects": [[6, 1], [6, 2], [5, 2], [5, 3]],
    "j_rects": [[6, 1], [6, 2], [6, 3], [5 ,3]],
    "l_rects": [[5, 1], [5, 2], [5, 3], [6, 3]],
    "t_rects": [[5, 1], [5, 2], [5, 3], [6, 2]],
    "i_rects": [[4, 1], [5, 1], [6, 1], [7, 1]],
    "o_rects": [[5, 1], [5, 2], [6, 1], [6, 2]]
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
        pygame.draw.line(screen, (255, 255, 255), [i * sq_size, sq_size], [i * sq_size, 21 * sq_size])
    for i in range (1, 22):
        pygame.draw.line(screen, (255, 255, 255), [sq_size, i * sq_size], [11 * sq_size, i * sq_size])

last_time_moved = time.time()
new_piece = True
curr_piece_index = 0
curr_piece = pieces[0]

while 1:
    if new_piece:
        # reset start position for next piece of the same type
        pieces[curr_piece_index].rect_coords = copy.deepcopy(block_rects[pieces[curr_piece_index].shape + "_rects"])

        curr_piece_index = random.randint(0,6)
        curr_piece = pieces[curr_piece_index]
        new_piece = False

    if curr_piece.get_bottom() > 21:
        '''TODO: add logic for saving final positions of rectangles and update if statement to track if a piece hits the top of a column, not just the bottom '''
        new_piece = True;

    if time.time() - last_time_moved >= .5:
        last_time_moved = time.time()
        curr_piece.move(0, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and curr_piece.get_top() > 1:
                curr_piece.move(0, -1)
            elif event.key == pygame.K_a and curr_piece.get_left() > 1:
                curr_piece.move(-1, 0)
            elif event.key == pygame.K_s and curr_piece.get_bottom() < 21:
                curr_piece.move(0, 1)
            elif event.key == pygame.K_d and curr_piece.get_right() < 11:
                curr_piece.move(1, 0)
            elif event.key == pygame.K_r:
                new_piece = True;

    screen.fill(black)

    curr_piece.draw()

    draw_grid()

    pygame.display.flip()
