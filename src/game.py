import pygame
import random
import time
from database import Database

#variables
time_limit = 2
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

class Game:
    

    def __init__(self, username, database):
        '''Initializes the game and links to database.
        args: database - str, the database
        username - str, the username'''
        self.username = username
        self.database = database
        self.score = 0
        self.game_over = False
        self.start_time = time.time()  
        self.game_time_limit = 30
        self.circle_spawn_time = time.time()
        self.time_limit = 2
        self.timeout = 30  
        self.time_left = self.timeout
        self.circle_radius = 50 
        self.circle_color = pygame.Color('green') 
        self.circle_position = self.spawn_circle()
        self.last_circle_spawn_time = time.time()

    def get_time_left(self):
        """Returns the time left in the game."""
        elapsed_time = time.time() - self.start_time 
        time_left = max(0, self.game_time_limit - elapsed_time)
        return time_left

        
    def spawn_circle(self):
        '''Spawn circle in random place.'''
        x = random.randint(self.circle_radius, 800 - self.circle_radius)
        y = random.randint(self.circle_radius, 600 - self.circle_radius)
        self.time_limit = 2
        return (x, y)
        


    def draw(self, screen):
        '''Draws the circle and the score.'''
        if not self.game_over:
            pygame.draw.circle(screen, self.circle_color, self.circle_position, self.circle_radius)
        else:
            font = pygame.font.Font(None, 36)
            game_over_text = font.render(f"Game Over! Final Score: {self.score}", True, pygame.Color('red'))
            screen.blit(game_over_text, (250, 150))
            high_score = self.get_high_score()
            if high_score:
                high_score_text = font.render(f"High Score: {high_score[0]}: {high_score[1]}", True, pygame.Color('yellow'))
                screen.blit(high_score_text, (200, 250))

    def check_click(self, mouse_pos):
        '''Determines if circle was clicked.
        args: mouse_pos: touple - x and y coordinates of cursor.
        '''
        if self.game_over:
            return
        mouse_x, mouse_y = mouse_pos
        circle_x, circle_y = self.circle_position
        distance = ((mouse_x - circle_x)**2 + (mouse_y - circle_y)**2)**0.5
        if distance <= self.circle_radius:
            self.score += 5 
            self.circle_position = self.spawn_circle()
            self.circle_clicked_time = time.time()  
            print(f"Circle clicked! Score: {self.score}")  # Debugging log
            self.time_left = 2 


            
    def check_time_out(self):
        """Check if the time has run out and update time_left."""
        if self.game_over:
            return
        elapsed_time = time.time() - self.circle_spawn_time
        self.time_left = max(0, self.time_left - elapsed_time) 
        if self.time_left <= 0:
            self.game_over = True
            print(f"Game Over! Final Score: {self.score}")  # Debugging log
            
    def get_high_score(self):
        return self.database.get_high_score()
    
    def save_score(self):
        '''Saves score to database.'''
        if self.score > self.database.get_high_score()[1]:  
            self.database.save_high_score(self.username, self.score)

    def reset(self):
        """Reset the game for a new session"""
        self.score = 0
        self.game_over = False
        self.start_time = time.time()  
        self.spawn_circle()  

