import os
import sys
import pygame


class Dino(pygame.sprite.Sprite):
    def __init__(self, app):
        super().__init__(app.herogroup)
        self.image = app.load_image('dino1.png')
        self.screen = app.screen
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 100

        self.isjump = False
        self.count = 25
        self.isrun = True


    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def jump(self):
        if self.count >= -25:
            self.rect.y += self.count / 2.5
            self.count -= 1
        else:
            self.isjump = False
            self.count = 25

    def run(self):
        if self.isrun and not self.isjump:
            self.rect.x += 5


class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 600
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Dino')
        self.fps = 60
        self.herogroup = pygame.sprite.Group()

    def terminate(self):
        pygame.quit()
        sys.exit()

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
        dino = Dino(self)
        while run:
            fon2 = pygame.transform.scale(self.load_image('grass2.png'), (600, 124))
            self.screen.blit(fon2, (0, self.height - 124))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        self.isjump = True
                    if self.isjump:
                        dino.jump()
            self.herogroup.draw(self.screen)
            self.herogroup.update(1,0)
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
    # app.start_screen()
    app.run_game()
