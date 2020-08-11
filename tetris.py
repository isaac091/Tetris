import sys, pygame, copy, random, time, numpy as np

pygame.init()

background_color = (150, 150, 150)
screen = pygame.display.set_mode([500, 600])
sq_size = 25
board_width = 10
board_height = 20
lines_cleared = 0
lines_until_next_level = 10
is_game_over = False

class Piece:
    def __init__(self, rect_coords, color, shape):
        # in the form [[left_coord, top_coord], [l, t], [l, t], [l, t]]
        self.rect_coords = rect_coords

        # in the form (r, g, b)
        self.color = color

        # i.e. 's'
        self.shape = shape

        # used for rotation
        self.state = 0

    def draw(self):
        for coord in self.rect_coords:
            pygame.draw.rect(screen, self.color, pygame.Rect(coord[0] * sq_size, coord[1] * sq_size, sq_size, sq_size))

    def move(self, x, y):
        for i in range(4):
            self.rect_coords[i][0] = self.rect_coords[i][0] + x
            self.rect_coords[i][1] = self.rect_coords[i][1] + y

    def rotate(self):
        new_pos = []

        if self.shape == "s":
            new_pos = self.__get_rotated_s()
        elif self.shape == "z":
            new_pos = self.__get_rotated_z()
        elif self.shape == "j":
            new_pos = self.__get_rotated_j()
        elif self.shape == "l":
            new_pos = self.__get_rotated_l()
        elif self.shape == "t":
            new_pos = self.__get_rotated_t()
        elif self.shape == "i":
            new_pos = self.__get_rotated_i()
        elif self.shape == "o":
            return

        for rect in new_pos:
            if rect[0] < 1 or rect[0] > board_width or rect[1] < 1 or rect[1] > board_height:
                return

            for block in dead_blocks:
                if block[0] == rect[0] and block[1] == rect[1]:
                    return

        self.rect_coords = new_pos
        self.state = (self.state + 1) % 4

    def __get_rotated_s(self):
        new_pos = []

        new_pos.append([self.rect_coords[0][0] + 2 * pow(-1, self.state), self.rect_coords[0][1]])
        new_pos.append([self.rect_coords[1][0], self.rect_coords[1][1]])
        new_pos.append([self.rect_coords[2][0], self.rect_coords[2][1]])
        new_pos.append([self.rect_coords[3][0], self.rect_coords[3][1] - 2 * pow(-1, self.state)])

        return new_pos

    def __get_rotated_z(self):
        new_pos = []

        new_pos.append([self.rect_coords[0][0], self.rect_coords[0][1] + 2 * pow(-1, self.state)])
        new_pos.append([self.rect_coords[1][0] - 2 * pow(-1, self.state), self.rect_coords[1][1]])
        new_pos.append([self.rect_coords[2][0], self.rect_coords[2][1]])
        new_pos.append([self.rect_coords[3][0], self.rect_coords[3][1]])

        return new_pos

    def __get_rotated_j(self):
        new_pos = []

        new_pos.append([self.rect_coords[0][0] + 1 * pow(-1, self.state), self.rect_coords[0][1] + 1 * pow(-1, self.state)])
        new_pos.append([self.rect_coords[1][0], self.rect_coords[1][1]])
        new_pos.append([self.rect_coords[2][0] - 1 * pow(-1, self.state), self.rect_coords[2][1] - 1 * pow(-1, self.state)])

        if self.state == 0:
            new_pos.append([self.rect_coords[3][0], self.rect_coords[3][1] - 2])
        elif self.state == 1:
            new_pos.append([self.rect_coords[3][0] + 2, self.rect_coords[3][1]])
        elif self.state == 2:
            new_pos.append([self.rect_coords[3][0], self.rect_coords[3][1] + 2])
        elif self.state == 3:
            new_pos.append([self.rect_coords[3][0] - 2, self.rect_coords[3][1]])

        return new_pos

    def __get_rotated_l(self):
        new_pos = []

        new_pos.append([self.rect_coords[0][0] + 1 * pow(-1, self.state), self.rect_coords[0][1] + 1 * pow(-1, self.state)])
        new_pos.append([self.rect_coords[1][0], self.rect_coords[1][1]])
        new_pos.append([self.rect_coords[2][0] - 1 * pow(-1, self.state), self.rect_coords[2][1] - 1 * pow(-1, self.state)])

        if self.state == 0:
            new_pos.append([self.rect_coords[3][0] - 2, self.rect_coords[3][1]])
        elif self.state == 1:
            new_pos.append([self.rect_coords[3][0], self.rect_coords[3][1] - 2])
        elif self.state == 2:
            new_pos.append([self.rect_coords[3][0] + 2, self.rect_coords[3][1]])
        elif self.state == 3:
            new_pos.append([self.rect_coords[3][0], self.rect_coords[3][1] + 2])

        return new_pos

    def __get_rotated_t(self):
        new_pos = []

        new_pos.append([self.rect_coords[0][0] + 1 * pow(-1, self.state), self.rect_coords[0][1] + 1 * pow(-1, self.state)])
        new_pos.append([self.rect_coords[1][0], self.rect_coords[1][1]])
        new_pos.append([self.rect_coords[2][0] - 1 * pow(-1, self.state), self.rect_coords[2][1] - 1 * pow(-1, self.state)])

        if self.state == 0:
            new_pos.append([self.rect_coords[3][0] - 1, self.rect_coords[3][1] + 1])
        elif self.state == 1:
            new_pos.append([self.rect_coords[3][0] - 1, self.rect_coords[3][1] - 1])
        elif self.state == 2:
            new_pos.append([self.rect_coords[3][0] + 1, self.rect_coords[3][1] - 1])
        elif self.state == 3:
            new_pos.append([self.rect_coords[3][0] + 1, self.rect_coords[3][1] + 1])

        return new_pos

    def __get_rotated_i(self):
        new_pos = []

        new_pos.append([self.rect_coords[0][0] + 2 * pow(-1, self.state), self.rect_coords[0][1] - 2 * pow(-1, self.state)])
        new_pos.append([self.rect_coords[1][0] + 1 * pow(-1, self.state), self.rect_coords[1][1] - 1 * pow(-1, self.state)])
        new_pos.append([self.rect_coords[2][0], self.rect_coords[2][1]])
        new_pos.append([self.rect_coords[3][0] - 1 * pow(-1, self.state), self.rect_coords[3][1] + 1 * pow(-1, self.state)])

        return new_pos

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
        pygame.draw.line(screen, (100, 100, 100), [i * sq_size, sq_size], [i * sq_size, (board_height + 1) * sq_size])
    for i in range (1, board_height + 2):
        pygame.draw.line(screen, (100, 100, 100), [sq_size, i * sq_size], [(board_width + 1) * sq_size, i * sq_size])

