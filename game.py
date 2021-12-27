import pygame


class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 600
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))

    def start_window(self):
        pass


if __name__ == '__main__':
    app = App()
    app.start_window()
