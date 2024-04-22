# Importing required modules
import sys
import pygame
from pygame.math import Vector2
import random

# All Class
class Snake:
    def __init__(self) -> None:
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = block.x*cell_size
            y_pos = block.y*cell_size
            block_rect = pygame.Rect((x_pos,y_pos,
                                      cell_size,cell_size))
            pygame.draw.rect(screen, (0,50,220),block_rect)
    
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

class Main:
    def __init__(self) -> None:
        self.snake = Snake()
        self.fruit = Fruit()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
    
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.random_pos()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


# Inititalizing Pygame modelue
pygame.init()

# All Variables
cell_size = 40
cell_number = 25


# All Objects
# Setting the Display size
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))  
# Creating a CLock Object to compansate for the DeltaTime
clock = pygame.time.Clock()
apple = pygame.image.load("Snakes_Game/apple.png").convert_alpha()

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


