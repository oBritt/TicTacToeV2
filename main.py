from tkinter.ttk import Button

import pygame
import numpy as np


class Button:
    def __init__(self, x, y, width, height, color_button, color_text, text):
        self.x = x
        self.y = y
        self.color_button = color_button
        self.color_text = color_text
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.Font(None, int(self.height // 1.5))

    def render(self, screen):
        text_surface = self.font.render(self.text, True, self.color_text)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        pygame.draw.rect(screen, self.color_button, (self.x, self.y, self.width, self.height), border_radius=int((self.width * self.height) ** 0.35))
        screen.blit(text_surface, text_rect)



class Game:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.should_stop = False
        self.menu = True
        self.buttons = []
        button_width = width // 3.5
        button_height = height // 6
        for i in range(3):
            self.buttons.append(Button((width - button_width) // 2, button_height + 1.3 * i * button_height, button_width, button_height, 'red', 'black', 'exit'))

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_stop = True

    def display_menu(self):
        for button in self.buttons:
            button.render(self.screen)

    def start(self):

        while not self.should_stop:
            self.screen.fill('white')
            self.handle_event()
            if self.menu:
                self.display_menu()
            pygame.display.flip()
        pygame.quit()


def main():
    g = Game(1024, 720)
    g.start()

if __name__ == '__main__':
    main()
    print("ASD")



# import pygame
#
# # pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
# dt = 0
#
# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
#
# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("purple")
#
#     pygame.draw.circle(screen, "red", player_pos, 40)
#
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_w]:
#         player_pos.y -= 300 * dt
#     if keys[pygame.K_s]:
#         player_pos.y += 300 * dt
#     if keys[pygame.K_a]:
#         player_pos.x -= 300 * dt
#     if keys[pygame.K_d]:
#         player_pos.x += 300 * dt
#
#     # flip() the display to put your work on screen
#     pygame.display.flip()
#
#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     dt = clock.tick(60) / 1000
#
# pygame.quit()