def draw_score():
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render("Lines " + str(lines_cleared), True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (14 * sq_size, 5 * sq_size)
    screen.blit(text, textRect)

def draw_game_over():
    font = pygame.font.Font("freesansbold.ttf", 32)
    text = font.render("Game Over", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (15 * sq_size, 10 * sq_size)
    screen.blit(text, textRect)

last_time_moved = time.time()
piece_place_delay = time.time()
delay_started = False
new_piece = True
next_piece_index = 0
curr_piece = pieces[0]
next_piece = copy.deepcopy(pieces[random.randint(0, 6)])

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
        if coord[0] + dir_x < 1 or coord[0] + dir_x > board_width:
            return True
        if coord[1] + dir_y < 1 or coord[1] + dir_y > board_height:
            return True

        for block in dead_blocks:
            if coord[0] + dir_x == block[0] and coord[1] + dir_y == block[1]:
                return True

def clear_full_lines():
    cleared = 0

    for i in range(1, board_height + 1):
        num_blocks_in_row = 0

        for block in dead_blocks:
            if block[1] == i:
                num_blocks_in_row = num_blocks_in_row + 1

        if num_blocks_in_row == board_width:
            cleared += 1

            for j in reversed(range(len(dead_blocks))):
                if dead_blocks[j][1] == i:
                    del dead_blocks[j]
                    del dead_blocks_colors[j]
                elif dead_blocks[j][1] < i:
                    dead_blocks[j][1] = dead_blocks[j][1] + 1

    return cleared

while 1:
    if new_piece:
        # reset start position for next piece of the same type

        curr_piece = copy.deepcopy(next_piece)

        next_piece_index = random.randint(0,6)
        next_piece = copy.deepcopy(pieces[next_piece_index])

        new_piece = False
        delay_started = False

        if is_collision(""):
            is_game_over = True

    if is_collision("down"):
        if not delay_started:
            piece_place_delay = time.time()
            delay_started = True

        if delay_started and time.time() - piece_place_delay > move_delay - .01:
            for coord in curr_piece.rect_coords:
                dead_blocks.append(coord)
                dead_blocks_colors.append(curr_piece.color)

            if not is_game_over:
                new_piece = True
    else:
        delay_started = False

    if time.time() - last_time_moved > move_delay and not is_collision("down") and not is_game_over:
        last_time_moved = time.time()
        curr_piece.move(0, 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN and not is_game_over:
            if event.key == pygame.K_w and curr_piece.get_top() > 1:
                curr_piece.rotate()
            elif event.key == pygame.K_a and not is_collision("left"):
                curr_piece.move(-1, 0)
            elif event.key == pygame.K_s and not is_collision("down"):
                curr_piece.move(0, 1)
            elif event.key == pygame.K_d and not is_collision("right"):
                curr_piece.move(1, 0)
            elif event.key == pygame.K_r:
                new_piece = True;

    screen.fill(background_color)

    full_lines = clear_full_lines()
    lines_until_next_level -= full_lines
    lines_cleared += full_lines

    if lines_until_next_level <= 0:
        lines_until_next_level += 10

        if move_delay >= .1:
            move_delay -= .02

    for i in range(len(dead_blocks)):
        pygame.draw.rect(screen, dead_blocks_colors[i], pygame.Rect(dead_blocks[i][0] * sq_size, dead_blocks[i][1] * sq_size, sq_size, sq_size))

    curr_piece.draw()

    # draw next piece
    for coord in pieces[next_piece_index].rect_coords:
        pygame.draw.rect(screen, pieces[next_piece_index].color, pygame.Rect((coord[0] + 7) * sq_size, coord[1] * sq_size, sq_size, sq_size))

    draw_grid()
    draw_score()
    if is_game_over:
        draw_game_over()

    pygame.display.flip()
