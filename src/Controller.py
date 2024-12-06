import pygame
import sys
from game import Game
from database import Database

width = 800
height = 600
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

font = pygame.font.SysFont("Arial", 20)

class Controller:
    
    def __init__(self):
        pygame.init()
        self.database = Database()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Circle Clicker Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True
        self.in_game = False
        self.show_start_screen = True
        self.show_game_over_screen = False
        self.username = ""
        
    def game_loop(self):
        while self.running:
            if self.show_start_screen:
                self.username = self.get_username() 
                if self.username:
                    self.game = Game(self.username, self.database) 
                    self.show_start_screen = False 
                    self.in_game = True
                    print(f"Game started for user: {self.username}")  # Debugging log
            if self.in_game:
                self.handle_events()
                self.game.check_click(pygame.mouse.get_pos())
                self.game.check_time_out()
                self.game.draw(self.screen)
                time_left = self.game.get_time_left()
                time_left_text = self.font.render(f"Time Left: {int(time_left)}s", True, pygame.Color('white'))
                self.screen.blit(time_left_text, (10, 10)) 
                print(f"Game running: Score {self.game.score}, Time Left: {int(time_left)}s")  # Debugging log
                pygame.display.flip()
                if self.game.game_over:
                    print(f"Game Over! Final Score: {self.game.score}") #Debugging log
                    self.show_game_over_screen = True
            if self.show_game_over_screen:
                self.show_game_over_screen_ui()
            pygame.display.flip()
            self.clock.tick(30) 

        pygame.quit()
        
    def handle_events(self):
        '''checks if quit or play again were clicked on end screen.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.in_game and not self.game.game_over:
                    self.game.check_click(event.pos)
                if self.show_game_over_screen:
                    self.handle_game_over_screen_click(event.pos)   
                    
    def show_game_over_screen_ui(self):
        """Display the game over screen UI"""
        self.screen.fill((0, 0, 0))
        game_over_text = self.font.render(f"Game Over! Score: {self.game.score}", True, pygame.Color('red'))
        self.screen.blit(game_over_text, (250, 150))
        high_score = self.game.get_high_score()
        if high_score:
            high_score_text = self.font.render(f"High Score: {high_score[0]}: {high_score[1]}", True, pygame.Color('yellow'))
            self.screen.blit(high_score_text, (200, 250))
        play_again_button = pygame.Rect(150, 400, 200, 50)
        exit_button = pygame.Rect(450, 400, 200, 50)
        pygame.draw.rect(self.screen, (0, 128, 0), play_again_button)
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button)
        play_again_text = self.font.render("Play Again", True, pygame.Color('white'))
        exit_text = self.font.render("Exit", True, pygame.Color('white'))
        self.screen.blit(play_again_text, (play_again_button.x + 50, play_again_button.y + 10))
        self.screen.blit(exit_text, (exit_button.x + 70, exit_button.y + 10))

        pygame.display.flip()
        
    def handle_game_over_screen_click(self, pos):
        """Handle click events on the game over screen buttons"""
        play_again_button = pygame.Rect(150, 400, 200, 50)
        exit_button = pygame.Rect(450, 400, 200, 50)
        if play_again_button.collidepoint(pos):
            self.game.save_score()
            self.game = Game(self.username, self.database)
            self.show_game_over_screen = False  
            self.in_game = True  
        if exit_button.collidepoint(pos):  
            self.running = False           
                                       
    def get_username(self):
        '''Asks user for username'''
        input_box = pygame.Rect(300, 200, 200, 50)
        color_inactive = pygame.Color('red')
        color_active = pygame.Color('blue')
        color = color_inactive
        text = ''
        active = False
        while True:
            self.screen.fill((30, 30, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                    play_button = pygame.Rect(300, 350, 200, 50)
                    if play_button.collidepoint(event.pos) and text != '':
                        return text
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
            title_text = self.font.render("Enter Your Name", True, pygame.Color('white'))
            self.screen.blit(title_text, (300, 150))  
            txt_surface = self.font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width 
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))  
            pygame.draw.rect(self.screen, color, input_box, 2)  
            play_button = pygame.Rect(300, 350, 200, 50)
            pygame.draw.rect(self.screen, (0, 128, 0), play_button) 
            play_text = self.font.render("Play", True, pygame.Color('white'))
            self.screen.blit(play_text, (play_button.x + 70, play_button.y + 10)) 
            pygame.display.flip()  
            self.clock.tick(30)  
        
    def reset_game(self):
        '''function that resets game.'''
        self.game = Game(self.database)
        self.in_game = False
        self.show_game_over_screen = False
        self.show_start_screen = True

    def show_start_screen_ui(self, screen):
        self.screen.fill((0, 0, 0))
        title_text = self.font.render("Enter Your Name", True, pygame.Color('white'))
        play_button = pygame.Rect(300, 300, 200, 50)
        pygame.draw.rect(self.screen, (0, 128, 0), play_button)
        play_text = self.font.render("Play", True, pygame.Color('white'))
        self.screen.blit(title_text, (300, 150))
        self.screen.blit(play_text, (play_button.x + 70, play_button.y + 10))
        pygame.display.flip()
        waiting_for_play = True
        while waiting_for_play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        waiting_for_play = False
                        self.username = self.get_username()
                        self.game = Game(self.username, self.database)
                        self.in_game = True













"""class Controller:
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill('black')
    
    def __init__(self):
    
        docstring
    
        
    
    def mainloop(self):
        
        docstring
        
        run = True
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    exit()

        #2. detect collisions and update models

        #3. Redraw next frame

        #4. Display next frame
        pygame.display.update()"""
        
