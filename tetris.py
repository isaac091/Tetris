import sys, pygame, copy, random, time, numpy as np

pygame.init()

black = 0, 0, 0
screen = pygame.display.set_mode([750, 750])
sq_size = 25
board_width = 10
board_height = 20

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
        left = board_width

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
        top = board_height

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
    for i in range(1, board_width + 2):
        pygame.draw.line(screen, (255, 255, 255), [i * sq_size, sq_size], [i * sq_size, (board_height + 1) * sq_size])
    for i in range (1, board_height + 2):
        pygame.draw.line(screen, (255, 255, 255), [sq_size, i * sq_size], [(board_width + 1) * sq_size, i * sq_size])

last_time_moved = time.time()
piece_place_delay = time.time()
delay_started = False
new_piece = True
curr_piece_index = 0
curr_piece = pieces[0]

col_tops = np.full((1, board_width), board_height + 1)
dead_blocks = []
dead_blocks_colors = []

move_delay = .5

def is_collision(direction):
    dir_x = 0
    dir_y = 0

    if direction == "left":
        dir_x = -1
    elif direction == "right":
        dir_x = 1
    elif direction == "down":
        dir_y = 1

    for coord in curr_piece.rect_coords:
        for block in dead_blocks:
            if coord[0] + dir_x == block[0] and coord[1] + dir_y == block[1]:
                return True

while 1:
    if new_piece:
        # reset start position for next piece of the same type
        pieces[curr_piece_index].rect_coords = copy.deepcopy(block_rects[pieces[curr_piece_index].shape + "_rects"])

        curr_piece_index = random.randint(0,6)
        curr_piece = pieces[curr_piece_index]

        new_piece = False
        delay_started = False

    if curr_piece.get_bottom() > board_height or is_collision("down"):
        if not delay_started:
            piece_place_delay = time.time()
            delay_started = True

        if delay_started and time.time() - piece_place_delay > move_delay - .01:
            for coord in curr_piece.rect_coords:
                dead_blocks.append(coord)
                dead_blocks_colors.append(curr_piece.color)

            new_piece = True
    else:
        delay_started = False

    if time.time() - last_time_moved > move_delay and not is_collision("down") and not curr_piece.get_bottom() > board_height:
        last_time_moved = time.time()
        curr_piece.move(0, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and curr_piece.get_top() > 1: # change to rotate
                curr_piece.move(0, -1)
            elif event.key == pygame.K_a and curr_piece.get_left() > 1 and not is_collision("left"):
                curr_piece.move(-1, 0)
            elif event.key == pygame.K_s and curr_piece.get_bottom() < board_height + 1 and not is_collision("down"):
                curr_piece.move(0, 1)
            elif event.key == pygame.K_d and curr_piece.get_right() < board_width + 1 and not is_collision("right"):
                curr_piece.move(1, 0)
            elif event.key == pygame.K_r:
                new_piece = True;

    screen.fill(black)

    for i in range(len(dead_blocks)):
        pygame.draw.rect(screen, dead_blocks_colors[i], pygame.Rect(dead_blocks[i][0] * sq_size, dead_blocks[i][1] * sq_size, sq_size, sq_size))

    curr_piece.draw()

    draw_grid()

    pygame.display.flip()
