import sys, pygame
pygame.init()

black = 0, 0, 0
screen = pygame.display.set_mode([750, 750])

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

s_pts = [[150, 25], [150, 50], [175, 50], [175, 75], [175, 100], [150, 100], [150, 75], [125, 75], [125, 50], [125, 25]]
z_pts = [[150, 25], [175, 25], [175, 50], [175, 75], [150, 75], [150, 100], [125, 100], [125, 75], [125, 50], [150, 50]]
j_pts = [[150, 25], [175, 25], [175, 50], [175, 75], [175, 100], [150, 100], [125, 100], [125, 75], [150, 75], [150, 50]]
l_pts = [[150, 25], [150, 50], [150, 75], [175, 75], [175, 100], [150, 100], [125, 100], [125, 75], [125, 50], [125, 25]]
t_pts = [[150, 25], [150, 50], [175, 50], [175, 75], [150, 75], [150, 100], [125, 100], [125, 75], [125, 50], [125, 25]]
i_pts = [[150, 25], [175, 25], [200, 25], [200, 50], [175, 50], [150, 50], [125, 50], [100, 50], [100, 25], [125, 25]]
o_pts = [[150, 25], [175, 25], [175, 50], [175, 75], [150, 75], [125, 75], [125, 50], [125, 25]]
pieces = [s_pts, z_pts, j_pts, l_pts, t_pts, i_pts, o_pts]

s = pygame.draw.polygon(screen, (0, 0, 255), s_pts)

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and s.top > 25:
                s_pts = move_poly(s_pts, 0, -25)
            elif event.key == pygame.K_a and s.left > 25:
                s_pts = move_poly(s_pts, -25, 0)
            elif event.key == pygame.K_s and s.top < 500:
                s_pts = move_poly(s_pts, 0, 25)
            elif event.key == pygame.K_d and s.left < 250:
                s_pts = move_poly(s_pts, 25, 0)

    screen.fill(black)

    s = pygame.draw.polygon(screen, (0, 0, 255), s_pts)
    draw_grid()

    pygame.display.flip()
