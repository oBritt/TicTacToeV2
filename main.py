import pygame
import numpy as np
from abc import ABC, abstractmethod
import time
import subprocess


class Button(ABC):
    def __init__(self, x, y, width, height, color_button, color_text, text):
        self.x = x
        self.y = y
        self.color_button = color_button
        self.color_text = color_text
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.Font(None, int(self.height // 1.5))
        self.hover_font = pygame.font.Font(None, int(self.height // 1.3))

    def is_howering(self, x, y):
        return x >= self.x and x <= self.x + self.width and y >= self.y and y <= self.y + self.height

    def render(self, screen, x, y, clicked):
        if self.is_howering(x, y):
            if clicked:
                text_surface = self.font.render(self.text, True, self.color_text)
                text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
                pygame.draw.rect(screen, self.color_button, (self.x, self.y, self.width, self.height), border_radius=int((self.width * self.height) ** 0.35))
                return self.action()
            text_surface = self.hover_font.render(self.text, True, (0, 0, 0))
            dx = self.width // 12
            dy = self.height // 12
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            new_color = (self.color_button[0] * 0.85, self.color_button[1] * 0.85, self.color_button[2] * 0.85)
            pygame.draw.rect(screen, new_color, (self.x - dx, self.y - dy, self.width + dx * 2, self.height + dy * 2), border_radius=int((self.width * self.height) ** 0.35))
        else:
            text_surface = self.font.render(self.text, True, self.color_text)
            text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            pygame.draw.rect(screen, self.color_button, (self.x, self.y, self.width, self.height), border_radius=int((self.width * self.height) ** 0.35))

        screen.blit(text_surface, text_rect)

    @abstractmethod
    def action(self):
        pass

class ExitButton(Button):
    def action(self):
        return [1, 0, 0]

class Start0Button(Button):
    def action(self):
        return [0, 0, -1]

class StartXButton(Button):
    def action(self):
        return [0, 0, 1]
    


class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.should_stop = False
        self.menu = True
        self.buttons = []
        self.button_width = width // 3.5
        self.button_height = height // 6
        self.buttons.append(StartXButton((width - self.button_width) // 2, self.button_height + 1.3 * 0 * self.button_height, self.button_width, self.button_height, (255, 32, 32), (35, 35, 35), 'Start X'))
        self.buttons.append(Start0Button((width - self.button_width) // 2, self.button_height + 1.3 * 1 * self.button_height, self.button_width, self.button_height, (255, 32, 32), (35, 35, 35), 'Start 0'))
        self.buttons.append(ExitButton((width - self.button_width) // 2, self.button_height + 1.3 * 2 * self.button_height, self.button_width, self.button_height, (255, 32, 32), (35, 35, 35), 'Exit'))
        self.pressed = False
        self.clock = pygame.time.Clock()
        self.player = 1
        self.map = np.zeros([3, 3], dtype="int32")
        self.last_move = 0
        self.amount_of_moves = 0
        self.text_surface = None
        self.text_rect = None
        self.play_again = None
        self.font = pygame.font.Font(None, 64)


    def handle_event(self):
        self.pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_stop = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.pressed = True
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    self.should_stop = True


    def display_menu(self):
        x, y = pygame.mouse.get_pos()
        for button in self.buttons:
            t = button.render(self.screen, x, y, self.pressed)
            if t is not None:
                self.should_stop = t[0]
                self.menu = t[1]
                self.player = t[2]
                self.last_move = time.time()
                self.amount_of_moves = 0
                self.map = np.zeros([3, 3], dtype="int32")


    def draw_circle(self, top_left, color, width, side, i, j):
        pygame.draw.circle(self.screen, color, (top_left[0] + side // 6 + side // 3 * j, top_left[1] + side // 6 + side // 3 * i), int(side / 6 * 0.75), int(width * 1.5))

    def draw_cross(self, top_left, color, width, side, i, j):
        transformed = (top_left[0] + side / 3 * j, top_left[1] + side / 3 * i)
        start = [transformed[0] + int(side / 3 * 0.15), transformed[1] + int(side / 3 * 0.15)]
        end = [transformed[0] + int(side  / 3 * 0.85), transformed[1] + int(side / 3 * 0.85)]
        pygame.draw.line(self.screen, color, start, end, int(width * 1.5)) 
        start[1], end[1] = end[1], start[1]
        pygame.draw.line(self.screen, color, start, end, int(width * 1.5))

    def get_current_pos(self):
        for i in range(3):
            t = np.sum(self.map[:, i])
            if t == 3:
                return self.player
            if t == -3:
                return -self.player
            t = np.sum(self.map[i, :])
            if t == 3:
                return self.player
            if t == -3:
                return -self.player
        t = self.map[0, 0] + self.map[1, 1] + self.map[2, 2]
        if t == 3:
            return self.player
        if t == -3:
            return -self.player
        t = self.map[2, 0] + self.map[1, 1] + self.map[0, 2]
        if t == 3:
            return self.player
        if t == -3:
            return -self.player
        return 0

    def max_min(self, current_move, res=0):
        t = self.get_current_pos()
        if (t != 0):
            return t
        if current_move >= 9:
            return 0
        arr = []
        for y in range(3):
            for x in range(3):
                if self.map[y, x] == 0:
                    self.map[y, x] = 1 if current_move % 2 == 0 else -1
                    arr.append([y * 3 + x, self.max_min(current_move + 1, 1)])
                    self.map[y, x] = 0
        if current_move % 2 == 1:
            max_or_min = 1
        else:
            max_or_min = 0
        if self.player == -1:
            max_or_min = not max_or_min
        arr = sorted(arr, key=lambda x: x[1])
        if max_or_min == 1:
            return arr[0][res]
        else:
            return arr[-1][res]

    def make_move_ai(self):
        if self.player == 1 and self.amount_of_moves % 2 == 0:
            return
        if self.player == -1 and self.amount_of_moves % 2 == 1:
            return
        if self.last_move + 0.3 > time.time() and self.play_again is None:
            return
        start = time.time()
        command = ["./a.out"] 
        for i in range(3):
            for j in range(3):
                command.append(str(self.map[i, j]))
        command.append(str(self.amount_of_moves))
        command.append(str(self.player))
        result = subprocess.run(command, capture_output=True)
        decoded_str = result.stdout.decode('utf-8')
        # print("--",decoded_str, "--")
        t = int(decoded_str)
        # print(time.time() - start)
        # start = time.time()
        # t = self.max_min(self.amount_of_moves)
        # print(t)
        # print(time.time() - start)
        self.map[int(t / 3), int(t % 3)] = -self.player 
        self.amount_of_moves += 1
        self.last_move = time.time()

    def display_game(self):
        x, y = pygame.mouse.get_pos()
        side = int(min(self.width, self.height) * 0.75)
        side -= side % 3
        top_left = ((self.width - side) // 2, (self.height - side) // 2)
        width = side / 80
        width = int(width)
        color = (25, 25, 25)
        if self.play_again is not None:
            color = (140, 140, 140)
        if width < 2:
            width = 2
        for i in range(2):
            start = (top_left[0] + int(side * (i + 1) / 3), top_left[1])
            pygame.draw.rect(self.screen, color, (start[0] - width, start[1], width * 2, side), border_radius=width)
        for i in range(2):
            start = (top_left[0], top_left[1] + int(side * (i + 1) / 3))
            pygame.draw.rect(self.screen, color, (start[0], start[1] - width, side, width * 2), border_radius=width)

        self.make_move_ai()
        for i in range(3):
            for j in range(3):
                if self.map[i, j] == -1:
                    self.draw_circle(top_left, color, width, side, i, j)
                elif self.map[i, j] == 1:
                    self.draw_cross(top_left, color, width, side, i, j)
                else:
                    if time.time() >= self.last_move + 0.2 and self.get_current_pos() == 0:
                        step = side // 3
                        current_top_left = (top_left[0] + j * step, top_left[1] + i * step)
                        if self.play_again is None and x >= current_top_left[0] + width * 2 and x <= current_top_left[0] + step - width * 2 and y >= current_top_left[1] + width * 2 and y <= current_top_left[1] + step - width * 2:
                            if self.player == 1 and self.amount_of_moves % 2 == 0:
                                self.draw_cross(top_left, (200, 200, 200), width, side, i, j)
                                if self.pressed:
                                    self.map[i, j] = self.player
                                    self.last_move = time.time()
                                    self.amount_of_moves += 1
                            elif self.player == -1 and self.amount_of_moves % 2 == 1:
                                self.draw_circle(top_left, (200, 200, 200), width, side, i, j)
                                if self.pressed:
                                    self.map[i, j] = self.player
                                    self.last_move = time.time()
                                    self.amount_of_moves += 1
        if self.play_again is None:
            t = self.get_current_pos()
            if t == 1 or t == -1 or self.amount_of_moves == 9:
                self.play_again = Start0Button((self.width - int(self.button_width * 1.5)) // 2, (self.height - int(self.button_height * 1.5)) // 2, int(self.button_width * 1.5), int(self.button_height * 1.5), (255, 32, 32), (35, 35, 35), "Play Again")
                if t == -1:
                    self.text_surface = self.font.render("You have lost :(", True, (25, 25, 25))
                elif t == 1:
                    self.text_surface = self.font.render("You have won :)", True, (25, 25, 25))
                else:
                    self.text_surface = self.font.render("Good game :|", True, (25, 25, 25))
                self.text_rect = self.text_surface.get_rect(center=(self.width // 2, int(self.height * 0.07)))

        else:
            self.screen.blit(self.text_surface, self.text_rect)
            if time.time() > self.last_move + 1:
                x, y = pygame.mouse.get_pos()
                t = self.play_again.render(self.screen, x, y, self.pressed)
                if t is not None:
                    self.menu = True
                    self.play_again = None
    


    def start(self):
        while not self.should_stop:
            self.screen.fill('white')
            self.handle_event()
            if self.menu:
                self.display_menu()
            else:
                self.display_game()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


def main():
    g = Game(1024, 720)
    g.start()

if __name__ == '__main__':
    main()

