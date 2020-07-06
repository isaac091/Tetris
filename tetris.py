import sys, pygame
pygame.init()

black = 0, 0, 0
screen = pygame.display.set_mode([750, 750])

def draw_grid():
    for i in range(1, 12):
        pygame.draw.line(screen, (255, 255, 255), [i * 25, 25], [i * 25, 525])
    for i in range (1, 22):
        pygame.draw.line(screen, (255, 255, 255), [25, i * 25], [275, i * 25])

square = pygame.Rect(25, 25, 25, 25);

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and square.top > 25:
                square = square.move(0, -25)
            elif event.key == pygame.K_a and square.left > 25:
                square = square.move(-25, 0)
            elif event.key == pygame.K_s and square.top < 500:
                square = square.move(0, 25)
            elif event.key == pygame.K_d and square.left < 250:
                square = square.move(25, 0)

    screen.fill(black)

    pygame.draw.rect(screen, (0, 255, 0), square)
    draw_grid()

    pygame.display.flip()
