import pygame, sys, random
from pygame.math import Vector2

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.display.set_caption('Snake')
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size * cell_number,cell_size * cell_number))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None,25)

class fruit:
    def __init__(self):
        self.randomize()
        self.apple = pygame.image.load('Graphics and Sounds/Graphics/apple.png').convert_alpha()

    def draw_fruit(self):
        fruit_rectangle = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        screen.blit(self.apple,fruit_rectangle)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics and Sounds/Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics and Sounds/Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics and Sounds/Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics and Sounds/Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics and Sounds/Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics and Sounds/Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics and Sounds/Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics and Sounds/Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics and Sounds/Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics and Sounds/Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics and Sounds/Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics and Sounds/Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics and Sounds/Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics and Sounds/Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Graphics and Sounds/Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block = self.body[index+1]-block
                next_block = self.body[index-1]-block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    def move_snake(self):
        if self.new_block == True:
            body = self.body[:]
            self.new_block = False
        else:
            body = self.body[:-1]
        body.insert(0,body[0] + self.direction)
        self.body = body[:]

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]

        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]

        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class main:
    def __init__(self):
        self.snake = snake()
        self.fruit = fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.draw_score()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if self.snake.body[0].x > cell_number-1 or self.snake.body[0].x < 0 or self.snake.body[0].y > cell_number-1 or self.snake.body[0].y < 0:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_colour = (167,209,61)

        for row in range(cell_number):
            for col in range(cell_number):
                grass_rect = pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                if col % 2 == 0 and row % 2 == 0 or col % 2 == 1 and row % 2 == 1:
                    pygame.draw.rect(screen,grass_colour,grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = self.fruit.apple.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 10,apple_rect.height)

        pygame.draw.rect(screen,(134,182,79),bg_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect,2)
        screen.blit(score_surface,score_rect)
        screen.blit(self.fruit.apple,apple_rect)

main_game = main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)

    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)