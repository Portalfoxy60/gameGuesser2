import pygame
from pygame_widgets.button import Button
from model import Player, Category, Word
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select, desc, not_, func
from pygame_widgets.textbox import TextBox

import random
import threading
import time
class ScreenShower:
    button_massive = []
    old_words = []

    engine = create_engine("sqlite:///wordsBase.sqlite", echo=True)
    session = Session(engine)
    def __init__(self, pygame, screen, fill):
        self.screen = screen
        self.pygame = pygame
        self.fill = fill
        self.textbox = None
        self.correct_answers_count = 0         
        self.score = 10000
        self.run = True
        self.timer_thread = ""
        self.start_game = False
        self.offset = 0

    def show_main_screen(self):
        self.offset = 0
        for button in self.button_massive:
            button.hide()
        self.screen.fill(self.fill)
        title_font = pygame.font.SysFont("arial", 80)
        title_text = title_font.render("Word Guesser", True,(0,0,0))
        self.screen.blit(title_text, (320, 100))
        
        start_button = Button(self.screen, 520, 400, 100, 40, text="Start!", textColour=(0,0,0), fontSize=40, onClick=lambda:self.show_category_selection_screen())
        start_button.draw()
        self.button_massive.append(start_button)

        score_button = Button(self.screen, 520, 500, 100, 40, text="Scores", textColour=(0,0,0), fontSize=40, onClick=lambda:self.all_scores_screen())
        score_button.draw()
        self.button_massive.append(score_button)

        


        self.pygame.display.flip()


    def all_scores_screen(self):
        self.screen.fill(self.fill)
        title_font = pygame.font.SysFont("arial", 80)
        title_text = title_font.render("SCORE TABLE", True,(0,0,0))
        self.screen.blit(title_text, (320, 100))
        stmt = select(Player).order_by(desc(Player.scores)).limit(10).offset(self.offset)
        stmt3 = select(func.count()).select_from(Player)
        player_count = self.session.execute(stmt3).scalar()
        
        
        self.players_view(stmt)
        
        for button in self.button_massive:
            button.hide()
        if player_count > 10:
            stmt = select(Player).order_by(desc(Player.scores)).limit(10).offset(self.offset)
            next_score_button = Button(self.screen, 800, 600, 120, 40, text=">", text_color=(0,0,0), fontSize=100, onClick=lambda:self.player_pagination())
            next_score_button.draw()
            self.button_massive.append(next_score_button)
            

        exit_button = Button(self.screen, 500, 750, 100, 40, text="exit", textColour=(0,0,0), fontSize=40, onClick=lambda:self.show_main_screen())
        exit_button.draw()
        self.button_massive.append(exit_button)
        
        
        self.pygame.display.flip()

    def player_pagination(self):
        self.offset += 1
        stmt = select(Player).order_by(desc(Player.scores)).limit(10).offset(self.offset*10)
        self.players_view(stmt)
        
        
    
    def players_view(self, array):
        r=self.offset*10+1
        position = 1
        player_surface = self.pygame.Surface((550,450))
        player_surface.fill((154, 213, 252))
        for a in self.session.scalars(array):
            text = pygame.font.SysFont("arial", 60)
            score_table = text.render("Rank\tName\tScores", True, (0,0,0))
            player_surface.blit(score_table, (50, 0))
            
            name = a.name
            scores = a.scores
            table = pygame.font.SysFont("arial", 35)
            column_rows=table.render(f"{r}\t{name}\t{scores}", True, (0,0,0))
            player_surface.blit(column_rows, (150, 20+position*38))
            position+=1
            r+=1
        self.screen.blit(player_surface, (300,250))
    def show_category_selection_screen(self):
        for button in self.button_massive:
            button.hide()
        self.screen.fill(self.fill)
        title_font = self.pygame.font.SysFont("arial", 60)
        title_text = title_font.render("Choose the category and enter the name", True, (0, 0, 0))
        self.screen.blit(title_text, (60, 50))

        stmt2 = self.session.query(Category)
        k = 5

        for c in stmt2:
            category_name = c.name  
            category_button = Button(self.screen, 500, k * 50, 150, 40, text=f"{category_name}", textColour=(0,0,0), fontSize=40, onClick=lambda name=category_name: self.check_name(name))
            category_button.draw()
            self.button_massive.append(category_button)
            k += 1



        self.textbox = TextBox(self.screen, 200, 600, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=lambda:print(textbox.getText()), radius=10, borderThickness=5)
        
        self.pygame.display.flip()

    def check_name(self, categoryId):
            if self.textbox.getText() == "":
                return
            save_name = self.textbox.getText()
            self.player_name = save_name
            self.game_screen(categoryId)
            

    def game_screen(self, categoryId):
        for button in self.button_massive:
            button.hide()
            self.textbox.hide()
        self.screen.fill(self.fill)
        

        score_font = pygame.font.SysFont("arial", 80)
        score_text = score_font.render(f"{self.score}", True,(0,0,0))
        


        title_font = pygame.font.SysFont("arial", 80)
        title_text = title_font.render("Word Guesser", True,(0,0,0))
        self.screen.blit(title_text, (320, 100))
        words_in_category = self.session.query(Word).join(Category).filter(Category.name == categoryId).filter(not_(Word.word.in_(self.old_words))).all()
        print(self.old_words)
        score_surface = self.pygame.Surface((500,100))

        score_surface.fill((154, 213, 252))
        score_surface.blit(score_text, (10, 10))
        self.screen.blit(score_surface, (800,10))
        


        random_word = random.choice(words_in_category).word
        self.old_words.append(random_word)
        print(random_word)
        word_chars = list(random_word)
        random.shuffle(word_chars)
        shuffled_word = ''.join(word_chars)

        word_text = title_font.render(shuffled_word, True, (0, 0, 0))
        self.screen.blit(word_text, (420, 300))
        self.pygame.display.update() 

        self.textbox = TextBox(self.screen, 200, 500, 800, 80, fontSize=50,
                  borderColour=(255, 0, 0), textColour=(0, 200, 0),
                  onSubmit=lambda:print(Textbox.getText()), radius=10, borderThickness=5)

        next_button = Button(self.screen, 500, 700, 100, 100, text=">", colour=(154, 213, 252), fontSize=100, onClick=lambda: self.check_answer(categoryId, random_word, score_surface))
        next_button.draw()
        self.button_massive.append(next_button)

        timer_surface = self.pygame.Surface((200,100))
        
        if self.start_game == False:
            self.timer_thread = threading.Thread(target=lambda: self.timer(timer_surface, score_surface))
            self.timer_thread.daemon = True  
            self.timer_thread.start()
            self.start_game = True
            timer_surface.fill((154, 213, 252))
            self.screen.blit(timer_surface,(10,10))
            score_surface.fill((154, 213, 252))
            score_surface.blit(score_text, (10, 10))
            self.screen.blit(score_surface,(800,10))
            
        return categoryId

        self.pygame.display.flip()

    

    

    def check_answer(self,categoryId, random_word, score_surface):
        user_input = self.textbox.getText().lower()  
        if user_input == random_word:
            self.correct_answers_count += 1
            if self.correct_answers_count == 10:
                self.show_score_screen()
                self.run = False
                self.timer_thread.join()
                self.start_game = False
            else:
                categoryId = self.game_screen(categoryId)
        else:
            self.score-=100
            score_font = pygame.font.SysFont("arial", 80)
            score_text = score_font.render(f"{self.score}", True,(0,0,0))
            score_surface.fill((154, 213, 252))
            score_surface.blit(score_text, (10, 10)) 
            self.screen.blit(score_surface,(800,10))
        


    def timer(self, surface, score_surface):
        seconds = 0

        while self.run:
            time_font = pygame.font.SysFont("arial", 80)
            time_text = time_font.render(f"{seconds}", True,(0,0,0))
            seconds += 1
            surface.fill((154, 213, 252))
            surface.blit(time_text, (10, 10)) 
            self.screen.blit(surface,(10,10))
            
            if seconds%61 == 0:
                self.score-=1000
                score_font = pygame.font.SysFont("arial", 80)
                score_text = score_font.render(f"{self.score}", True,(0,0,0))
                score_surface.fill((154, 213, 252))
                score_surface.blit(score_text, (10, 10)) 
                self.screen.blit(score_surface,(800,10))

            self.pygame.display.flip()
            time.sleep(1)

    def show_score_screen(self):
        self.run = False
        self.timer_thread.join()
        self.start_game = False
        for button in self.button_massive:
            button.hide()
            self.textbox.hide()
        self.screen.fill(self.fill)
        exit_button = Button(self.screen, 500, 750, 100, 40, text="exit", textColour=(0,0,0), fontSize=40, onClick=lambda:self.show_main_screen())
        exit_button.draw()
        self.button_massive.append(exit_button)

        title_font = pygame.font.SysFont("arial", 80)
        title_text = title_font.render("Your Score", True, (0, 0, 0))
        self.screen.blit(title_text, (320, 100))

        name_font = pygame.font.SysFont("arial", 80)
        name_text = name_font.render(f"Player: {self.player_name}", True, (0, 0, 0))
        self.screen.blit(name_text, (250, 250))

        score_font = pygame.font.SysFont("arial", 80)
        final_score_text = score_font.render(f"Final Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(final_score_text, (250, 350))

        self.save_player_score(self.player_name, self.score)

        self.pygame.display.flip()

    def save_player_score(self, player_name, score):
        existing_player = self.session.query(Player).filter(Player.name == player_name).first()

        if existing_player:
            existing_player.scores = score
        else:
            new_player = Player(name=player_name, scores=score)
            self.session.add(new_player)

        self.session.commit()


    def bad_end_screen(self):
        for button in self.button_massive:
            button.hide()
            self.textbox.hide()
        self.screen.fill((255,0,0))
        title_font = pygame.font.SysFont("arial", 80)
        title_text = title_font.render("YOU ARE LOSE!", True,(0,0,0))
        self.screen.blit(title_text, (320, 100))
        self.pygame.display.flip()
    def check_score(self):
        if self.score <= 0:
            self.bad_end_screen()
            self.run = False
            self.timer_thread.join()
