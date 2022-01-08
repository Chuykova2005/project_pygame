import os
import sys
import pygame


class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 600
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Mario')
        self.recty = self.height - 289
        self.rectx = -10
        self.fps = 50
        self.isjump = False
        self.count = 25

    def terminate(self):
        pygame.quit()
        sys.exit()

    def jump(self):
        if self.count >= -25:
            self.recty += self.count / 2.5
            self.count -= 1
        else:
            self.isjump = False
            self.count = 25

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def run_game(self):
        run = True
        while run:
            fon = pygame.transform.scale(self.load_image('gamefon.jpg'), (self.width, self.height))
            self.screen.blit(fon, (0, 0))
            fon2 = pygame.transform.scale(self.load_image('grass2.png'), (600, 124))
            self.screen.blit(fon2, (0, self.height - 124))
            dino = pygame.transform.scale(self.load_image('dino1.png'), (216, 289))
            self.screen.blit(dino, (self.rectx, self.height - self.recty))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        self.isjump = True
                    if self.isjump:
                        self.jump()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def start_screen(self):
        intro_text = ["Динозаврик Гугл"]

        fon = pygame.transform.scale(self.load_image('pretty.jpg'), (self.width, self.height))
        self.screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('purple'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return  # начинаем игру
            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = App()
    app.start_screen()
    app.run_game()
