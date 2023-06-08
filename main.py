import pygame
import random

pygame.init()

box_size = 30
box_width = 10
box_height = 20
width = box_size * box_width
height =box_size * box_height
side_width = 100
screen_width = width + side_width
white = (245,245,245)
black = (0, 0, 0)
line_color= (139,125,107)
cube_colors = [(255,245,40),(175,175,20),(185,185,185),(155,0,0),(175,20,20),(0, 155,0),(20,175,20),(0,0,155),(20,20,175)]

screen = pygame.display.set_mode((screen_width, height))
pygame.display.set_caption("テトリス")
clock = pygame.time.Clock()
FPS = 60


def draw_grids():
    for i in range(box_width):
        pygame.draw.line(screen, line_color, (i * box_size, 0), (i * box_size, height))

    for i in range(box_height):
        pygame.draw.line(screen, line_color, (0, i * box_size), (width, i * box_size))

    pygame.draw.line(screen, white, (box_size * box_width, 0), (box_size * box_width, box_size * box_height))

def show_text(surf, text, size, x, y, color=white):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
level = 1
def show_gameover(screen):
    show_text(screen, 'cube', 30, 225, 250)
    show_text(screen, 'press enter to start', 20, 225, 300)


screen_color_matrix = []
for i in range(box_height):
    screen_color_matrix.append([0] * box_width)

class CubeShape(object):
    shapes = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
    I = [[(0, -1), (0, 0), (0, 1), (0, 2)],
         [(-1, 0), (0, 0), (1, 0), (2, 0)]]
    J = [[(-2, 0), (-1, 0), (0, 0), (0, -1)],
         [(-1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, 1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (1, 0)]]
    L = [[(-2, 0), (-1, 0), (0, 0), (0, 1)],
         [(1, 0), (0, 0), (0, 1), (0, 2)],
         [(0, -1), (0, 0), (1, 0), (2, 0)],
         [(0, -2), (0, -1), (0, 0), (-1, 0)]]
    O = [[(0, 0), (0, 1), (1, 0), (1, 1)]]
    S = [[(-1, 0), (0, 0), (0, 1), (1, 1)],
         [(1, -1), (1, 0), (0, 0), (0, 1)]]
    T = [[(0, -1), (0, 0), (0, 1), (-1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, 1)],
         [(0, -1), (0, 0), (0, 1), (1, 0)],
         [(-1, 0), (0, 0), (1, 0), (0, -1)]]
    Z = [[(0, -1), (0, 0), (1, 0), (1, 1)],
         [(-1, 0), (0, 0), (0, -1), (1, -1)]]
    shapes_with_dir = {
        'I': I, 'J': J, 'L': L, 'O': O, 'S': S, 'T': T, 'Z': Z
    }
    def __init__(self):
        self.shape = self.shapes[random.randint(0, len(self.shapes) - 1)]
        self.center = (2, box_width // 2)
        self.dir = random.randint(0, len(self.shapes_with_dir[self.shape]) - 1)
        self.color = cube_colors[random.randint(0, len(cube_colors) - 1)]

    def get_all_gridpos(self, center=None):
        curr_shape = self.shapes_with_dir[self.shape][self.dir]
        if center is None:
            center = [self.center[0], self.center[1]]

        return [(cube[0] + center[0], cube[1] + center[1])
                for cube in curr_shape]
    def conflict(self, center):
        for cube in self.get_all_gridpos(center):
            if cube[0] < 0 or cube[1] < 0 or cube[0] >= box_height or cube[1] >= box_width:
                return True
            if screen_color_matrix[cube[0]][cube[1]] != 0:
                return True
        return False

    def rotate(self):
        new_dir = self.dir + 1
        new_dir %= len(self.shapes_with_dir[self.shape])
        old_dir = self.dir
        self.dir = new_dir
        if self.conflict(self.center):
            self.dir = old_dir
            return False

    def down(self):
        center = (self.center[0] + 1, self.center[1])
        if self.conflict(center):
            return False
        self.center = center
        return True

    def left(self):
        center = (self.center[0], self.center[1] - 1)
        if self.conflict(center):
            return False
        self.center = center
        return True

    def right(self):
        center = (self.center[0], self.center[1] + 1)
        if self.conflict(center):
            return False
        self.center = center
        return True

    def draw(self):
        for cube in self.get_all_gridpos():
            pygame.draw.rect(screen, self.color,
                             (cube[1] * box_size, cube[0] * box_size,
                              box_size, box_size))
            pygame.draw.rect(screen, white,
                             (cube[1] * box_size, cube[0] * box_size,
                              box_size, box_size),
                             1)
def draw_matrix():
    for i, row in zip(range(box_height), screen_color_matrix):
        for j, color in zip(range(box_width), row):
            if color != 0:
                pygame.draw.rect(screen, color,
                                 (j * box_size, i * box_size,
                                  box_size, box_size))
                pygame.draw.rect(screen, white,
                                 (j * box_size, i * box_size,
                                  box_size, box_size), 2)


def remove_full_line():
    global screen_color_matrix

    new_matrix = [[0] * box_width for i in range(box_height)]
    index = box_height - 1
    n_full_line = 0
    for i in range(box_height - 1, -1, -1):
        is_full = True
        for j in range(box_width):
            if screen_color_matrix[i][j] == 0:
                is_full = False
                continue
        if not is_full:
            new_matrix[index] = screen_color_matrix[i]
            index -= 1
        else:
            n_full_line += 1
    screen_color_matrix = new_matrix


running = True
stop = False
gameover = True
counter = 0
live_cube = 0

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if gameover:
                gameover = False
                live_cube = CubeShape()
                break
            if event.key == pygame.K_LEFT:
                live_cube.left()
            elif event.key == pygame.K_RIGHT:
                live_cube.right()
            elif event.key == pygame.K_DOWN:
                live_cube.down()
            elif event.key == pygame.K_UP:
                live_cube.rotate()
            elif event.key == pygame.K_SPACE:
                while live_cube.down() == True:
                    pass

    if gameover is False and counter % (FPS // level) == 0:
        if live_cube.down() == False:
            for cube in live_cube.get_all_gridpos():
                screen_color_matrix[cube[0]][cube[1]] = live_cube.color
            live_cube = CubeShape()
            counter=0
            if live_cube.conflict(live_cube.center):
                gameover = True
                live_cube = 0
                screen_color_matrix = [[0] * box_width for i in range(box_height)]

        remove_full_line()
    counter += 1

    screen.fill(black)
    draw_grids()
    draw_matrix()
    if live_cube != 0:
        live_cube.draw()
    if gameover:
        show_gameover(screen)
    pygame.display.update()