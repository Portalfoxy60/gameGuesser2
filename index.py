import pygame
from model import Category, Word
from screens import ScreenShower
import pygame_widgets
width = 1200
height = 800
window_caption = "Word Guesser"
FPS = 120 # частота обновления экрана
background = (154, 213, 252)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(window_caption)
clock = pygame.time.Clock()
screen.fill(background)
pygame.display.update() # обновление экрана, чтобы заменять элементы

my_screen = ScreenShower(pygame, screen, background)

my_screen.show_main_screen() # вывод функции главного экрана
# обработчик события для того, чтобы :
# 1) выводить постоянно очки в главном экране игры
# 2) закрыть игру на ЕСК или крестик
# 3) цикл для перебирания кнопок в массиве и дальнейший вывод этих кнопок

done = True
while done :
  events = pygame.event.get()
  my_screen.check_score()
  for event in events:
    if event.type == pygame.QUIT:
      done = False
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        done = False
    for n in my_screen.button_massive:
      n.listen(event)
  pygame_widgets.update(events)
  pygame.display.update()
  clock.tick(FPS)  # в каком темпе будет обновление экрана по FPS
pygame.quit() # выход

