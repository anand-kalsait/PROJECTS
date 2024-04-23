from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
# Importing required modules
import sys
import pygame
from pygame.math import Vector2
import random

# All Class
class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(12,12),Vector2(11,12),Vector2(10,12)]
        self.direction = Vector2(0,0)
        self.new_block = False

        # Images for the Head of the Snake
        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()
        # Images for Tail of the Snake
        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()
        # Images for the Body of the Snake
        self.body_vertical = pygame.image.load("Graphics/body_vertical.png").convert_alpha()
        self.body_horizontal = pygame.image.load("Graphics/body_horizontal.png").convert_alpha()
        self.body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()
        # Sound for the Fruit when eaten
        self.crunch_sound = pygame.mixer.Sound("Sound/crunch.wav")
        
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = block.x*cell_size
            y_pos = block.y*cell_size
            block_rect = pygame.Rect((x_pos,y_pos,cell_size,cell_size))

            if index == 0:
                screen.blit(self.head,block_rect)
            elif index == len(self.body)-1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x: screen.blit(self.body_vertical,block_rect)
                elif previous_block.y == next_block.y: screen.blit(self.body_horizontal,block_rect)
                else: 
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    if previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    if previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    if previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)
    
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False  
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True 

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset_snake(self):
        self.body = [Vector2(12,12),Vector2(11,12),Vector2(10,12)]
        self.direction = Vector2(0,0)
        
class Fruit:
    def __init__(self) -> None:
        self.random_pos()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size,self.pos.y*cell_size,
                                 cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        # pygame.draw.rect(screen,(255,10,0),fruit_rect)

    def random_pos(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)

    def reset_fruit(self):
        self.random_pos()

class Main:
    def __init__(self) -> None:
        self.snake = Snake()
        self.fruit = Fruit()
        # Background Game Music in loop
        pygame.mixer.music.load("Sound/8-bit-space.mp3")
        pygame.mixer.music.play(loops=-1, start=1, fade_ms=1000)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.random_pos()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.random_pos()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset_snake()
        self.fruit.reset_fruit()

    def draw_grass(self):
        grass_color = (150,245,60)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,
                                                 cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(col*cell_size,row*cell_size,
                                                 cell_size,cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
        
    def draw_score(self):
        score_text = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text, True ,(50,50,50))
        score_x = int(cell_size*cell_number-60)
        score_y = int(cell_size + 20)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top,
                              apple_rect.width + score_rect.width + 10, apple_rect.height)
        
        pygame.draw.rect(screen, (210,210,210), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen, (50,50,50), bg_rect,2)

# Inititalizing Pygame modelue
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# All Variables
cell_size = 40
cell_number = 25


# All Objects
# Setting the Display size
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))  
# Creating a CLock Object to compansate for the DeltaTime
clock = pygame.time.Clock()
apple = pygame.image.load("Graphics/apple.png").convert_alpha()
game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)
gameover_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 100)


Screen_Update = pygame.USEREVENT
pygame.time.set_timer(Screen_Update,150)

main_game = Main()


# Game Loop
while True:
    # To check if player is trying to Exit the Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == Screen_Update:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)

    # Background Color 
    screen.fill((100,200,50))
    # Draw elements from main_game obj
    main_game.draw_elements()
    # Draw all the content on screen
    pygame.display.update()
    # The While loop will only tick for 60 fps
    clock.tick(60)


